# NHL API Class (fetch and cache only)

import json, gzip
from pathlib import Path
import requests
from nhl_pool.config import RAW_DIR

#### DEALING WITH CACHE FILES

def load_json_gz(path: Path):
    '''Load existing cache file.'''
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)

def save_json_gz(path: Path, obj):
    '''Save response to cache.'''
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with gzip.open(tmp, "wt", encoding="utf-8") as f:
        json.dump(obj, f)
    tmp.replace(path)

class NHLAPI:
    BASE_URL_WEB = "https://api-web.nhle.com/v1/"
    BASE_URL_STATS = "https://api.nhle.com/stats/rest/en/"
    
    def __init__(self, raw_root=RAW_DIR, sleep_s=0.05, timeout_s=30, retries=2):
        self.raw_root = raw_root
        self.sleep_s = sleep_s
        self.timeout_s = timeout_s
        self.retries = retries
        self.session = requests.Session()
    
    #### CACHING
    def _cache_path(self, *parts):
        return self.raw_root.joinpath(*parts)
    
    def _load_from_cache(self, cache_path: Path):
        if cache_path.exists():
            return load_json_gz(cache_path)
        return None
    
    def _save_to_cache(self, data, cache_path):
        if data is None:
            return
        save_json_gz(cache_path, data)

    #### INTERACT WITH API
    def _make_request(self, base_url, endpoint, force=False):
        """
        Internal helper method to make a GET request to an endpoint.
        """
        url = f"{base_url}{endpoint}"
        self.query_url = url
        try:
            response = self.session.get(url, timeout=self.timeout_s)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    #### GET
    
    # Team Codes
    def _team_codes_endpoint(self):
        return f"team"
    
    def get_team_codes(self, force=False):
        '''Fetches all team codes.'''
        cache_path = self._cache_path("team_codes", "team_codes.json.gz")
        
        # Return if cache already exists
        if not force:
            cached = self._load_from_cache(cache_path)
            if cached is not None:
                return cached
            
        # Call API
        endpoint = self._team_codes_endpoint()
        data = self._make_request(base_url=self.BASE_URL_STATS, endpoint=endpoint, force=force)
        
        # Save to cache
        self._save_to_cache(data, cache_path)
        
        return data

    # Player stats by team and season
    def _player_stats_endpoint(self, abbrev, season, season_type):
        return f"club-stats/{abbrev}/{season}/{season_type}"
    
    def get_team_roster_stats(self, params, force=False):
        '''Fetches the stats for an entire team's roster for a single season.'''
        # Unpack params
        abbrev = params["abbrev"]
        season = params["season"]
        season_type = params["season_type"]
        
        cache_path = self._cache_path(str(season), str(season_type), f"{str(abbrev)}.json.gz")
        
        # Return if cache already exists
        if not force:
            cached = self._load_from_cache(cache_path)
            if cached is not None:
                return cached
        
        # Call API
        endpoint = self._player_stats_endpoint(abbrev, season, season_type)
        data = self._make_request(base_url=self.BASE_URL_WEB, endpoint=endpoint, force=force)
        
        # Save to cache
        self._save_to_cache(data, cache_path)
        
        return data
