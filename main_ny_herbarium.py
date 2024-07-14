"""
File : main_ny_herbarium.py

Author: Tim Schofield
Date: 05 June 2024

--------------------------------------------
NY Specimen column meanings

Text on labels is predominently Engish with some in Spanish or French
The "Dar" prefix indicates the column is part of the Darwin Core description
--------------------------------------------

DarCollector	The Collectors name (WITH AUTHORITY FILE)
CollectionTeam	(List of other people involved in the collecting)

CollectionNumberPrefix	(e.g. BN)
CollectionNumber	    (e.g. 456)
CollectionNumberSuffix	(e.g. XV)
CollectionNumberText	(e.g. BN-456-XV) i.e. verbatim

 
ColDateVisitedFrom	    (e.g. 1891-01-) (e.g. 2002-11-19)
ColDateVisitedTo	    (e.g. 1891-01-) (e.g. 2002-11-19)
ColVerbatimDate	        (e.g. Jan 1891) (e.g. 19 Nov 1990)

DarCollectionNotes	  (e.g. [Collector on label: L. Iralrit [?]] OR "Flora of India and Burma." OR [The BIOTA Yemen Project's plant collection])

DarContinent	DarCountry	DarStateProvince	DarCounty	(ALL WITH AUTHORITY FILE)
DarLocality
    (e.g. 
    Lake Mgardok, Babeldaob Island OR 
    
    3rd pool east of road, Duval Creek, 7 mi. 
    north of Armidale, in c. 4" of water, mud bottom OR
    
    47 km N of Daly River Police Station on road to Darwin.)

e.g. 1
Yaundé, Urwaldgebiet - was all that was mentoned
but the following was recorded
Africa	Cameroon	Centre		

e.g. 2
Gabon, 8 km ENE of Bellevue. - was recoded


Township_tab  (NO IDEA rare) (e.g. T35N OR T16N)           in ocr T5S R44E S15
Range_tab	    (NO IDEA rare) (e.g. R35E OR R20E)           in ocr T35N R35E S23 SW1/4
Section_tab	  (NO IDEA rare) (e.g. S23 SW1/4 OR S36 SW1/4) in ocr T16N, R20E, SW^ section 36

DarMinimumElevationMeters	(when a single altitude is given, copy it to both max and min, and do the maths for meter/feet conversion)
DarMaximumElevationMeters	
MinimumElevationFeet	
MaximumElevationFeet	

DarLatitudeDecimal	
DarLongitudeDecimal	 (If the Lat and Lng given in decimal, make a conversion and vica versa)
LatitudeDMS	
LongitudeDMS	

DarGeodeticDatum (e.g. WGS84 The World Geodetic System 1984 - a satalite navigation system OR NAD83 North American Datum 1983)
DarGeorefMethod	(e.g. GPS)


DarCoordinateUncertaintyInMeter	e.g. - rare 1000 OR 703 OR 1971   <<<< This may retult from no lat and lng info and lat and lng being estimated from locality

ColLocationNotes	e.g. [Mexico & Central America] OR [Pacifica] OR [Australia] OR [US & Canada] etc.


FeaCultivated? (Y/N)	      Yes - look for the word Cultivated
FeaPlantFungDescription	    Shrub to 2m OR Herb to 0.5m; spore casings green OR Disk and rays yellow
FeaFrequency	              Abundant OR Occasional OR Common OR Frequent OR Rare at 100 ft. but common at Middlesex 200 ft


HabHabitat	        e.g. on grassy field OR lateau, succulent thicket OR Végétation très basse, ericoide arbustive ou herbacée OR Humid forest in limestone mogote
HabVegetation	      e.g. humid pine-hardwood forest OR low scrub forest (charrascales) OR rain forest OR humid scrub forest (charrascales)
HabSubstrate	      e.g. on tile roof of house OR On rotting log OR On damp rock OR on bark of <Quercus> OR On sandy soil.     <<<<< all start with "on"

SpeOtherSpecimenNumbers_tab	 e.g. PFIMASTE 02129 OR RON 00010095 OR SPF 41191 OR HBR 15094  <<< information mostly not in ocr


OcrText

"""
import openai
from openai import OpenAI
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

MODEL = "gpt-4o" # Context window of 128k max_tokens 4096

load_dotenv()
try:
    my_api_key = os.environ['OPENAI_API_KEY']          
    client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()


input_folder = "ny_herbarium_input"
input_file = "NY_specimens_transcribed.csv"
input_path = Path(f"{input_folder}/{input_file}")

input_jpg_folder = "jpg_folder_input"

output_folder = "ny_herbarium_output"

project_name = "ny_herbarium_transcribed"

batch_size = 20 # saves every
time_stamp = get_file_timestamp()

# This is just blank exept for the columns already filled in like irn and DarImageURL
df_input_csv = pd.read_csv(input_path)

# This would all be fine except that a DarImageURL column can contain multiple image urls in one line seperated a pipes ("|")
# So its easiest just to get it out of the way and make a df copy with each url having its own line - the new df will have more lines obviously
to_transcribe_list = []
for index, row in df_input_csv.iterrows():

    dar_image_url = row["DarImageURL"]
    if "|" in dar_image_url:
        
        url_list = dar_image_url.split("|")
        for url in url_list:
            url = url.strip()
            this_row = df_input_csv.loc[index].copy()
            this_row["DarImageURL"] = url
            to_transcribe_list.append(this_row)
    else:
        this_row  = df_input_csv.loc[index].copy() 
        to_transcribe_list.append(this_row)

df_to_transcribe = pd.DataFrame(to_transcribe_list).fillna('none')
df_to_transcribe["ERROR"] = "none"
df_to_transcribe["MyOcrText"] = "No OCR text"

# Necessary because by copying rows to give each url a seperate row, we have also copied indexes
# We want each row to have its own index - so reset_index
df_to_transcribe.reset_index(drop=True, inplace=True)

"""
output_path = f"{output_folder}/NY_transcribed_{time_stamp}-1062"
save_dataframe_to_csv(df_to_save=df_to_transcribe, output_path=output_path)
exit()
"""


# These are the columns that ChatGPT will try to fill from the OCR
ocr_column_names = [ 
        ("DarCollector","Collector Name"), 
        ("CollectionTeam","Collection Team"), 
        ("CollectionNumberPrefix","Collection Number Prefix"), 
        ("CollectionNumber","Collection Number"), 
        ("CollectionNumberSuffix","Collection Number Suffix"), 
        ("CollectionNumberText","Collection Number Verbatim"), 
        ("ColDateVisitedFrom","Collection Date From"), 
        ("ColDateVisitedTo","Collection Date To"), 
        ("ColVerbatimDate","Collection Date Verbatim"), 
        ("DarCollectionNotes","Collection Notes"), 
        ("DarContinent","Continent"), 
        ("DarCountry","Country"), 
        ("DarStateProvince","Province"), 
        ("DarCounty","County"),
        ("DarLocality","Locality Description"), 
        ("Township_tab","Township_tab"), 
        ("Range_tab","Range_tab"), 
        ("Section_tab", "Section_tab"),
        ("DarMinimumElevationMeters","Minimum Elevation in Meters"), 
        ("DarMaximumElevationMeters","Maximum Elevation in Meters"), 
        ("MinimumElevationFeet","Minimum Elevation in Feet"), 
        ("MaximumElevationFeet","Maximum Elevation in Feet"),
        ("DarLatitudeDecimal","Latitude Decimal"), 
        ("DarLongitudeDecimal","Longitude Decimal"), 
        ("LatitudeDMS","Latitude (Degrees Minutes Seconds)"), 
        ("LongitudeDMS","Longitude (Degrees Minutes Seconds)"), 
        ("DarGeodeticDatum","Geodetic Datum"), 
        ("DarGeorefMethod","Geo Reference Method"), 
        ("DarCoordinateUncertaintyInMeter","Coordinate Uncertainty in Meters"), 
        ("ColLocationNotes","Collection Location Notes"),
        ("FeaCultivated? (Y/N)","Cultivated"), 
        ("FeaPlantFungDescription","Plant Description"), 
        ("FeaFrequency","Plant Frequency"), 
        ("HabHabitat","Plant Habitat"), 
        ("HabVegetation","Plant Forest Type"), 
        ("HabSubstrate","Plant Substrate"), 
        ("SpeOtherSpecimenNumbers_tab","SpeOtherSpecimenNumbers_tab"), 
        ("MyOcrText", "OCR Text")]


df_column_names = []          # To make the DataFrame with
prompt_key_names = []         # To use in the prompt for ChatGPT
empty_output_dict = dict([])  # Useful when you have an error but still need to return a whole DataFrame row
for df_name, prompt_name in ocr_column_names:
    df_column_names.append(df_name)     
    prompt_key_names.append(prompt_name)   
    empty_output_dict[df_name] = "none"

keys_concatenated = ", ".join(prompt_key_names) # For the prompt

# Should check that the columns in df_column_names are in df_to_transcribe
# If they are not, no error occures, but the OCR output will be not copied into the missing columns
# This is silent and bad
df_to_transcribe_keys = list(df_to_transcribe.keys())
if set(df_column_names) <= set(df_to_transcribe_keys):
    print("df_column_names is a subset of df_to_transcribe_keys - GOOD")
else:
    print("ERROR: df_column_names is NOT a subset of df_to_transcribe_keys - BAD")
    exit()


# New - got it to estimate Lat and Lng from location
prompt = (
    f"Read this herbarium sheet and extract all the text you can"
    f"The herbarium sheet may sometimes use Spanish, French or German"
    f"Go through the text you have extracted and return data in JSON format with {keys_concatenated} as keys"
    f"Use exactly {keys_concatenated} as keys"
    
    f"Use the English spelling for Country e.g. 'Brazil' not 'Brasil'"
    
    f"Return the text you have extracted in the field 'OCR Text'"
    
    f"'Collection Team' should contain other people involved in collecting the specimen"
    
    f"The 'Collection Date To' and 'Collection Date From' should have the format YYYY-MM-DD"
    f"If there is only one date then fill in 'Collection Date To' and 'Collection Date From' with the same value"
    
    f"Infer the Continent field from the Country e.g. If the Country is 'Belize' then the Continent field is 'Central America', if the Country is 'Costa Rica' the the Continent field is 'South America'"
    f"If no Country is mentioned then infer it from the Continent, Province, County and Locality Description"
    
    f"If Latitude and Longitude are not mentioned in the text then infer them from the Country, Province, County and Locality Description"
    f"Put the infered Latitude and Longitude in the 'Latitude (Degrees Minutes Seconds)' 'Longitude (Degrees Minutes Seconds)' 'Latitude Decimal' and 'Longitude Decimal' fields"
    f"If Latitude and Longitude have been inferred fill in the 'Coordinate Uncertainty In Meters' with an estimate of the accuracy and 'Geo Reference Method' with 'Estimated from locality description'"
    
    f"If a single elevation or altitude is mentioned fill in both the 'Minimum Elevation (Meters)' and 'Maximum Elevation (Meters)' with the same value"
    f"If there is elevation information in Meters then do a conversion to feet and store the conversion in 'Minimum Elevation (Feet)' and 'Maximum Elevation (Feet)'"
    
    f"For 'Plant Frequency' field look for words like abundant, cccasional, common, frequent or rare"
    f"For 'Plant Habitat' field put what type of environment the plant grows in e.g. forest, scrub, rocky hillside"
    f"For 'Plant Substrate' field look for what the plant grows on e.g. on rotting log, on damp rock, on bark"
    f"For 'Plant Description' field put a description of the plant e.g. Shrub 4m high, flowers white, fruit orange"
    
    f"If a plant is cultivated put 'Yes' in the 'Cultivated' field, otherwise put 'No'"
    
    f"If you find 'INB' followed by a number add INB and the number to SpeOtherSpecimenNumbers_tab"
    
    f"If you can not find a value for a key return value 'none'"
)


headers = get_headers(my_api_key)

source_type="url" # "url" or "local"
print("####################################### START OUTPUT ######################################")
for index, row in df_to_transcribe.iloc[0:].iterrows():  

    count = index + 1
    
    image_path = row["DarImageURL"]
    
    
    if source_type != "url":
        # JPGs in local folder
        filename = image_path.split("/")[-1]
        image_path = Path(f"{input_jpg_folder}/{filename}")
        if image_path.is_file() == False:
            print(f"File {image_path} does not exist")
            exit()
            
    print(f"\n########################## OCR OUTPUT {image_path} ##########################")
    print(f"count: {count}")
    
    payload = make_payload(model=MODEL, prompt=prompt, source_type=source_type, image_path=image_path, num_tokens=4096)

    num_tries = 3
    for i in range(num_tries):
        ocr_output = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        response_code = ocr_output.status_code
        if response_code != 200:
            # NOT 200
            print(f"======= 200 not returned {response_code}. Trying request again number: {i} ===========================")
            time.sleep(0.5)
        else:
            # YES 200
            json_returned = clean_up_ocr_output_json_content(ocr_output)
            json_valid = is_json(json_returned)
            if json_valid == False:
                # INVALID JSON
                print(f"======= Returned JSON content not valid. Trying request again number: {i} ===========================")
                print(f"INVALID JSON content****{json_returned}****")
            else:
                # VALID JSON
                # Have to check that the returned JSON keys are correct 
                # Sometimes ChatGPT just doesn't do as its told and changes the key names!
                if are_keys_valid(json_returned, prompt_key_names) == False:
                    # INVALID KEYS
                    print(f"======= Returned JSON contains invalid keys. Trying request again number: {i} ===========================")
                else:
                    # VALID KEYS
                    break
                
    ###### eo try requests three times

    # OK - we've tried three time to get
    # 1. 200 returned AND
    # 2. valid JSON returned AND
    # 3. valid key names
    # Now we have to create a valid Dict line for the spreadsheet
    error_message = "OK"
    dict_returned = dict()
    if response_code != 200:
        # NOT 200
        # Make a Dict line from the standard empty Dict and 
        # put the whole of the returned message in the OcrText field
        print("RAW ocr_output ****", ocr_output.json(),"****")                   
        dict_returned = eval(str(empty_output_dict))
        dict_returned['MyOcrText'] = str(ocr_output.json())
        error_message = "200 NOT RETURNED FROM GPT"
        print(error_message)
    else:
        # YES 200
        print(f"content****{json_returned}****")
    
        if is_json(json_returned):
            # VALID JSON
            
            # Have to deal with the possibility of invalid keys returned in the valid JSON
            if are_keys_valid(json_returned, prompt_key_names):
                # VALID KEYS
                # Now change all the key names from the human readable used in the prompt to 
                # DataFrame output names to match the NY spreadsheet
                
                dict_returned = eval(json_returned) # JSON -> Dict
                
                for df_name, prompt_name in ocr_column_names:
                    dict_returned[df_name] = dict_returned.pop(prompt_name)
            else:
                # INVALID KEYS
                dict_returned = eval(str(empty_output_dict))
                dict_returned['MyOcrText'] = str(json_returned)                  
                error_message = "INVALID JSON KEYS RETURNED FROM GPT"
                print(error_message)
        else:
            # INVALID JSON
            # Make a Dict line from the standard empty Dict and 
            # just put the invalid JSON in the OcrText field
            dict_returned = eval(str(empty_output_dict))
            dict_returned['MyOcrText'] = str(json_returned)
            error_message = "JSON NOT RETURNED FROM GPT"
            print(error_message)
        
    ###### EO dealing with various types of returned code ######
    
    dict_returned["ERROR"] = str(error_message)  # Insert error message into output
    
    df_to_transcribe.loc[index, dict_returned.keys()] = dict_returned.values() # <<<<<<<<<<<<<<<<< 
    
    if count % batch_size == 0:
        print(f"WRITING BATCH:{count}")
        output_path = f"{output_folder}/{project_name}_{time_stamp}-{count:04}"
        save_dataframe_to_csv(df_to_save=df_to_transcribe, output_path=output_path)

   

#################################### eo for loop ####################################

# For safe measure and during testing where batches are not %batch_size
print(f"WRITING BATCH:{count}")
output_path = f"{output_folder}/{project_name}_{time_stamp}-{count:04}"
save_dataframe_to_csv(df_to_save=df_to_transcribe, output_path=output_path)

print("####################################### END OUTPUT ######################################")
  

  


