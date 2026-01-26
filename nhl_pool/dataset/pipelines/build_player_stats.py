import json
from pathlib import Path
import pandas as pd

from nhl_pool.dataset.scripts.common import build_season_query_key
from nhl_pool.dataset.api import load_json_gz
from nhl_pool.config import RAW_DIR, PROCESSED_DIR, REFERENCE_DIR

from nhl_pool.dataset.api import NHLAPI

SEASON_TYPE_NAME = {2: "regular", 3: "playoffs"}

def extract_skater_stats_from_file(path):
    '''From each raw json file, extract skater stats.'''
    raw = load_json_gz(path)
    
    # Get metadata
    teamAbbrev = path.stem.split(".")[0]
    season = path.parts[-3]
    season_type = path.parts[-2]
    
    players = raw.get("skaters")
    
    out = []
    
    for p in players:
        player_id = p.get("playerId")

        if player_id is None:
            continue
        
        first = p.get("firstName", {}) or {}
        last = p.get("lastName", {}) or {}
        
        out.append(
            {
                "playerId": player_id,
                "firstName": first.get("default"),
                "lastName": last.get("default"),
                "teamAbbrev": teamAbbrev,
                "season": season,
                "seasonType": season_type,
                "positionCode": p.get("positionCode"),
                "gamesPlayed": p.get("gamesPlayed"),
                "goals": p.get("goals"),
                "assists": p.get("assists"),
                "points": p.get("points"),
                "plusMinus": p.get("plusMinus"),
                "penaltyMinutes": p.get("penaltyMinutes"),
                "powerPlayGoals": p.get("powerPlayGoals"),
                "shorthandedGoals": p.get("shorthandedGoals"),
                "gameWinningGoals": p.get("gameWinningGoals"),
                "overtimeGoals": p.get("overtimeGoals"),
                "shots": p.get("shots"),
                "shootingPctg": p.get("shootingPctg"),
                "avgTimeOnIcePerGame": p.get("avgTimeOnIcePerGame"),
                "avgShiftsPerGame": p.get("avgShiftsPerGame"),
                "faceoffWinPctg": p.get("faceoffWinPctg"),
                "sourceFile": str(path)
            }
        )
            
    return out

def extract_goalie_stats_from_file(path):
    '''From each raw json file, extract goalie stats.'''
    raw = load_json_gz(path)
    
    # Get metadata
    teamAbbrev = path.stem.split(".")[0]
    season = path.parts[-3]
    season_type = path.parts[-2]
    
    players = raw.get("goalies")
    
    out = []
    
    for p in players:
        player_id = p.get("playerId")

        if player_id is None:
            continue
        
        first = p.get("firstName", {}) or {}
        last = p.get("lastName", {}) or {}
        
        out.append(
            {
                "playerId": player_id,
                "firstName": first.get("default"),
                "lastName": last.get("default"),
                "teamAbbrev": teamAbbrev,
                "season": season,
                "seasonType": season_type,
                "positionCode": "G",
                "gamesPlayed": p.get("gamesPlayed"),
                "gamesStarted": p.get("gamesStarted"),
                "wins": p.get("wins"),
                "losses": p.get("losses"),
                "overtimeLosses": p.get("overtimeLosses"),
                "goalsAgainstAverage": p.get("goalsAgainstAverage"),                
                "savePercentage": p.get("savePercentage"),
                "shotsAgainst": p.get("shotsAgainst"),                
                "saves": p.get("saves"),
                "goalsAgainst": p.get("goalsAgainst"),                
                "shutouts": p.get("shutouts"),
                "goalsAgainst": p.get("goalsAgainst"),                
                "goals": p.get("goals"),
                "assists": p.get("assists"),
                "points": p.get("points"),
                "penaltyMinutes": p.get("penaltyMinutes"),                
                "timeOnIce": p.get("timeOnIce"),
                "sourceFile": str(path)
            }
        )
    
    return out

def build_player_stats(year, season_type):
    '''Search for all stats files per season and season type in the raw/cached data 
    and save relevant information to two .csv files, skaters.csv and goalies.csv'''
    
    season = build_season_query_key(year)
    
    # Get paths of all saved stats files
    stats_dir = RAW_DIR / season / str(season_type)

    stats_files = list(stats_dir.glob("*.json.gz"))
    
    # Initialize
    skaters = []
    goalies = []
    
    for path in stats_files:
        skaters.extend(extract_skater_stats_from_file(path))
        goalies.extend(extract_goalie_stats_from_file(path))
    
    # Turn into dataframes
    skaters_df = pd.DataFrame(skaters)
    goalies_df = pd.DataFrame(goalies)
    
    # Save to file
    save_path = PROCESSED_DIR / season / SEASON_TYPE_NAME[season_type]
    save_path.mkdir(parents=True, exist_ok=True)
    
    skaters_path = save_path / "skaters.csv"
    goalies_path = save_path / "goalies.csv"
    
    skaters_df.to_csv(skaters_path, index=False)
    goalies_df.to_csv(goalies_path, index=False)
    
    return skaters_path, goalies_path