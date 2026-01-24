from pathlib import Path

from nhl_pool.config import RAW_DIR
from nhl_pool.dataset.api import NHLAPI 

def player_stats_raw_path(params):
    # Unpack params
    abbrev = params["abbrev"]
    season = params["season"]
    season_type = params["season_type"]
    
    return RAW_DIR / str(season) / str(season_type) / f"{str(abbrev)}.json.gz"

def fetch_player_stats_by_team_and_season(params, force=False):
    """
    Fetch + cache raw player stats (by team for season and season type) JSON to data/raw.
    Returns the raw cache path.
    params contains team abbrev, season, and season type.
    """
    
    api = NHLAPI()
    api.get_team_roster_stats(params=params, force=force)
    return player_stats_raw_path(params)
