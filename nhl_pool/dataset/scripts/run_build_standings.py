from nhl_pool.dataset.pipelines.build_standings import build_league_standings_season
import itertools

def run_league_standings(start_year=2015, end_year=2024, season_types=(2,3)):
    years = list(range(start_year, end_year+1))
    
    combinations = list(itertools.product(years, season_types))
    
    for c in combinations:
        out = build_league_standings_season(year=c[0], game_type=c[1])
        print(f"Wrote: {out}")

if __name__ == "__main__":
    run_league_standings()