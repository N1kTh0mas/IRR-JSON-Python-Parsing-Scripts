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

NameAdjustments = {
    "545x39_7N22" : "545x39_BP" ,
    "545x39_7N6" : "545x39_PS",
    "57x28_SS197LF" : "57x28_SS198LF",
    "MarkedCoin" : "Marked_Coin",
    "BT_Quick_Detach_Unigrip" : "BT_QuickDetach_Unigrip",
    "AK_CAF_WASR_Wooden_Handguard" :"CAF_WASR_Wooden_Handguard",
    "HK_MP5_9x19_30rnd_magazine" : "HK_MP5_9x19_30rnd",
    "HK_MP5_End-Cap_Buttstock" : "MP5_End-Cap_Buttstock",
    "HK_MP5_Polymer_Handguard" : "MP5_Polymer_Handguard",
    "Magpul_MOE_RVG_Foregrip" : "Magpul_MOE_RVG_Forerip",
    "SRS-A2" : "SRS_A2",
    "DT338_Suppressor" : "DT_338_Suppressor",
    "DT338_Muzzle_Brake" : "DT_338_Muzzle_Brake",
    "M2_Agency_Arms_18x5_Inch_12ga_7-shell" : "M2_Agency_Arms_18x5_inch_12ga_7-shell",
    "M2_Agency_Arms_21_Inch_12ga_8-shell" : "M2_Agency_Arms_21_inch_12ga_8-shell",
    "M2_14_Inch_Tactical_Barrel" : "M2_14_inch_Tactical_Barrel",
    "M2_18x5_Inch_Field_Barrel" : "M2_18x5_inch_Field_Barrel",
    "M2_18x5_Inch_Tactical_Barrel" : "M2_18x5_inch_Tactical_Barrel",
    "M2_21_Inch_Field_Barrel" : "M2_21_inch_Field_Barrel",
    "JTAC_V1_Armored_Rig" : "JTAC_V1_Vest",
    "AVS_Rifleman_V4_Armored_Rig" : "AVS_Rifleman_V4_Vest",
    "AVS_PL_SGT_Armored_Rig" : "AVS_PL_SGT_Vest",
    "AVS_SL_Armored_Rig" : "AVS_SL_Vest",
    "MP5K" : "MP5k",
    "Simonov_SKS" : "SKS",
    "762x39_57-N-231" : "762x39_PS",
    "762x39_7N23" : "762x39_BP",
    "QBZ-97" : "Norinco_QBZ-97",
    "AR-15_Colt_A2_Stanag_556x45_20Rnd" : "AR-15_Colt_A2_Stanag_556x45_20rnd",
    "Zenitco_DTK-1_545x39_Muzzle_Brake" : "Zenitco_DTK-1_545x39",
    "Jmac_Customs_RRD-4C_545x39_Muzzle_Brake" : "Jmac_Customs_RRD-4C_545x39",
    "PBS-4_545x39_Suppressor" : "PBS-4_545x39Suppressor",
    "Z111_762x39_30Rnd" : "Z111_762x39_30rnd",
    "AK_762x39_Star_20Rnd" : "AK_762x39_20rnd",
    "AK_545x39_Polymer_45Rnd" : "AK_545x39_45rnd",
    "AK_Molot_556x45_45Rnd" : "AK_556x45_45rnd",
    "MP5_KCI_9x19_20Rnd" : "HK_MP5_9x19_20rnd",
    "MP5_X-Products_X-5_9x19_50Rnd" : "HK_MP5_9x19_50rnd",
    "PP-19_F5MFG_9mm_50Rnd" : "PP-19_9x19_50rnd",
    "LBT_Breacher_V1_Armored_Rig" : "LBT_Breacher_V1",
    "MICH_2000_Helmet" : "MICH_2000",
    "GoldenBangle" : "Golden_Bangle",
    "FilmCase" : "Film_Case",
    "SilverPearls" : "Silver_Pearls",
    "GoldenRing" : "Golden_Ring",
    "GasCan" : "Gas_Can",
    "PlasticWireSpool" : "Plastic_Wire_Spool",
    "OldChemicalBottle" : "Old_Chemical_Bottle",
    "RebarCutter" : "Rebar_Cutter",
    "HDMICable" : "HDMI_Cable",
    "PuzzleCube" : "Puzzle_Cube",
    "QSZ-92_9x19_15Rnd" : "QSZ-92_9x19_15rnd",
    "AK-12_Pistolgrip_Polymer" : "AK-12_Pistol_Grip",
    "AK-12_Handguard_Polymer" : "AK-12_Polymer_Handguard",
    "AK-12_545x39_Polymer_30Rnd" : "AK12_545x39_30rnd",
    "Elcan_SpecterDR_1x-4x_Scope" : "Elcan_SpecterDR_1x/4x_Scope",
    "Weather_Device" : "Kestrel_5700X",
    "Bunker_Large_Safe_key" : "Bunker_Large_Safe_Key",
    "Quarry_Large_Safe_key" : "Quarry_Large_Safe_Key",
    "Quarry_Compact_Safe_key" : "Quarry_Compact_Safe_Key",
    "Bunker_General_key" : "Bunker_General_Key"

}

IgnoreList = [
    "KeyCard1",
    "Recording_Backpack"
]


DataItem = data[0]["Rows"]
VendorItems = []
   
for x in data[0]["Rows"]:
    Id = NameAdjustments.get(x,x)
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
        "ItemID" : Id,
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

for item in VendorItems:
    if item['ItemID'] in IgnoreList:
        VendorItems.remove(item)


with open (csvFileDir, 'w', newline='') as csvFile:
    fieldnames = ['ItemID','ItemName','DefaultStock','MaxStock','StockRate','Faction','Tier','Qty','CMPrice','BMPrice']
    itemWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    
    itemWriter.writeheader()
    for i in VendorItems:
        itemWriter.writerow(i)

print("Script Complete")