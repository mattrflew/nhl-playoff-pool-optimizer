# nhl_pool\dataset

This directory contains all of the scripts to download and process data from the NHL APIs.

There are two useful community-maintained documentations of these APIs:

- [github.com/Zmalski/NHL-API-Reference](https://github.com/Zmalski/NHL-API-Reference)
- [gitlab.com/dword4/nhlapi/-/blob/master/new-api.md](https://gitlab.com/dword4/nhlapi/-/blob/master/new-api.md)

## Directory structure

### api.py

Contains a class method to interact with the NHL API.

### \fetch

Contains all functions that utilize the API and saves responses to data\raw.

### \pipelines

Contains all functions which takes raw data and processes it and saves to data\processed.

### \scripts

Contains executable scripts that call the fetch and pipeline functions.
