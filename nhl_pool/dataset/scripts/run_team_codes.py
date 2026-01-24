from nhl_pool.dataset.fetch.fetch_team_codes import fetch_team_codes
from nhl_pool.dataset.pipelines.build_team_codes import build_team_codes

def run_team_codes(force=False):
    fetch_team_codes(force=force)
    out = build_team_codes()
    print(f"Wrote: {out}")

if __name__ == "__main__":
    run_team_codes(force=False)