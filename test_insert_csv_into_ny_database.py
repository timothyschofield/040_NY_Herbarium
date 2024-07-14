"""

    File: main_ny_csv_to_sql.py
    
    Author: Tim Schofield
    Date: 26 June 2024

    Take the CSV output of main_ny_hebarium and generates SQL to import the spreadsheet into a database
    The columns are duplicated with AI versions for editing

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
def get_sql_vals_from_csv(row):
    
    # A Dict db_col_name: (db_col_type, col_value)
    this_db_cols = ny_db_cols.copy()

    this_db_cols["irn"][1] = csv2sql_val(row["irn"], this_db_cols["irn"])
    
    this_db_cols["darGlobalUniqueIdentifier"][1] = csv2sql_val(row["DarGlobalUniqueIdentifier"], this_db_cols["darGlobalUniqueIdentifier"])    
        
    this_db_cols["darInstitutionCode"][1] = csv2sql_val(row["DarInstitutionCode"], this_db_cols["darInstitutionCode"])     
        
    # DarCatalogNumber is what Frank uses as a unique identifier
    this_db_cols["darCatalogNumber"][1] = csv2sql_val(row["DarCatalogNumber"], this_db_cols["darCatalogNumber"])  
    
    this_db_cols["darRelatedInformation"][1] = csv2sql_val(row["DarRelatedInformation"], this_db_cols["darRelatedInformation"]) 
    
    this_db_cols["darImageURL"][1] = csv2sql_val(row["DarImageURL"], this_db_cols["darImageURL"]) 
    
    this_db_cols["darImageURL_a"][1] = None # No column in CSV
    this_db_cols["darImageURL_b"][1] = None # No column in CSV
    
    this_db_cols["darKingdom"][1] = csv2sql_val(row["DarKingdom"], this_db_cols["darKingdom"]) 
    this_db_cols["darPhylum"][1] = csv2sql_val(row["DarPhylum"], this_db_cols["darPhylum"]) 
    this_db_cols["darFamily"][1] = csv2sql_val(row["DarFamily"], this_db_cols["darFamily"]) 
    this_db_cols["darScientificName"][1] = csv2sql_val(row["DarScientificName"], this_db_cols["darScientificName"]) 
    
    csv_val = row["ColDateVisitedFrom"]
    if type(csv_val) == str: date_list = csv_val.split("-")
    else: date_list = []
    
    if len(date_list) != 3:
        this_db_cols["collectionYYYY"][1] = None
        this_db_cols["collectionMM"][1] = None
        this_db_cols["collectionDD"][1] = None
    else:
        this_db_cols["collectionYYYY"][1] = f'{str(date_list[0])}'
        this_db_cols["collectionMM"][1] =  f'{str(date_list[1])}'
        this_db_cols["collectionDD"][1] =  f'{str(date_list[2])}'  
    
    return this_db_cols


def INSERT_sql_line(ny_db_cols):
    
    db_keys = ny_db_cols.keys()
    db_col_names = ", ".join(db_keys)
    
    db_col_val_str = f""
    for db_col_name, (db_col_type, db_col_val) in ny_db_cols.items():
        if type(db_col_val) == str:
          db_col_val_str = f"{db_col_val_str}'{db_col_val}', " 
        else:
          db_col_val_str = f"{db_col_val_str}{str(db_col_val)}, "  
    
    db_col_val_str = db_col_val_str.replace("None", "NULL") # Not happy with this
    db_col_val_str = db_col_val_str[:-2]
    
    sql = f"INSERT INTO specimenCards ({db_col_names}) \nVALUES ({db_col_val_str});"
    #print("-------")
    #print(sql)

    return sql

"""
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
            
            sql_vals = get_sql_vals_from_csv(row)
            sql_line = INSERT_sql_line(sql_vals)
            
            # print(sql_line)

            #df_output_csv.loc[index, "SQL"] = sql
            
            # Need to escape 'Carex fuscula d'Urv.'
            
            
            print(sql_line)
         
            with connection.cursor() as cursor:
                cursor.execute(sql_line) 
                connection.commit()
            
        #print(f"WRITING: {output_path}")
        #save_dataframe_to_csv(df_to_save=df_output_csv, output_path=output_path)

except Error as error:
    print(f"TIM ERROR: {error}")
    exit()


