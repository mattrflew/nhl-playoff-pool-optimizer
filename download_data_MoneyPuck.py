###### download_data.py
# Running this script will download the last X seasons worth of data to the data folder.

# IMPORTS
import requests
import os
from pathlib import Path
from urllib.parse import urljoin
import itertools

# CONSTANTS
# Query URL
BASE_URL = "https://moneypuck.com/moneypuck/playerData/seasonSummary/"

# Save path 
BASE_PATH = Path(r"data\MoneyPuck\raw")
OVERWRITE = True

# DOWNLOAD PARAMETERS
years = [str(year) for year in range(2015, 2025)] 
season_type = ["regular", "playoffs"]
categories = ["skaters", "goalies"] # Choose between skaters, goalies, teams

# Build different combinations of downloads
combinations = list(itertools.product(years, season_type, categories))


# Helper functions
def params_from_combination(combination):
    params = {
    "year": combination[0],
    "season": combination[1],
    "category": combination[2]
    }
    return params

def build_query_url(params):
    return urljoin(BASE_URL, f"{params["year"]}/{params["season"]}/{params["category"]}.csv")

def ffn_from_params(params):
    fpath = os.path.join(BASE_PATH, params["year"], params["season"])
    
    if OVERWRITE or not os.path.exists(fpath):
        os.makedirs(fpath, exist_ok=True)
    
    ffn = os.path.join(fpath, f"{params["category"]}.csv")
    return ffn

def download_to_file(query_url, ffn, params):
    if OVERWRITE or not os.path.exists(ffn):
        response = requests.get(query_url)
        with open(ffn, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {params["year"]} {params["season"]} {params["category"]}")

# RUN
N = len(combinations)
cnt = 0

for combination in combinations:
    cnt += 1
    print(f"Downloading: {cnt} of {N}")
    
    params = params_from_combination(combination)
    query_url = build_query_url(params)
    ffn = ffn_from_params(params)
    
    # Download
    download_to_file(query_url, ffn, params)