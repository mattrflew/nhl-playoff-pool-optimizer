# Wrapper script to run download and compile function for given season(s).

from nhl_pool.dataset.scripts.run_team_codes import run_team_codes
from nhl_pool.dataset.scripts.run_build_games import run_build_games_script
from nhl_pool.dataset.scripts.run_player_stats import run_player_stats_script
from nhl_pool.dataset.scripts.run_build_standings import run_league_standings

from nhl_pool.config import RAW_DIR, REFERENCE_DIR, PROCESSED_DIR

def run_all(
    force_team_codes: bool = False,
    force_games_fetch: bool = False,
    force_player_fetch: bool = False,
    start_year = 2015,
    end_year = 2024
):
    # 1) Team codes must exist before the other scripts read TEAM_CODES_REF_DIR
    print(f"DOWNLOADING TEAM CODES")
    run_team_codes(force=force_team_codes)

    # 2) Build games (fetch schedules + compile)
    print(f"DOWNLOADING GAMES")
    run_build_games_script(
        start_year=start_year,
        end_year=end_year,
        season_types=(None,),
        force_fetch=force_games_fetch,
    )
    # 3) Build standings (from games.csv)
    print("BUILDING LEAGUE STANDINGS")
    run_league_standings(
        start_year=start_year,
        end_year=end_year,
        season_types=(2, 3))

    # 4) Player stats (fetch + compile)
    print(f"DOWNLOADING PLAYER STATS")
    run_player_stats_script(
        start_year=start_year,
        end_year=end_year,
        season_types=(2, 3),
        force_fetch=force_player_fetch,
    )


if __name__ == "__main__":
    # Create the relevant directories
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    run_all(
        force_team_codes=False,
        force_games_fetch=False,
        force_player_fetch=False,
    )
