import pandas as pd
import glob

for f in glob.glob("seeds/*.csv"):
    df = pd.read_csv(f, encoding="utf-8-sig")
    df.to_csv(f, index=False, encoding="utf-8")
    print("Cleaned BOM for:", f)
