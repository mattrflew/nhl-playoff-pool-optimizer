# nhl-playoff-pool-optimizer

Build the highest scoring NHL playoff pool roster using machine learning projections, linear programming, and playoff bracket simulations.

## Project Goal

Every year, my family runs a NHL Stanley Cup playoff pool. This project is a system to:

1. Simulate playoff bracket outcomes (ELO Ranking & Monte Carlo Methods)
2. Predict player points for the playoffs (Machine Learning)
3. Select an optimal fantasy roster (Linear Programming)
4. And most importantly, win the playoff pool (Bragging Rights).

While this might break the spirit of a fun family competition, it provides for an interesting project. I have also consistently done poorly in this playoff pool, so I clearly need to change my old strategy of hurriedly choosing players the day before the deadline.

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

## Data

The NHL API will be the source of data.

There are two useful community documentations of this API.

- https://github.com/Zmalski/NHL-API-Reference
- https://gitlab.com/dword4/nhlapi/-/blob/master/new-api.md
