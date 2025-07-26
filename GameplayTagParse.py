import csv

AmtofTags = 0

iniFileDir = "./Unparsed/DefaultGameplayTags.ini"
csvFileDir = "./Parsed/ItemTags.csv"



TestList = []
TagList = []

with open(iniFileDir,"r", encoding="utf-8") as file:
    for line in file:
        SLine = line.strip("\n")
        SplitLine = SLine.split('"')
        
        if (SplitLine[0] == "+GameplayTagList=(Tag="):  
            TagList.append(SplitLine[1]) 


Items = []
ItemList = []




for tag in TagList:
    tagGroup = tag.split(".")
    if(tagGroup[0] == "Inventory" and tagGroup[1] == "Items" and len(tagGroup) > 4):
        
        tagGroup.remove("Inventory")
        AbvTag = ".".join(tagGroup)
        ItemType = tagGroup[0]
        ItemCategory = tagGroup[1]
        ItemSubCategory = tagGroup[2]
        ItemName = tagGroup[3]
        if (len(tagGroup) > 4):
            ItemName = ItemName + " " + tagGroup[4]

            TempAbv = AbvTag.split(".")
            TempAbv.pop(4)
            TempAbv.pop(3)
            AbvTag = ".".join(TempAbv)

        else:
            TempAbv = AbvTag.split(".")
            TempAbv.pop(3)
            AbvTag = ".".join(TempAbv)

        ItemFName = ItemName.replace(" ","_")
        AmtofTags += 1
        if ItemFName == "Elevator_Room":
            ItemFName = ItemFName + "_Key"
        if ItemFName == "General_Bunker_Key":
            ItemFName = "Bunker_General_Key"
            ItemName = "Bunker General Key"

        if (ItemCategory == "Keys" and ItemFName != "Bunker_General_Key"):
            ItemFName = ItemSubCategory + "_" + ItemFName
            ItemName = ItemSubCategory + " " + ItemName


        Items.append({
            "FullTag" : tag,
            "ShortTag": AbvTag,
            "Type" : ItemType,
            "Category" : ItemCategory,
            "SubCategory": ItemSubCategory,
            "Name" : ItemName,
            "FName" : ItemFName
        })
    elif (tagGroup[0] == "Inventory" and tagGroup[1] == "Items" and len(tagGroup) == 4):
        if (tagGroup[2] == "Medical" or tagGroup[2] == "Currency" or tagGroup[2] == "Quest"):
            if (tagGroup[3] != "Defense"):
                print(f"{tag} -- {len(tagGroup)}") 
                ItemType = tagGroup[0]
                ItemCategory = tagGroup[1]
                ItemSubCategory = tagGroup[2]
                ItemName = tagGroup[3]
                tagGroup.remove("Inventory")
                AbvTag = ".".join(tagGroup)
                ItemFName = ItemName.replace(" ","_")
                AmtofTags += 1
                Items.append({
                    "FullTag" : tag,
                    "ShortTag": AbvTag,
                    "Type" : ItemType,
                    "Category" : ItemCategory,
                    "SubCategory": ItemSubCategory,
                    "Name" : ItemName,
                    "FName" : ItemFName
                })
         

for Item in Items:
    if Item['Category'] == 'Ammunition':
        FNamesplit = Item['FName'].split('_')
        if(len(FNamesplit) < 2):
            Items.remove(Item)
            AmtofTags -= 1

with open (csvFileDir, 'w', newline='') as csvFile:
    fieldnames = ['FName','Name','FullTag','ShortTag','Type','Category','SubCategory']
    itemWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    
    itemWriter.writeheader()
    for x in Items:
        itemWriter.writerow(x)
    



print("Script Completed!")
print("Processed "+str(AmtofTags)+" Item Tags to CSV")