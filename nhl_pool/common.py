from nhl_pool.config import PROCESSED_DIR

def stats_file_path(params):
    return PROCESSED_DIR / str(params["season"]) / params["season_type"] / f"{params["player_type"]}.csv"

def games_file_path():
    return PROCESSED_DIR / "games.csv"