import csv
import json
import os

jsonFolderDir = "./Unparsed/Containers/"
csvSpawnFileDir = "./Parsed/ContainerSpawn.csv"
csvPropertiesFileDir = "./Parsed/ContainerProperties.csv"

jsonFileList = []

for jsonFile in os.listdir(jsonFolderDir):
    jsonCheck = jsonFile.split(".")

    if (jsonCheck[len(jsonCheck)-1] == "json"):
        jsonFileList.append(jsonFile)
PropertyList = []
OverrideList = []
SpawnWeightList = []


for file in jsonFileList:
    jsonDir = jsonFolderDir + file
    #print(file)

    with open(jsonDir, 'r') as f:
        data = json.load(f)


    
    
    filesplit = file.split(".")
    TempName = filesplit[0].split("_",2)
    
    ContainerName = TempName[2].replace("_"," ")
    print(ContainerName)
    

    DataItem = data[0]['Properties']['DefaultItemsContainers']
    for line in DataItem:
        WeaponMags = line['bTryAddWeaponMags']
        RandomItems = line['bAddRandomItems']
        RandomSpawnChance = line['RandomItemSpawnChances']
        MinItemAmt = line['RandomItemParameters']['MinItemsToAdd']
        MaxItemAmt = line['RandomItemParameters']['MaxItemsToAdd']
        MinItemValue = line['RandomItemParameters']['MinValue']
        MaxItemValue = line['RandomItemParameters']['MaxValue']
        AddSameItem = line['RandomItemParameters']['bCanAddSameItem']
        ForceRarity = line['RandomItemParameters']['bForceMatchRarity']
        ForceVital = line['RandomItemParameters']['bForceVitalParts']
        SupportFactionCount = len(line['RandomItemParameters']['SupportedFactions'])
        AttachmentMinDepth = line['RandomItemParameters']['AttachmentMinDepth']
        AttachmentMaxDepth = line['RandomItemParameters']['AttachmentMaxDepth']

        PropertyList.append({
            "Container" : ContainerName,
            "WeaponMags": WeaponMags,
            "RandomItems": RandomItems,
            "RandomSpawnChance" : RandomSpawnChance,
            "MinItemAmt" : MinItemAmt,
            "MaxItemAmt" : MaxItemAmt,
            "MinItemValue" : MinItemValue,
            "MaxItemValue" : MaxItemValue,
            "AddSameItem" : AddSameItem,
            "ForceRarity" : ForceRarity,
            "ForceVital" : ForceVital,
            "SupportFactionCount" : SupportFactionCount,
            "AttachmentMinDepth" : AttachmentMinDepth,
            "AttachmentMaxDepth" : AttachmentMaxDepth
        })

        for override in line['RandomItemParameters']['ItemCountOverrides']:
            
            OR_Tag = override['Key']['TagName']
            OR_Min = override['Value']['X']
            OR_Max = override['Value']['Y']

            OverrideList.append({
                "Container" : ContainerName,
                "Tag" : OR_Tag,
                "MinAmt" : OR_Min,
                "MaxAmt" : OR_Max
            })
    
    DataItem = data[0]['Properties']['DefaultItemsContainers']

    for item in DataItem:
        for element in item['RandomItemParameters']['ItemSpawnChances']:
            TempTag = element['Key']['TagName']
            TagSplit = TempTag.split('.')
            TagSplit.remove("Inventory")
            Tag = ".".join(TagSplit)

            Weight = element['Value']
            
            SpawnWeightList.append({
                "Container" : ContainerName,
                "Type" : "Item",
                "Tag":  Tag,
                "Weight" : Weight
            })
        for element in item['RandomItemParameters']['RarityChanceDrop']:
            TempTag = element['Key']['TagName']
            Tag = TempTag[len(TempTag)-1]

            Weight = element['Value']
            SpawnWeightList.append({
                "Container" : ContainerName,
                "Type" : "Rarity",
                "Tag":  Tag,
                "Weight" : Weight
            })



with open (csvPropertiesFileDir, 'w', newline='') as csvFile:
    fieldnames = ['Container','WeaponMags', 'RandomItems', 'RandomSpawnChance', 'MinItemAmt', 'MaxItemAmt', 'MinItemValue', 'MaxItemValue', 'AddSameItem', 'ForceRarity', 'ForceVital', 'SupportFactionCount', 'AttachmentMinDepth', 'AttachmentMaxDepth']
    itemWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    
    itemWriter.writeheader()
    for i in PropertyList:
        itemWriter.writerow(i)

    itemWriter.writerow({})
    fieldnames = ['Container','Tag', 'MinAmt', 'MaxAmt']
    orWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)

    orWriter.writeheader()
    for y in OverrideList:
        orWriter.writerow(y)


with open (csvSpawnFileDir, 'w', newline='') as csvFile:
    fieldnames = ['Container','Type', 'Tag', 'Weight']
    itemWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    
    itemWriter.writeheader()
    for i in SpawnWeightList:
        itemWriter.writerow(i)

print('Script Complete')




