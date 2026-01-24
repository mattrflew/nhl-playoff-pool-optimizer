import json
from pathlib import Path
import pandas as pd

from nhl_pool.dataset.api import load_json_gz
from nhl_pool.config import RAW_DIR, PROCESSED_DIR, REFERENCE_DIR

from nhl_pool.dataset.api import NHLAPI

GAME_TYPE_NAME = {2: "regular", 3: "playoffs"}