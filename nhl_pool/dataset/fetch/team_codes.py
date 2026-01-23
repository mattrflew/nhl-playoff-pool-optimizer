from pathlib import Path

from nhl_pool.config import RAW_DIR
from nhl_pool.dataset.api import NHLAPI 

def team_codes_raw_path() -> Path:
    return RAW_DIR / "team_codes" / "team_codes.json.gz"

def fetch_team_codes(force: bool = False) -> Path:
    """
    Fetch + cache raw team codes JSON to data/raw.
    Returns the raw cache path.
    """
    api = NHLAPI()
    # IMPORTANT: NHLAPI.get_team_codes() must save to team_codes_raw_path()
    api.get_team_codes(force=force)
    return team_codes_raw_path()
