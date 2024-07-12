"""

    File: main_ny_csv_to_sql.py
    
    Author: Tim Schofield
    Date: 26 June 2024

    Take the CSV output of main_ny_hebarium and generates SQL to import the spreadsheet into a database
    Te columns are duplicated with AI versions for editing


"""

from dotenv import load_dotenv
from helper_functions_ny_herbarium import get_file_timestamp, save_dataframe_to_csv

import os
from pathlib import Path 
import pandas as pd
import time
from datetime import datetime
import json
import sys
print(f"Python version {sys.version}")


def make_sql_line(row):
    eol = f"\n"
    
    sql = f"UPDATE specimenCards SET "
    
    val = row["DarCollector"]
    if type(val) != str: val = ""
    new_str = f"darCollector = '{val}', AI_darCollector = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionTeam"]
    if type(val) != str: val = ""
    new_str = f"collectionTeam = '{val}', AI_collectionTeam = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionNumberPrefix"]
    if type(val) != str: val = ""   
    new_str = f"collectionNumberPreffix = '{val}', AI_collectionNumberPrefix = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionNumber"]
    if type(val) != str: val = ""
    new_str = f"collectionNumber = '{val}', AI_collectionNumber = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionNumberSuffix"]
    if type(val) != str: val = ""
    new_str = f"collectionNumberSuffix = '{val}', AI_collectionNumberSuffix = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionNumberText"]
    if type(val) != str: val = ""
    new_str = f"collectionNumberText = '{val}', AI_collectionNumberText = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["ColDateVisitedFrom"]
    if type(val) != str: val = ""
    date_list = val.split("-")
    if len(date_list) != 3:
        year = ""
        month = ""
        day = ""
    else:
        year = str(date_list[0])
        month =  str(date_list[1])
        day =  str(date_list[2])
        
    new_str = f"collectionDD = '{day}', collectionMM = '{month}', collectionYYYY = '{year}', AI_collectionDD = '{day}', AI_collectionMM = '{month}', AI_collectionYYYY = '{year}',{eol}"
    sql = f"{sql}{new_str}"
    
    val = row["ColDateVisitedTo"]
    if type(val) != str: val = ""
    date_list = val.split("-")
    if len(date_list) != 3:
        year = ""
        month = ""
        day = ""
    else:
        year = str(date_list[0])
        month =  str(date_list[1])
        day =  str(date_list[2])
        
    new_str = f"collectionDD2 = '{day}', collectionMM2 = '{month}', collectionYYYY2 = '{year}', AI_collectionDD2 = '{day}', AI_collectionMM2 = '{month}', AI_collectionYYYY2 = '{year}',{eol}"
    sql = f"{sql}{new_str}"     
      
    val = row["ColVerbatimDate"]
    if type(val) != str: val = ""
    new_str = f"colVerbatimDate = '{val}', AI_colVerbatimDate = '{val}' {eol}" # comma replaced by space
    sql = f"{sql}{new_str}" 
      
    # NO FINAL COMMA BEFORE WHERE
    ##################
   
    # INTEGER
    val = row["DarCatalogNumber"]
    #if type(val) != str: val = ""
    new_str = f"WHERE darCatalogNumber = '{val}';"
    
    #new_str = f"WHERE darCatalogNumber = '{val}' AND transcriptionStateId = 0;" # from Max
    
    sql = f"{sql}{new_str}"

    return sql



"""
Remember - the records will already exist becuse of the irn, url and darCatalogNumber inherited from NY
So we are starting with a preexisting database table that is partialy instanciated in some columns that will never change
and has many empty columns that need updating from a CSV


# works from within Workbench
# For creating a new record
INSERT INTO ny_herbarium.specimenCards (darCollector, AI_darCollector)
VALUES ('G. T. Johnson', 'G. T. Johnson');

# For updateing existing record
UPDATE specimenCards 
SET darCollector = 'G. T. Johnson', AI_darCollector = 'G. T. Johnson'
WHERE darCatalogNumber = 4285750;
"""


time_stamp = get_file_timestamp()

input_folder = "ny_csv_to_sql_input"
input_file = "ny_hebarium_improvement_2024-06-15T23-40-20-1001-ALL.csv"
input_path = Path(f"{input_folder}/{input_file}")

if os.path.exists(input_path) != True:
    print(f"ERROR: {input_path} file does not exits")
    exit()
else:
    print(f"READING: {input_path}")

output_folder = "ny_csv_to_sql_output"
input_file_basename = input_file.split(".")[0] # get ride of the ".csv"
output_file = f"ny_with_sql_{time_stamp}_{input_file_basename}"
output_path = Path(f"{output_folder}/{output_file}")


df_input_csv = pd.read_csv(input_path)

df_output_csv = df_input_csv.copy(deep=True)
df_output_csv["SQL"] = "No SQL"
df_output_csv["SQL"] = df_output_csv["SQL"].astype("string")

from mysql.connector import connect, Error
    
try:

    with connect(host="localhost", user="root", password="password") as connection:
        
        use_db_query = "USE ny_herbarium"
        with connection.cursor() as cursor:
            cursor.execute(use_db_query) 

        for index, row in df_output_csv.iloc[0:].iterrows(): 
            
            sql = make_sql_line(row)

            df_output_csv.loc[index, "SQL"] = sql
            
            with connection.cursor() as cursor:
                cursor.execute(sql) 
                connection.commit()
                
            if index > 10: break


        print(f"WRITING: {output_path}")
        save_dataframe_to_csv(df_to_save=df_output_csv, output_path=output_path)

except Error as error:
    print(f"TIM ERROR: {error}")
    exit()


