import csv
import json
import os

AIFolderDir = "./Unparsed/AI/"
csvAISpawnFile = "./Parsed/NPCLoadoutSpawn.csv"
csvAIPropertiesFile = "./Parsed/NPCLoadoutProperties.csv"

jsonFileList = []

SlotLookup = {
    0 : "Rifle 1",
    1 : "Rifle 2",
    2 : "Pistol",
    3 : "Plate Carrier",
    4 : "Rig",
    5 : "Pockets",
    6 : "Backpack",
    7 : "Helmet"
}

for folder in os.listdir(AIFolderDir):
    for file in os.listdir(AIFolderDir+"/"+folder):
        jsonCheck = file.split(".")

        if (jsonCheck[len(jsonCheck)-1] == "json"):
            fileFullPath = f"{AIFolderDir}{folder}/{file}"

            jsonFileList.append(fileFullPath)
            print(folder + " : " + file)

PropertyList = []
OverrideList = []
SpawnWeightList = []

for filePath in jsonFileList:
    with open(filePath, 'r') as f:
        data = json.load(f)

    filesplit = filePath.split("/")
    filesplit = filesplit[len(filesplit)-1].split(".")

    TempName = filesplit[0].split("_",2)
    
    NPCName = TempName[2].replace("_"," ")
    #print(ContainerName)
    
    DataItem = data[0]['Properties']['DefaultItemsContainers']
    for line in DataItem:
        Slot = SlotLookup.get(line['ContainerIndex'],"Error")
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
            "NPCName" : NPCName,
            "Slot" : Slot,
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
                "NPCName" : NPCName,
                "Slot" : Slot,
                "Tag" : OR_Tag,
                "MinAmt" : OR_Min,
                "MaxAmt" : OR_Max
            })

    DataItem = data[0]['Properties']['DefaultItemsContainers']

    for item in DataItem:
        for element in item['RandomItemParameters']['ItemSpawnChances']:
            Slot = SlotLookup.get(line['ContainerIndex'],"Error")
            TempTag = element['Key']['TagName']
            TagSplit = TempTag.split('.')
            TagSplit.remove("Inventory")
            Tag = ".".join(TagSplit)

            Weight = element['Value']
            
            SpawnWeightList.append({
                "NPCName" : NPCName,
                "Slot" : Slot,
                "Type" : "Item",
                "Tag":  Tag,
                "Weight" : Weight
            })
        for element in item['RandomItemParameters']['RarityChanceDrop']:
            TempTag = element['Key']['TagName']
            Tag = TempTag[len(TempTag)-1]

            Weight = element['Value']
            SpawnWeightList.append({
                "NPCName" : NPCName,
                "Slot" : Slot,
                "Type" : "Rarity",
                "Tag":  Tag,
                "Weight" : Weight
            })




with open (csvAIPropertiesFile, 'w', newline='') as csvFile:
    fieldnames = ['NPCName','Slot','WeaponMags', 'RandomItems', 'RandomSpawnChance', 'MinItemAmt', 'MaxItemAmt', 'MinItemValue', 'MaxItemValue', 'AddSameItem', 'ForceRarity', 'ForceVital', 'SupportFactionCount', 'AttachmentMinDepth', 'AttachmentMaxDepth']
    itemWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    
    itemWriter.writeheader()
    for i in PropertyList:
        itemWriter.writerow(i)

    itemWriter.writerow({})
    fieldnames = ['NPCName','Slot','Tag', 'MinAmt', 'MaxAmt']
    orWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)

    orWriter.writeheader()
    for y in OverrideList:
        orWriter.writerow(y)


with open (csvAISpawnFile, 'w', newline='') as csvFile:
    fieldnames = ['NPCName','Slot','Type', 'Tag', 'Weight']
    itemWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    
    itemWriter.writeheader()
    for i in SpawnWeightList:
        itemWriter.writerow(i)

print('Script Complete')