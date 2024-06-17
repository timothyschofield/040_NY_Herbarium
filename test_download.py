import requests
from pathlib import Path
import pandas as pd

input_folder = "ny_herbarium_input"
input_file = "NY_specimens_to_transcribe.csv"
input_path = Path(f"{input_folder}/{input_file}")
df_input_csv = pd.read_csv(input_path)

input_url_list = df_input_csv["DarImageURL"]
# print(input_url_list)

output_folder = "jpg_folder"
count = 1
for url in input_url_list:

    url_list = url.split("/")
    filename = url_list[-1]
    print(f"{count}: {filename}")
    count = count + 1
    
    res = requests.get(url)

    # print(type(res)) # requests.models.Response
    # print(res.url)
    # print(res.status_code)

    output_path = Path(f"{output_folder}/{filename}")

    if res.status_code == 200:
        with open(output_path,'wb') as f:
            print(f"Writing: {output_path}")
            f.write(res.content)
    else:
        print("200 not returned")

   











