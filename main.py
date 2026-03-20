import pandas as pd
import requests
from pathlib import Path
from tqdm import tqdm

CSV_PATH = "observations.csv"
USER_AGENT = "Mozilla/5.0 (compatible; BulkImageDownloader/1.0)"

Path("images").mkdir(exist_ok=True)

df = pd.read_csv(CSV_PATH)
df = df[["uuid", "image_url"]].dropna()

success = failed = 0
for _, row in tqdm(df.iterrows(), total=len(df), desc="Downloading", unit="img"):
    uuid = row["uuid"]
    url = row["image_url"]

    try:
        img_resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
        img_resp.raise_for_status()

        with open(f"./images/{uuid}.jpg", "wb") as f:
            f.write(img_resp.content)

        success += 1

    except requests.exceptions.RequestException:
        failed += 1

print(f"Successful: {success}")
print(f"Failed: {failed}")
print(f"Total: {len(df)}")
