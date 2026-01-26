from pathlib import Path

from nhl_pool.config import RAW_DIR
from nhl_pool.dataset.api import NHLAPI 

def team_schedule_raw_path(params):
    # Unpack params
    abbrev = params["abbrev"]
    season = params["season"]
    
    return RAW_DIR / str(season) / "schedules" / f"{str(abbrev)}.json.gz"

def fetch_team_schedule_by_season(params, force=False):
    """
    Fetch + cache raw by team schedule by season JSON to data/raw.
    Returns the raw cache path.
    params contains team abbrev, season.
    """
    
    api = NHLAPI()
    api.get_team_schedule(params=params, force=force)
    return team_schedule_raw_path(params)