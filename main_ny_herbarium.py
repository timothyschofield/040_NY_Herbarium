"""
File : main_ny_herbarium.py

Author: Tim Schofield
Date: 05 June 2024

"""
import openai
from openai import OpenAI
from db import OPENAI_API_KEY

from url_ny_sweetgum_1000 import URL_PATH_LIST

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





































