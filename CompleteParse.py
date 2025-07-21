import pandas as pd
import os

csvFileDir = "./Parsed/"
mainOutputFile = "./Parsed/Complete.xlsx"


with pd.ExcelWriter(mainOutputFile, engine="xlsxwriter") as writer:
    for fname in os.listdir(csvFileDir):
        if not fname.lower().endswith(".csv"):
            continue
        sheet = os.path.splitext(fname)[0][:31]
        df = pd.read_csv(os.path.join(csvFileDir,fname))
        df.to_excel(writer, sheet_name=sheet, index=False)