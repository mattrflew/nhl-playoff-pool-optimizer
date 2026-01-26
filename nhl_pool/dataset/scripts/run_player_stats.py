import json
import itertools
import requests

from nhl_pool.config import TEAM_CODES_REF_DIR
from nhl_pool.dataset.fetch.fetch_player_stats import fetch_player_stats_by_team_and_season
from nhl_pool.dataset.scripts.common import package_params_from_combination
from nhl_pool.dataset.pipelines.build_player_stats import build_player_stats

def run_fetch_player_stats(params, force=False):
    fetch_player_stats_by_team_and_season(params, force=force)

def run_build_player_stats(year, season_type):
    out = build_player_stats(year, season_type)
    print(f"Wrote: {out}")

def run_player_stats_script(
    start_year: int = 2015,
    end_year: int = 2024,
    season_types=(2, 3),
    force_fetch: bool = False,
):
    with open(TEAM_CODES_REF_DIR, "r") as f:
        team_dicts = json.load(f)

    abbrevs = [t["abbrev"] for t in team_dicts]
    query_years = list(range(start_year, end_year + 1))
    query_season_types = list(season_types)

    # FETCH
    query_combinations = list(itertools.product(abbrevs, query_years, query_season_types))
    for i, c in enumerate(query_combinations, start=1):
        print(f"{i} of {len(query_combinations)}")
        params = package_params_from_combination(c)
        try:
            run_fetch_player_stats(params=params, force=force_fetch)
        except requests.exceptions.RequestException as e:
            print(f"[NETWORK ERROR] {params} -> {e}")
            continue

    # BUILD
    build_combinations = list(itertools.product(query_years, query_season_types))
    for year, season_type in build_combinations:
        run_build_player_stats(year, season_type)


if __name__ == "__main__":
    run_player_stats_script()