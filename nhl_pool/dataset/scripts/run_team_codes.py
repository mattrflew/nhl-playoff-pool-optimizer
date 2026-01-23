from nhl_pool.dataset.fetch.team_codes import fetch_team_codes
from nhl_pool.dataset.pipelines.build_team_codes import build_team_codes

if __name__ == "__main__":
    fetch_team_codes(force=False)
    out = build_team_codes()
    print(f"Wrote: {out}")