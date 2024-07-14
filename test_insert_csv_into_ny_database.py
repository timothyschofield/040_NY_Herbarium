"""

    File: main_ny_csv_to_sql.py
    
    Author: Tim Schofield
    Date: 26 June 2024

    Take the CSV output of main_ny_hebarium and generates SQL to import the spreadsheet into a database
    Te columns are duplicated with AI versions for editing


"""

from dotenv import load_dotenv
from helper_functions_ny_herbarium import get_file_timestamp, save_dataframe_to_csv, csv2sql_val

import os
from pathlib import Path 
import pandas as pd
import time
from datetime import datetime
import json
import sys

from test_ny_cols import ny_db_cols

print(f"Python version {sys.version}")
"""
This is specificaly for this database, its impossible to be totaly general

"""

# Collect all the values from the CSV and turn them into 
# The correct form - string, number, None (NULL) for SQL
def get_values_from_csv(row):
    
    # A Dict db_col_name: (db_col_type, col_value)
    this_db_cols = ny_db_cols.copy()

    this_db_cols["irn"][1] = csv2sql_val(row["irn"], this_db_cols["irn"])
    
    this_db_cols["darGlobalUniqueIdentifier"][1] = csv2sql_val(row["DarGlobalUniqueIdentifier"], this_db_cols["darGlobalUniqueIdentifier"])    
        
    this_db_cols["darInstitutionCode"][1] = csv2sql_val(row["DarInstitutionCode"], this_db_cols["darInstitutionCode"])     
        
    this_db_cols["darCatalogNumber"][1] = csv2sql_val(row["DarCatalogNumber"], this_db_cols["darCatalogNumber"])  
    
    csv_val = row["ColDateVisitedFrom"]
    if type(csv_val) == str: date_list = csv_val.split("-")
    else: date_list = []
    
    if len(date_list) != 3:
        this_db_cols["collectionYYYY"][1] = None
        this_db_cols["collectionMM"][1] = None
        this_db_cols["collectionDD"][1] = None
    else:
        this_db_cols["collectionYYYY"][1] = f"'{str(date_list[0])}'"
        this_db_cols["collectionMM"][1] =  f"'{str(date_list[1])}'"
        this_db_cols["collectionDD"][1] =  f"'{str(date_list[2])}'"   
    
    print(this_db_cols["collectionYYYY"][1])
    print(this_db_cols["collectionMM"][1])
    print(this_db_cols["collectionDD"][1])
    exit()
        





def make_UPDATE_sql_line(row):
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
1) CREATE the specimenCards with irn, darCatalogNumber, urls, etc. columns which are not edited, 
    as well as darCollector, AI_darCollector, collectionTeam, AI_collectionTeam, etc. 
    This is done ONCE

2) INSERT the values for all columns from the CSV. Duplicate values form darCollector to AI_darCollector, etc.
    This is done ONCE
    
3) UPDATE - which columns are updated? and when is dependednt of Max work flow.

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
input_file = "ny_hebarium_improvement_test.csv"
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
            
            sql = get_values_from_csv(row)

            df_output_csv.loc[index, "SQL"] = sql
            
            """
            with connection.cursor() as cursor:
                cursor.execute(sql) 
                connection.commit()
            """
             
            if index > 10: break


        print(f"WRITING: {output_path}")
        save_dataframe_to_csv(df_to_save=df_output_csv, output_path=output_path)

except Error as error:
    print(f"TIM ERROR: {error}")
    exit()


