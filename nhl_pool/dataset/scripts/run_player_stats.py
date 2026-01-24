import json
from typing import Union
import itertools
import requests

from nhl_pool.config import TEAM_CODES_REF_DIR
from nhl_pool.dataset.fetch.fetch_player_stats import fetch_player_stats_by_team_and_season
# from nhl_pool.dataset.pipelines.build_team_codes import build_team_codes

def build_season_query_key(year: Union[int, str]) -> str:
    year = int(year)
    return f"{str(year)}{str(year+1)}"

def package_params_from_combination(combination):
    params = {
        "abbrev": combination[0],
        "season": build_season_query_key(combination[1]),
        "season_type": combination[2]
        }
    return params

def run_fetch_player_stats(params, force=False):
    fetch_player_stats_by_team_and_season(params, force=force)


if __name__ == "__main__":
    
    # Read in team codes
    with open(TEAM_CODES_REF_DIR, 'r') as f:
        team_dicts = json.load(f) 
    
    # Set query parameters
    abbrevs = [t["abbrev"] for t in team_dicts]
    query_years = [2022,2023, 2024]
    query_season_types = [2, 3] # 1: preseason, 2: regular season, 3: playoffs
    
    # Get all combinations of the query parameters
    query_combinations = list(itertools.product(abbrevs, query_years, query_season_types))

    for i,c in enumerate(query_combinations):
        print(f"{i} of {len(query_combinations)}")
        # Configure query parameters
        params = package_params_from_combination(c)
        
        try:
            # Call API
            run_fetch_player_stats(params=params, force=False)
            
        except requests.exceptions.RequestException as e:
            print(f"[NETWORK ERROR] {params} -> {e}")
            continue


    # out = build_team_codes()
    # print(f"Wrote: {out}")