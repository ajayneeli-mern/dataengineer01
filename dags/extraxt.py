import shutil
import os,re
import kagglehub
import pandas as pd

src = kagglehub.dataset_download("yapwh1208/supermarket-sales-data")
dst = "data/"   # your project folder
dst2 ="my_dbt/seeds/"

shutil.copytree(src, dst, dirs_exist_ok=True)
print("Copied dataset to:", os.path.abspath(dst))

shutil.copytree(src, dst2, dirs_exist_ok=True)
print("Copied dataset to:", os.path.abspath(dst2))


# Path to your dbt seeds folder
seeds_path = "my_dbt/seeds/"

# List all CSVs downloaded from KaggleHub
def clean_column(col):
    col = col.strip().lower()
    col = re.sub(r"\s+", "_", col)           # spaces -> underscores
    col = re.sub(r"[^a-z0-9_]", "_", col)    # replace symbols with _
    col = re.sub("_+", "_", col)             # collapse multiple ___ → _
    col = col.rstrip("_")                    # remove trailing underscores
    return col

for file in os.listdir(seeds_path):
    if file.endswith(".csv"):
        path = os.path.join(seeds_path, file)
        df = pd.read_csv(path)

        df.columns = [clean_column(c) for c in df.columns]

        df.to_csv(path, index=False)
        print("Cleaned:", file)