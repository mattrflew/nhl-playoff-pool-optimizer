# MoneyPuck

[MoneyPuck.com](https://moneypuck.com/data.htm) provides a simple API to download NHL player and team data over different seasons.

It's a bit disapointing that this site's goalie data does not have a win and shutout category. It may not be the best option.

The "all_teams.csv" file could be useful when trying to build an ELO ranking system since it contains game data, but not super convenient as it will take a bit of logic to get a simple win/loss for each game.

# RotoWire

[RotoWire](https://www.rotowire.com/hockey/stats.php) allows for manual downloading of data.

I think this might be a good data source since it is simple. I'll just manually download .csv files from the site.

This annoyingly does not include a column for unique ID of a player. I can devise one, but need to think of a way to make it match for players across seasons.

Also not great for this dataset is that even when filtering for a player's historical data, the "team" column will be their present team making that a useless column when considering an ML model.
