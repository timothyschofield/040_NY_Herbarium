import requests
from pathlib import Path
import pandas as pd


data = {"Name": ["T′m", "Nick", "K′ish", "Jack"],
        "Month": ["January", "Ma′ch", "July", "August"],
        "Place": ["Lan′aster", "Ca′d′n", "London", "P′ris"]
        }

df = pd.DataFrame(data)

print(df)
print("------")

# Counts the number of instances of the string in the df
sum_cols = 0
for col in df:
    sum_cols+= df[col].str.count("′").sum()
print(sum_cols)

# \u2032 ′ 8242
print(ord("′")) # 8242

print(chr(8242)) # ′
print("------")

# Replaces all instances of one string in a df with another
df.replace({"′": "'"}, regex=True, inplace=True)


print(df)
print("------")



exit()



input_folder = "ny_herbarium_input"
input_file = "NY_specimens_to_transcribe.csv"
input_path = Path(f"{input_folder}/{input_file}")
df_input_csv = pd.read_csv(input_path)

input_url_list = df_input_csv["DarImageURL"]
# print(input_url_list)

output_folder = "jpg_folder_input"
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












