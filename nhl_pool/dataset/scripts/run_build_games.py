import json
from typing import Union
import itertools
import requests

from nhl_pool.config import TEAM_CODES_REF_DIR
from nhl_pool.dataset.fetch.fetch_team_schedule import fetch_team_schedule_by_season
from nhl_pool.dataset.scripts.common import package_params_from_combination
from nhl_pool.dataset.pipelines.build_games import build_games

def run_fetch_team_schedule(params, force=False):
    fetch_team_schedule_by_season(params, force=force)

def run_build_games():
    out = build_games()
    print(f"Wrote: {out}")

if __name__ == "__main__":
    
    # Read in team codes
    with open(TEAM_CODES_REF_DIR, 'r') as f:
        team_dicts = json.load(f) 
    
    # Set query parameters
    abbrevs = [t["abbrev"] for t in team_dicts]
    query_years = [i for i in range(2015,2024+1)]
    query_season_types = [None] # 1: preseason, 2: regular season, 3: playoffs
    
    #### FETCH
    # Get all combinations of the query parameters
    query_combinations = list(itertools.product(abbrevs, query_years, query_season_types))

    for i,c in enumerate(query_combinations):
        print(f"{i+1} of {len(query_combinations)}")
        # Configure query parameters
        params = package_params_from_combination(c)
        
        try:
            # Call API
            run_fetch_team_schedule(params=params, force=False)
            
        except requests.exceptions.RequestException as e:
            print(f"[NETWORK ERROR] {params} -> {e}")
            continue

    #### BUILD
    run_build_games()