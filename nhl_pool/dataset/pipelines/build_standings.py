# From games.csv, compute the regular season standings based on the Win/Loss information

import pandas as pd

from nhl_pool.config import PROCESSED_DIR, GAMES_DIR
from nhl_pool.dataset.scripts.common import build_season_query_key

SEASON_TYPE_NAME = {2: "regular", 3: "playoffs"}

def initialize_standings_dict(teams_list):
    standings = {}
    for team in teams_list:
        standings[team] = {
                           "gamesPlayed": 0,
                           "wins": 0,
                           "losses": 0,
                           "overtimeLosses": 0,
                           "points": 0,
                           "goalsFor": 0,
                           "goalsAgainst": 0,
                           "goalsDiff": 0,
                           "regulationWins": 0,
                           "overtimeWins": 0}
    return standings

def update_standings_from_game(row, standings):
    abbrev_h = row["homeTeamAbbrev"]
    abbrev_a = row["awayTeamAbbrev"]
    
    score_h = row["homeTeamScore"]
    score_a = row["awayTeamScore"]
    
    last_period_type = row["lastPeriodType"]
    
    home_team_win = score_h > score_a
    
    # Update (home team)
    standings[abbrev_h]["gamesPlayed"] += 1
    standings[abbrev_h]["wins"] += home_team_win
    if last_period_type == 'REG':
        standings[abbrev_h]["regulationWins"] += home_team_win
        standings[abbrev_h]["losses"] += (1-home_team_win)
        standings[abbrev_h]["overtimeLosses"] += 0
    elif last_period_type == "OT":
        standings[abbrev_h]["overtimeWins"] += home_team_win
        standings[abbrev_h]["losses"] += 0
        standings[abbrev_h]["overtimeLosses"] += (1-home_team_win)
    else:
        standings[abbrev_h]["losses"] += 0
        standings[abbrev_h]["overtimeLosses"] += (1-home_team_win)
        
    standings[abbrev_h]["points"] = 2*standings[abbrev_h]["wins"] + standings[abbrev_h]["overtimeLosses"]
    standings[abbrev_h]["goalsFor"] += score_h
    standings[abbrev_h]["goalsAgainst"] += score_a
    standings[abbrev_h]["goalsDiff"] = standings[abbrev_h]["goalsFor"] - standings[abbrev_h]["goalsAgainst"]
    
    # Update (away team)
    standings[abbrev_a]["gamesPlayed"] += 1
    standings[abbrev_a]["wins"] += 1-home_team_win
    
    if last_period_type == 'REG':
        standings[abbrev_a]["regulationWins"] += 1-home_team_win
        standings[abbrev_a]["losses"] += home_team_win
        standings[abbrev_a]["overtimeLosses"] += 0
    elif last_period_type == "OT":
        standings[abbrev_a]["overtimeWins"] += 1-home_team_win
        standings[abbrev_a]["losses"] += 0
        standings[abbrev_a]["overtimeLosses"] += home_team_win
    else:
        standings[abbrev_a]["losses"] += 0
        standings[abbrev_a]["overtimeLosses"] += home_team_win
        
    standings[abbrev_a]["points"] = 2*standings[abbrev_a]["wins"] + standings[abbrev_a]["overtimeLosses"]
    standings[abbrev_a]["goalsFor"] += score_a
    standings[abbrev_a]["goalsAgainst"] += score_h
    standings[abbrev_a]["goalsDiff"] = standings[abbrev_a]["goalsFor"] - standings[abbrev_a]["goalsAgainst"]
    
    return standings

def standings_dict_to_df(standings):
    teams = list(standings.keys())
    
    wins = []
    losses = []
    overtimeLosses = []
    points = []
    goalsFor = []
    goalsAgainst = []
    goalsDiff = []
    regulationWins = []
    overtimeWins = []
    regulationAndOvertimeWins = []
    
    for team in teams:
        wins.append(standings[team]["wins"])
        losses.append(standings[team]["losses"])
        overtimeLosses.append(standings[team]["overtimeLosses"])
        points.append(standings[team]["points"])
        goalsFor.append(standings[team]["goalsFor"])
        goalsAgainst.append(standings[team]["goalsAgainst"])
        goalsDiff.append(standings[team]["goalsDiff"])
        regulationWins.append(standings[team]["regulationWins"])
        overtimeWins.append(standings[team]["overtimeWins"])
        regulationAndOvertimeWins.append(standings[team]["regulationWins"] + standings[team]["overtimeWins"])
        
    data = {
        "teamAbbrev": teams,
        "wins": wins,
        "losses": losses,
        "overtimeLosses": overtimeLosses,
        "points": points,
        "goalsFor": goalsFor,
        "goalsAgainst": goalsAgainst,
        "goalsDiff": goalsDiff,
        "regulationWins": regulationWins,
        "overtimeWins": overtimeWins,
        "regulationAndOvertimeWins": regulationAndOvertimeWins
    }
    standings_df = pd.DataFrame(data)
    standings_df['rank'] = standings_df['points'].rank(ascending=False).astype(int)
    return standings_df.sort_values(by="points", ascending=False)

def build_league_standings_season(year, game_type=2):
    '''Builds league standings for one regular season, given games.csv already exists.'''
    
    # Read data
    games_raw = pd.read_csv(GAMES_DIR)
    games_raw['gameId'] = games_raw['gameId'].astype(str)
    
    # Filter for year and game type
    mask = (games_raw['gameId'].str.startswith(str(year))) & (games_raw['gameType'] == game_type)
    games = games_raw[mask]
    
    # Get list of team in this season
    teams_list = list(games['homeTeamAbbrev'].unique())
    
    # Initialize standings
    standings = initialize_standings_dict(teams_list)
    
    # Update standings for each game
    for _, row in games.iterrows():
        standings = update_standings_from_game(row, standings)
    
    # Convert to a dataFrame
    standings_df = standings_dict_to_df(standings)
    
    # Write to path as csv
    out_path = PROCESSED_DIR / build_season_query_key(year) / SEASON_TYPE_NAME[game_type]
    out_path.mkdir(parents=True, exist_ok=True)
    
    out_path = out_path / "standings.csv"
    
    standings_df.to_csv(out_path, index=False)
    
    return out_path