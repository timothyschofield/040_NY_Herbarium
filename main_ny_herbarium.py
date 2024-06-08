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

from helper_functions_ny_herbarium import encode_image, get_file_timestamp, is_json, create_and_save_dataframe, make_payload

import requests
import os
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime
import json

from url_ny_sweetgum_1000 import URL_PATH_LIST

MODEL = "gpt-4o"            # Context window of 128k max_tokens 4096

load_dotenv()

try:
  my_api_key = os.environ['OPENAI_API_KEY']          
  client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()

# These are the columns that ChatGPT will try to fill from the OCR
# Other columns will include URL, ERROR, STOP REASON
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
        ("DarMinimumElevationMeters","Minimum Elevation (Meters)"), 
        ("DarMaximumElevationMeters","Maximum Elevation (Meters)"), 
        ("MinimumElevationFeet","Minimum Elevation (Feet)"), 
        ("MaximumElevationFeet","Maximum Elevation (Feet)"),
        ("DarLatitudeDecimal","Latitude Decimal"), 
        ("DarLongitudeDecimal","Longitude Decimal"), 
        ("LatitudeDMS","Latitude (Degrees Minutes Seconds)"), 
        ("LongitudeDMS","Longitude (Degrees Minutes Seconds)"), 
        ("DarGeodeticDatum","Geodetic Datum"), 
        ("DarGeorefMethod","Geo Reference Method"), 
        ("DarCoordinateUncertaintyInMeter","Coordinate Uncertainty In Meters"), 
        ("ColLocationNotes","Collection Location Notes"),
        ("FeaCultivated? (Y/N)","Cultivated (Yes or No)"), 
        ("FeaPlantFungDescription","Plant Description"), 
        ("FeaFrequency","Plant Frequency"), 
        ("HabHabitat","Plant Habitat"), 
        ("HabVegetation","Plant Forest Type"), 
        ("HabSubstrate","Plant Substrate"), 
        ("SpeOtherSpecimenNumbers_tab","SpeOtherSpecimenNumbers_tab"), 
        ("OcrText", "OCR Text")]

batch_size = 20 # saves every
time_stamp = get_file_timestamp()

input_folder = "ny_hebarium_input"
output_folder = "ny_hebarium_output"
project_name = "NY"

source_type = "url" # url or offline
if source_type == "url":
  image_path_list = URL_PATH_LIST
else:
  image_folder = Path(f"{input_folder}/")
  image_path_list = list(image_folder.glob("*.jpg"))

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {my_api_key}"
}

output_list = []
count = 0
print("####################################### START OUTPUT ######################################")
try:
  
  for image_path in image_path_list[:5]:
    pass










except openai.APIError as e:
  #Handle API error here, e.g. retry or log
  print(f"TIM: OpenAI API returned an API Error: {e}")
  pass

except openai.APIConnectionError as e:
  #Handle connection error here
  print(f"TIM: Failed to connect to OpenAI API: {e}")
  pass

except openai.RateLimitError as e:
  #Handle rate limit error (we recommend using exponential backoff)
  print(f"TIM: OpenAI API request exceeded rate limit: {e}")
  pass
  


