#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 15:07:30 2022

@author: carsonletts
"""
import pandas as pd
import numpy as np
import requests
import io

# Pull in initial CSV file from Github and transform it into a Dataframe

url = "https://raw.githubusercontent.com/camjm21/4133project/main/March%20Madness.csv"
download = requests.get(url).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')))
df.set_index('TEAM', inplace=True)

# Create initial dictionary for round one matchups, every team will be a key, with their opponent being the value
keys = list(df.index)
values = [0] * len(keys)
for i in range(len(keys)):
    if i % 2 == 0:
        values[i+1] = keys[i]
    else:
        values[i-1] = keys[i]
    
firstround = dict(zip(keys, values))

def win_percentage(teamname, roundnum):
    