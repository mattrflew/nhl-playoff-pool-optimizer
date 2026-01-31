# nhl-playoff-pool-optimizer

Build the highest scoring NHL playoff pool roster using machine learning projections, linear programming, and playoff bracket simulations.

## Project Goal

Every year, my family runs a NHL Stanley Cup playoff pool. This project is a system to:

1. Simulate playoff bracket outcomes (ELO Ranking & Monte Carlo Methods)
2. Predict player points for the playoffs (Machine Learning)
3. Select an optimal fantasy roster (Linear Programming)
4. And most importantly, win the playoff pool (Bragging Rights).

While doing this might break the spirit of a fun family competition, it provides for an interesting project. I have also consistently done poorly in this playoff pool, so I clearly need to change my old strategy of hurriedly choosing players the day before the deadline.

## Fantasy League Rules

### Roster Contraints

The roster is selected once at the beginning of the playoffs.

- 15 skaters total
  - 9 forwards
  - 6 defence
- 2 goalies

### Scoring

Skaters:

- Goal: 2 Points
- Assist: 1 Point

Goalies:

- Win: 1 Point
- Assist: 1 Point
- Shutout: 2 Points

## Environment setup

This project requires you to run **both** a `requirements.txt` and a `pyproject.toml`.

### Create and activate a virtual environment

From the repository root:

```
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies

```
pip install -r requirements.txt
```

### Install project package

For importing purposes within the project:

```
pip install -e
```

## Data

All data for this project is sourced from the public NHL API. There are two useful community-maintained documentations of this API:

- https://github.com/Zmalski/NHL-API-Reference
- https://gitlab.com/dword4/nhlapi/-/blob/master/new-api.md

These resources were used to identify endpoints for team metadata, schedules, and player statistics.

### Downloading data

The entire data ingestion pipeline can be run via the following script:

```
python -m nhl_pool.dataset.scripts.run_all
```

This script performs the full workflow:

1. Fetches and builds team code reference data,
2. Downloads team schedules across seasons and compiles game-level data (boxscore information),
3. Downloads player statistics by team and season, and compiles them into tables.

All raw API responses are saved as cache to a `data/raw` directory at the root of the repository.

Similarly, processed results ready for analysis exist at `data/processed`.

All code used to query the API and compile data exists in `nhl_pool/dataset`

At a high level:

- `fetch/` contains wrappers for NHL API endpoints,
- `pipelines/` handles compiling raw responses into tables,
- `scripts/` provides run-able scripts for the run and build steps.

The pipeline is modular such that individual components (i.e. only running player stats) can be run independently if desired.

## notebooks

This directory contains all of the exploratory work for this project. They serve to develop scripts, tune parameters, build models, etc.

The notebooks are organized such that their prefix indicates the chronological order in which they were developed.

All design choices for the overall system are justified throughout these notebooks.
