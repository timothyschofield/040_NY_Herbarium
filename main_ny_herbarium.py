"""
File : main_ny_herbarium.py

Author: Tim Schofield
Date: 05 June 2024

"""

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

# MODEL = "gpt-4-turbo"     # Context window of 128k max_tokens 4096
MODEL = "gpt-4o"            # Context window of 128k max_tokens 4096

load_dotenv()

try:
  my_api_key = os.environ['OPENAI_API_KEY']          
  client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()

"""

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

DarCollectionNotes	

DarContinent	DarCountry	DarStateProvince	DarCounty	(ALL WITH AUTHORITY FILE)
DarLocality
    e.g. 
    Lake Mgardok, Babeldaob Island OR 
    
    3rd pool east of road, Duval Creek, 7 mi. 
    north of Armidale, in c. 4" of water, mud bottom OR
    
    47 km N of Daly River Police Station on road to Darwin.

e.g. 1
Yaundé, Urwaldgebiet - was all that was mentoned
but the following was recorded
Africa	Cameroon	Centre		

e.g. 2
Gabon, 8 km ENE of Bellevue. - was recoded


Township_tab Range_tab	Section_tab	 (NO IDEA IGNORE)

DarMinimumElevationMeters	(when a single altitude is given, copy it to both max and min, and do the maths for meter/feet conversion)
DarMaximumElevationMeters	
MinimumElevationFeet	
MaximumElevationFeet	

DarLatitudeDecimal	DarLongitudeDecimal	 (If the Lat and Lng given in decimal, make a conversion and vica versa)
LatitudeDMS	LongitudeDMS	

DarGeodeticDatum (e.g. WGS84 The World Geodetic System 1984 - a satalite navigation system OR NAD83 North American Datum 1983)
DarGeorefMethod	(e.g. GPS)


DarCoordinateUncertaintyInMeter	e.g. - vary raire 1000 ro 10000

ColLocationNotes	e.g. [Mexico & Central America] OR [Pacifica] OR [Australia] etc.


FeaCultivated? (Y/N)	
FeaPlantFungDescription	
FeaFrequency	


HabHabitat	        e.g. on grassy field OR lateau, succulent thicket OR Végétation très basse, ericoide arbustive ou herbacée
HabVegetation	
HabSubstrate	

SpeOtherSpecimenNumbers_tab	


OcrText

"""


P


























