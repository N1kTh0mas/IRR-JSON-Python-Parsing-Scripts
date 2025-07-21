import csv
import json


jsonFileDir = "./Unparsed/DT_Vendor.json"
csvFileDir = "./Parsed/VendorDT.csv"


with open(jsonFileDir, 'r') as jsonFile:
    data = json.load(jsonFile)

factionDict = {
    "Mission.Faction.BLUEFOR" : "UICS",
    "Mission.Faction.GREYFOR" : "IGC",
    "Mission.Faction.OPFOR" : "VLF"
}


DataItem = data[0]["Rows"]
VendorItems = []
   
for x in data[0]["Rows"]:
    ItemName = x
    DefaultStock = DataItem[x]['DefaultStockCount']
    MaxStock = DataItem[x]['MaxStockCount']
    StockRate = DataItem[x]['RestockRate']
    Faction = factionDict.get(DataItem[x]['FactionAvailability']['FactionTag']['TagName'],"None")
    
    Rarity = DataItem[x]['ItemRarityTag']['TagName']
    Tier = Rarity[len(Rarity)-1]

    Qty = DataItem[x]['ItemData']['Count']
    CMPrice = DataItem[x]['MarketAvailability']['DefaultMarketPrice']
    BMPrice = DataItem[x]['MarketAvailability']['BlackMarketPrice']

    VendorItems.append({
        "ItemName" : ItemName,
        "DefaultStock" : DefaultStock,
        "MaxStock" : MaxStock,
        "StockRate" : StockRate,
        "Faction" : Faction,
        "Tier" : Tier,
        "Qty" : Qty,
        "CMPrice" : CMPrice,
        "BMPrice" : BMPrice
    })


with open (csvFileDir, 'w', newline='') as csvFile:
    fieldnames = ['ItemName','DefaultStock','MaxStock','StockRate','Faction','Tier','Qty','CMPrice','BMPrice']
    itemWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    
    itemWriter.writeheader()
    for i in VendorItems:
        itemWriter.writerow(i)

print("Script Complete")