import json

from nhl_pool.config import REFERENCE_DIR
from nhl_pool.dataset.api import load_json_gz
from nhl_pool.dataset.fetch.fetch_team_codes import team_codes_raw_path

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

def build_team_codes():
    # define paths
    raw_path = team_codes_raw_path()
    out_path = REFERENCE_DIR / "team_codes.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load object
    raw_obj = load_json_gz(raw_path)
    
    # Extract info
    processed = extract_team_codes(raw_obj)

    # Write to path
    out_path.write_text(json.dumps(processed, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path