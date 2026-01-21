# nhl-playoff-pool-optimizer

Build the highest scoring NHL playoff pool roster using machine learning projections, linear programming, and playoff bracket simulations.

## Project Goal

Every year, my family runs a Stanley Cup playoff pool. This project is a system to:

1. Simulate playoff bracket outcomes (ELO Ranking & Monte Carlo Methods)
2. Predict player points for the playoffs (Machine Learning)
3. Select an optimal fantasy roster (Linear Programming)

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

[MoneyPuck.com](https://moneypuck.com/data.htm) provides a simple API to download NHL player and team data over different seasons.

The [NHL API](https://github.com/Zmalski/NHL-API-Reference?tab=readme-ov-file#get-boxscore) could be a useful source as well.
