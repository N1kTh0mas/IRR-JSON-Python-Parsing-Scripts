import csv
import json


jsonFileDir = "./Unparsed/DA_VendorSettings.json"
csvFileDir = "./Parsed/VendorSettings.csv"

with open(jsonFileDir, 'r') as jsonFile:
    data = json.load(jsonFile)

DataItem = data[0]["Properties"]['VendorSellMultiplierMap']


SettingsList = []

SettingsList.append({
        "Tag" : "Default",
        "Multiplier" : data[0]["Properties"]['VendorSellMultiplierDefault']
    })

for x in DataItem:
    Tag = x['Key']['TagName']
    Multiplier = x['Value']

    SettingsList.append({
        "Tag" : Tag,
        "Multiplier" : Multiplier
    })
    
with open (csvFileDir, 'w', newline='') as csvFile:
    fieldnames = ['Tag','Multiplier']
    itemWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    
    itemWriter.writeheader()
    for i in SettingsList:
        itemWriter.writerow(i)
    

print("Script Complete")