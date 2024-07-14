import requests
from pathlib import Path
import pandas as pd

"""
try:
  print(x)
except NameError:
  print("Variable x is not defined")
except:
  print("Something else went wrong") 

"""

def make_UPDATE_sql_line(row):
    eol = f"\n"
    
    sql = f"UPDATE specimenCards SET "
    
    val = row["DarCollector"]
    if type(val) != str: val = ""
    new_str = f"darCollector = '{val}', AI_darCollector = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionTeam"]
    if type(val) != str: val = ""
    new_str = f"collectionTeam = '{val}', AI_collectionTeam = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionNumberPrefix"]
    if type(val) != str: val = ""   
    new_str = f"collectionNumberPreffix = '{val}', AI_collectionNumberPrefix = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionNumber"]
    if type(val) != str: val = ""
    new_str = f"collectionNumber = '{val}', AI_collectionNumber = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionNumberSuffix"]
    if type(val) != str: val = ""
    new_str = f"collectionNumberSuffix = '{val}', AI_collectionNumberSuffix = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["CollectionNumberText"]
    if type(val) != str: val = ""
    new_str = f"collectionNumberText = '{val}', AI_collectionNumberText = '{val}',{eol}"
    sql = f"{sql}{new_str}"

    val = row["ColDateVisitedFrom"]
    if type(val) != str: val = ""
    date_list = val.split("-")
    if len(date_list) != 3:
        year = ""
        month = ""
        day = ""
    else:
        year = str(date_list[0])
        month =  str(date_list[1])
        day =  str(date_list[2])
        
    new_str = f"collectionDD = '{day}', collectionMM = '{month}', collectionYYYY = '{year}', AI_collectionDD = '{day}', AI_collectionMM = '{month}', AI_collectionYYYY = '{year}',{eol}"
    sql = f"{sql}{new_str}"
    
    val = row["ColDateVisitedTo"]
    if type(val) != str: val = ""
    date_list = val.split("-")
    if len(date_list) != 3:
        year = ""
        month = ""
        day = ""
    else:
        year = str(date_list[0])
        month =  str(date_list[1])
        day =  str(date_list[2])
        
    new_str = f"collectionDD2 = '{day}', collectionMM2 = '{month}', collectionYYYY2 = '{year}', AI_collectionDD2 = '{day}', AI_collectionMM2 = '{month}', AI_collectionYYYY2 = '{year}',{eol}"
    sql = f"{sql}{new_str}"     
      
    val = row["ColVerbatimDate"]
    if type(val) != str: val = ""
    new_str = f"colVerbatimDate = '{val}', AI_colVerbatimDate = '{val}' {eol}" # comma replaced by space
    sql = f"{sql}{new_str}" 
      
    # NO FINAL COMMA BEFORE WHERE
    ##################
   
    # INTEGER
    val = row["DarCatalogNumber"]
    #if type(val) != str: val = ""
    new_str = f"WHERE darCatalogNumber = '{val}';"
    
    #new_str = f"WHERE darCatalogNumber = '{val}' AND transcriptionStateId = 0;" # from Max
    
    sql = f"{sql}{new_str}"

    return sql




data = {"Name": ["T′m", "00°38", "K′ish", "Jack"],
        "Month": ["January", "Ma′ch", "July", "August"],
        "Place": ["Lan′aster", "Ca′d′n", "London", "P′ris"]
        }

df = pd.DataFrame(data)

print(df)

with open(f"test_from_linux.csv", encoding="utf-8", mode="w") as f:
  df.to_csv(f, index=False)



print("------")
exit()

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




