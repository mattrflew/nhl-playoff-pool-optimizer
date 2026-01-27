# Reusable functions for handling the skaters.csv and goalies.csv files
import pandas as pd
import numpy as np

from nhl_pool.processing.common import weighted_average

def collapse_one_skater(df):
    '''For one season, collapse the dataFrame to account for skaters who played on more than one team in a season.
    Depending on the statistic, either sum together, take weighted average (based on games played), or other.
    Will concatenate team abbreviations (i.e. if played on "MTL" and "TOR", it will be "MTL,TOR" with no consideration of chronological order).
    '''
    
    # What columns to sum together
    SUM_COLS = [
        "gamesPlayed", "goals", "assists", "points", "plusMinus",
        "penaltyMinutes", "powerPlayGoals", "shorthandedGoals",
        "gameWinningGoals", "overtimeGoals", "shots",
    ]
    # What columns to take weighted average
    WAVG_COLS = ["avgTimeOnIcePerGame", "avgShiftsPerGame", "faceoffWinPctg"]
    
    # For ID columns, select the first appearing
    ID_COLS_FIRST = ["firstName", "lastName", "season", "seasonType", "positionCode"]
    
    # Initialise
    out = {}

    for c in ID_COLS_FIRST:
        out[c] = df[c].dropna().iloc[0] if df[c].notna().any() else np.nan

    # teamAbbrev: concatenate unique teams
    teams = df["teamAbbrev"].dropna().astype(str).unique()
    out["teamAbbrev"] = ",".join(sorted(teams)) if len(teams) else np.nan

    # sums
    for c in SUM_COLS:
        out[c] = pd.to_numeric(df[c], errors="coerce").sum(min_count=1)

    # weighted avgs by gamesPlayed
    for c in WAVG_COLS:
        out[c] = weighted_average(df[c], df["gamesPlayed"])

    # shooting % recomputed from totals
    goals = out.get("goals", np.nan)
    shots = out.get("shots", np.nan)
    out["shootingPctg"] = (goals / shots) if pd.notna(shots) and shots != 0 else np.nan

    # join source files
    out["sourceFile"] = "|".join(sorted(set(map(str, df["sourceFile"].dropna()))))

    return pd.Series(out)

def collapse_one_goalie(df):
    '''For one season, collapse the dataFrame to account for goalies who played on more than one team in a season.
    Depending on the statistic, either sum together, take weighted average (based on games played), or other.
    Will concatenate team abbreviations (i.e. if played on "MTL" and "TOR", it will be "MTL,TOR" with no consideration of chronological order).
    '''
    
    # What columns to sum together
    SUM_COLS = [
        "gamesPlayed", "gamesStarted", "wins", "losses",
        "overtimeLosses", "shotsAgainst", "saves", "goalsAgainst",
        "shutouts", "goals", "assists", "points", 
        "penaltyMinutes", "timeOnIce"]
    
    # What columns to take weighted average
    WAVG_COLS = []
    
    # For ID columns, select the first appearing
    ID_COLS_FIRST = ["firstName", "lastName", "season", "seasonType", "positionCode"]

    # Initialise
    out = {}

    for c in ID_COLS_FIRST:
        out[c] = df[c].dropna().iloc[0] if df[c].notna().any() else np.nan

    # teamAbbrev: concatenate unique teams
    teams = df["teamAbbrev"].dropna().astype(str).unique()
    out["teamAbbrev"] = ",".join(sorted(teams)) if len(teams) else np.nan

    # sums
    for c in SUM_COLS:
        out[c] = pd.to_numeric(df[c], errors="coerce").sum(min_count=1)

    # weighted avgs by gamesPlayed
    for c in WAVG_COLS:
        out[c] = weighted_average(df[c], df["gamesPlayed"])

    # savePercentage recomputed from totals
    saves = out.get("saves", np.nan)
    shots = out.get("shotsAgainst", np.nan)
    out["savePercentage"] = (saves / shots) if (pd.notna(shots) and shots != 0) else np.nan

    # goalsAgainstAverage recomputed from totals
    goals_against = out.get("goals_against", np.nan)
    time_on_ice = out.get("timeOnIce", np.nan)
    out["goalsAgainstAverage"] = (goals_against * 60.0) / (time_on_ice / 60.0) if (pd.notna(time_on_ice) and time_on_ice != 0) else np.nan



    # join source files
    out["sourceFile"] = "|".join(sorted(set(map(str, df["sourceFile"].dropna()))))

    return pd.Series(out)

def collapse_players(df, key='playerId', collapse_type="skater"):
    # 1) Identify duplicated player-season entries
    dup_mask = df.duplicated(key, keep=False)

    df_single = df.loc[~dup_mask].copy()
    df_dups   = df.loc[dup_mask].copy()
    
    if df_dups.empty:
        return df_single.reset_index(drop=True)
    
    # 2) Collapse only the duplicated groups
    if collapse_type == "skater":
        collapse_function = collapse_one_skater
    elif collapse_type == "goalie":
        collapse_function = collapse_one_goalie
        
    df_dups_collapsed = (
        df_dups.groupby(key, dropna=False, as_index=False)
            .apply(collapse_function)
            .reset_index(drop=True)
        )
    
    # 3) Combine back together (keeping singles unchanged)
    df_fixed = pd.concat([df_single, df_dups_collapsed], ignore_index=True)
    
    return df_fixed

def map_positions(df):
    '''The league points system makes no distinction 
    between C, LW, and RW. So we need to map these positions to simply forward, "F"'''
    
    position_map = {
        "C": "F",
        "L": "F",
        "R": "F",
        "D": "D",
        "G": "G",
    }   
    
    df["positionCode"] = df["positionCode"].map(position_map)
    return df