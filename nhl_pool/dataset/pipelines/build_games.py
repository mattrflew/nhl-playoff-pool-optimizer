import json
import pandas as pd
import glob

from nhl_pool.dataset.api import load_json_gz
from nhl_pool.config import RAW_DIR, PROCESSED_DIR

def extract_game_info_from_schedule(path):
    '''From each raw json file, extract only the game information we care about.'''
    raw = load_json_gz(path)
    games = raw.get("games")
    
    out = []
    
    for g in games:
        game_id = g.get("id")

        if game_id is None:
            continue
        
        away = g.get("awayTeam", {}) or {}
        home = g.get("homeTeam", {}) or {}
        outcome = g.get("gameOutcome", {}) or {}

        out.append(
            {
                "gameId": game_id,
                "gameType": g.get("gameType"),
                "gameDate": g.get("gameDate"),
                "gameState": g.get("gameState"),
                "awayTeamId": away.get("id"),
                "awayTeamAbbrev": away.get("abbrev"),
                "awayTeamScore": away.get("score"),
                "homeTeamId": home.get("id"),
                "homeTeamAbbrev": home.get("abbrev"),
                "homeTeamScore": home.get("score"),
                "lastPeriodType": outcome.get("lastPeriodType"),
                "sourceFile": str(path),
            }
        )
            
    return out

def build_games():
    '''Search for all team schedules in the raw/cached data and save relevant information to one .csv file.'''
    
    # Get paths of all save schedules
    schedule_files = list(RAW_DIR.glob("*/schedules/*.json.gz"))
    rows = []
    
    # Iterate over all files
    for path in schedule_files:
        rows.extend(extract_game_info_from_schedule(path))
    
    # Turn into dataframe
    df = pd.DataFrame(rows)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=["gameId"]).reset_index(drop=True)
    
    # Fix dtypes
    df["awayTeamScore"] = pd.to_numeric(df["awayTeamScore"], errors="coerce").astype("Int64")
    df["homeTeamScore"] = pd.to_numeric(df["homeTeamScore"], errors="coerce").astype("Int64")
    
    # Sort by gameId
    df = df.sort_values(by='gameId')
    
    # Save to csv
    games_path = PROCESSED_DIR / "games.csv"
    df.to_csv(games_path, index=False)
    
    return games_path