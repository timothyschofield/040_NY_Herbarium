"""

    File: main_ny_analysis.py
    
    Author: Tim Schofield
    Date: 01 July 2024

    Compares the difference btween the NY_transcribed input lats and lngs
    and the AI output lats and lngs

"""
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import geopy.distance
from helper_functions_ny_herbarium import get_file_timestamp, save_dataframe_to_csv

ny_input_folder = "ny_analysis_input"
# A copy of the origonal NY_transcribed but with all rows having their own url - two bum rows removed - 1060 rows in total
ny_input_file = "NY_human_transcribed_2024-07-01T12-54-01-1060.csv" 
ny_input_path = Path(f"{ny_input_folder}/{ny_input_file}")

ai_input_folder = "ny_analysis_input"
# With the AI version of the OCR - 1060 rows in total
ai_input_file = "ny_ai_herbarium_transcribed_2024-06-26_ALL_1060.csv"
ai_input_path = Path(f"{ai_input_folder}/{ai_input_file}")

output_folder = "ny_analysis_output"
 
if os.path.exists(ny_input_path) != True:
    print(f"ERROR: {ny_input_path} file does not exits")
    exit()
else:
    print(f"READING: {ny_input_path}")       

if os.path.exists(ai_input_path) != True:
    print(f"ERROR: {ai_input_path} file does not exits")
    exit()
else:
    print(f"READING: {ai_input_path}") 

df_ny_metadata = pd.read_csv(ny_input_path)
df_ai_metadata = pd.read_csv(ai_input_path)

all_lines = []

this_point = geopy.point.Point("3 26m 22s N, 23 27m 30s E")
print(this_point) # 3 26m 22s N, 23 27m 30s E
this_point = geopy.point.Point("-21.1036, 55.4781")
print(this_point) # 21 6m 12.96s S, 55 28m 41.16s E


exit()



for index, row in df_ny_metadata.iloc[0:].iterrows():  
    
    ai_row = df_ai_metadata.iloc[index]
    
    darCatalogNumber = row["DarCatalogNumber"]
    darImageURL = row["DarImageURL"]
    
    darLatitudeDecimal = row["DarLatitudeDecimal"]
    darLongitudeDecimal = row["DarLongitudeDecimal"]
    
    ai_darCatalogNumber = ai_row["DarCatalogNumber"]
    ai_darLatitudeDecimal = ai_row["DarLatitudeDecimal"]
    ai_darLongitudeDecimal = ai_row["DarLongitudeDecimal"]
    ai_darLatitudeDMS = ai_row["LatitudeDMS"]
    ai_darLongitudeDMS = ai_row["LongitudeDMS"]


    # It seems that in the NY human transcribed sheet Lat and Lng are NEVER given in DMS
    # So compare the Decimal versions in AI
    
    if darLatitudeDecimal == "none" or ai_darLatitudeDecimal == "none":
        lat_diff = "N/A"
    else:
        lat_diff = round(abs(float(darLatitudeDecimal) - float(ai_darLatitudeDecimal)), 4)
    
    if darLongitudeDecimal == "none" or ai_darLongitudeDecimal == "none":
        lng_diff = "N/A"
    else:
        lng_diff = round(abs(float(darLongitudeDecimal) - float(ai_darLongitudeDecimal)), 4)
    
    if darLatitudeDecimal != "none" and ai_darLatitudeDecimal != "none" and darLongitudeDecimal != "none" and ai_darLongitudeDecimal != "none":
        coords_1 = (darLatitudeDecimal, darLongitudeDecimal)
        coords_2 = (ai_darLatitudeDecimal, ai_darLongitudeDecimal)
        km_distance = round(geopy.distance.geodesic(coords_1, coords_2).km, 2)
    else:
        km_distance = "N/A"
    
    this_line = dict()
    this_line["NY_Cat_Num"] = darCatalogNumber
    this_line["AI_Cat_Num"] = ai_darCatalogNumber
    this_line["NY_URL"] = darImageURL
    
    this_line["NY_Lat_Dec"] = darLatitudeDecimal
    this_line["NY_Lng_Dec"] = darLongitudeDecimal
    this_line["AI_Lat_Dec"] = ai_darLatitudeDecimal
    this_line["AI_Lng_Dec"] = ai_darLongitudeDecimal
    this_line["AI_Lat_DMS"] = ai_darLatitudeDMS
    this_line["AI_Lng_DMS"] = ai_darLongitudeDMS
    
    this_line["Diff_Lat"] = lat_diff
    this_line["Diff_Lng"] = lng_diff
    this_line["Kilometers"] = km_distance
    
    all_lines.append(this_line)

    if index > 200: break

df_output = pd.DataFrame(all_lines)
print(df_output)

output_path = f"{output_folder}/NY_analysis_{get_file_timestamp()}"
save_dataframe_to_csv(df_to_save=df_output, output_path=output_path)

print("########### END ###########")





































