from typing import Union

def build_season_query_key(year: Union[int, str]) -> str:
    year = int(year)
    return f"{str(year)}{str(year+1)}"

def package_params_from_combination(combination):
    params = {
        "abbrev": combination[0],
        "season": build_season_query_key(combination[1]),
        "season_type": combination[2]
        }
    return params