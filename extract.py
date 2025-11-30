import shutil
import os
import re
import kagglehub
import pandas as pd

# Download dataset from KaggleHub
src = kagglehub.dataset_download("yapwh1208/supermarket-sales-data")

# Absolute paths to mounted folders (persistent)
dst = "/opt/airflow/project_root/data"
dst2 = "/opt/airflow/project_root/my_dbt/seeds"

# Ensure target folders exist
os.makedirs(dst, exist_ok=True)
os.makedirs(dst2, exist_ok=True)

# Copy raw dataset to both folders
shutil.copytree(src, dst, dirs_exist_ok=True)
print("Copied dataset to:", os.path.abspath(dst))

shutil.copytree(src, dst2, dirs_exist_ok=True)
print("Copied dataset to:", os.path.abspath(dst2))

# ===============================
# Clean CSV column names for dbt
# ===============================

seeds_path = dst2   # only clean dbt seeds, not /data

def clean_column(col):
    col = col.strip().lower()
    col = re.sub(r"\s+", "_", col)             # spaces -> underscores
    col = re.sub(r"[^a-z0-9_]", "_", col)      # symbols -> _
    col = re.sub("_+", "_", col)               # collapse multiple _
    col = col.rstrip("_")                      # remove trailing _
    return col

for file in os.listdir(seeds_path):
    if file.endswith(".csv"):
        path = os.path.join(seeds_path, file)

        try:
            df = pd.read_csv(path)
        except Exception as e:
            print(f"Skipping {file}, could not parse CSV: {e}")
            continue

        df.columns = [clean_column(c) for c in df.columns]
        df.to_csv(path, index=False)
        print("Cleaned:", file)

print("DONE: Extracted + Cleaned CSV files")
