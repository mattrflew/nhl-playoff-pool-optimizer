from nhl_pool.dataset.pipelines.process_team_codes import run_team_codes

def main():
    outputs = []
    outputs.append(run_team_codes())
    for p in outputs:
        print(f"Wrote: {p}")

if __name__ == "__main__":
    main()