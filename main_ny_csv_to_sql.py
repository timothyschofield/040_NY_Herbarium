"""

    File: main_ny_csv_to_sql.py
    
    Author: Tim Schofield
    Date: 26 June 2024

    Take the CSV output of main_ny_hebarium and generates SQL to import the spreadsheet into a database

"""

from dotenv import load_dotenv
from helper_functions_ny_herbarium import get_file_timestamp, is_json, make_payload, clean_up_ocr_output_json_content, are_keys_valid, get_headers, save_dataframe_to_csv

import requests
import os
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime
import json
import sys
print(f"Python version {sys.version}")

time_stamp = get_file_timestamp()

input_folder = "ny_csv_to_sql_input"
input_file = "ny_hebarium_improvement_2024-06-15T23-40-20-1001-ALL.csv"
input_path = Path(f"{input_folder}/{input_file}")

output_folder = "ny_csv_to_sql_output"
input_file_basename = input_file.split(".")[0] # get ride of the ".csv"
output_file = f"ny_with_sql_{time_stamp}_{input_file_basename}"
output_path = Path(f"{output_folder}/{output_file}")


df_input_csv = pd.read_csv(input_path)

df_output_csv = df_input_csv.copy(deep=True)
df_output_csv["SQL"] = "No SQL"
df_output_csv["SQL"] = df_output_csv["SQL"].astype("string")

# WHERE column_name IS NULL;

eol = f"\n"
for index, row in df_output_csv.iloc[0:].iterrows():  
    count = index + 1
    
    sql = f"UPDATE specimenCards SET "
    
    val = row["DarCatalogNumber"]
    #if val.isdigit(): int_val = int(val)
    #else: int_val = None
    str = f"darCatalogNumber = {val},{eol}"
    sql = f"{sql}{str}" 

    val = row["DarCollector"]
    str = f"darCollector = '{val}', AI_darCollector = '{val}',{eol}"
    sql = f"{sql}{str}"

    val = row["CollectionTeam"]
    str = f"collectionTeam = '{val}', AI_collectionTeam = '{val}',{eol}"
    sql = f"{sql}{str}"

    val = row["CollectionNumberPrefix"]
    str = f"collectionNumberPreffix = '{val}', AI_collectionNumberPrefix = '{val}',{eol}"
    sql = f"{sql}{str}"

    val = row["CollectionNumber"]
    if val.isdigit(): int_val = int(val)
    else: int_val = None
    str = f"collectionNumber = {int_val}, AI_collectionNumber = {int_val},{eol}"
    sql = f"{sql}{str}"

    val = row["CollectionNumberSuffix"]
    str = f"collectionNumberSuffix = '{val}', AI_collectionNumberSuffix = '{val}',{eol}"
    sql = f"{sql}{str}"

    val = row["CollectionNumberText"]
    str = f"collectionNumberText = '{val}', AI_collectionNumberText = '{val}',{eol}"
    sql = f"{sql}{str}"

    ##################
   
    # WHERE column_name IS NULL; 
    val = row["DarCatalogNumber"]
    #if val.isdigit(): int_val = int(val)
    #else: int_val = None
    str = f"WHERE darCatalogNumber = {val} OR darCatalogNumber IS NULL;"
    sql = f"{sql}{str}"
    
    
    df_output_csv.loc[index, "SQL"] = sql


    # print(f"****\n{sql}****")
    if count > 10: break

print(f"WRITING BATCH: {output_path}")
save_dataframe_to_csv(df_to_save=df_output_csv, output_path=output_path)




