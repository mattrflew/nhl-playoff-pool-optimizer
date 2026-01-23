import json
from pathlib import Path

from nhl_pool.dataset.api import load_json_gz
from nhl_pool.config import RAW_DIR, REFERENCE_DIR

from nhl_pool.dataset.api import NHLAPI


def extract_team_codes(data):
    '''
    Convert raw NHL API team codes response into a minimal schema.
    
    Returns a list of dicts like:
    [
    {"id": 8, "abbrev": "MTL", "name": "Montréal Canadiens", "franchiseId": 1},
    ...
    ]
    '''
    # Don't include very old teams (Atlanta Thrashers should be the oldest team still included)
    old_team_abbrevs = ["AFM", "BRK", "CGS", "CLE", "CLR", "DCG", "DFL", "HAM", "HFD", "KCS", "MMR",
                        "MNS", "MWN", "NYA", "OAK", "PIR", "QBD", "QUA", "QUE", "SEN", "SLE", "TAN",
                        "TSP", "WIN"]
    
    out = []
    for team in data["data"]:
        # Extract info
        team_id = team.get("id")
        abbrev = team.get("triCode")
        name = team.get("fullName")
        franchise_id  = team.get("franchiseId")
        
        # Exit early if empty
        if team_id is None and abbrev is None and name is None and franchise_id is None:
            continue
        
        # Skip old teams and future placeholders
        if abbrev in old_team_abbrevs or abbrev == "TBD":
            continue
        
        # Package
        out.append(
            {
                "id": team_id,
                "abbrev": abbrev,
                "name": name,
                "franchiseId": franchise_id 
            }
        )

    return out

def run_team_codes(force_fetch=False):
    # Call API
    api = NHLAPI()
    api.get_team_codes(force=force_fetch)
    
    # define paths
    raw_path = RAW_DIR / "team_codes" / "team_codes.json.gz"
    out_path = REFERENCE_DIR / "team_codes.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load object
    raw_obj = api._load_from_cache(raw_path)
    
    # Extract info
    processed = extract_team_codes(raw_obj)

    # Write to path
    out_path.write_text(json.dumps(processed, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path