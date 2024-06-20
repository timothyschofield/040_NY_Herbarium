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

_data = "sh′56jkAS"

data = list((c.encode("utf-8") for c in _data))
print(data)

data = _data.encode("utf-8")
print(data)


exit()

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




