import pandas as pd
import requests
import io
from math import *

# Pull in initial CSV file from Github and transform it into a Dataframe

url = "https://raw.githubusercontent.com/camjm21/4133project/main/March%20Madness.csv"
download = requests.get(url).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')))
df.set_index('TEAM', inplace=True)

# Create dictionary for round one matchups, every team will be a key, with their opponent being the value
teams = list(df.index)
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 2 == 0:
        values[i+1] = teams[i]
    else:
        values[i-1] = teams[i]

firstround = dict(zip(teams, values))

# Create dataframe to put results in
results = pd.DataFrame(index=teams,columns=['First Round','Second Round', 'Third Round', 'Fourth Round', 'Fifth Round', 'Sixth Round'])

# Put first round probabilities in
results['First Round'] = [df.loc[i, firstround[i]] for i in teams]

# Create dictionary for round two matchups, same format as round one, but the values are lists of the two possible opponents they could face in round two
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 4 < 2:
        values[i] = [teams[4*floor(i/4)+j] for j in range(2,4)]
    else:
        values[i] = [teams[4*ceil(i/4)-j] for j in range(4,2)]

secondround = dict(zip(teams, values))

# Put second round probabilities in
results['Second Round'] = [sum(df.loc[i, j]*results.loc[j, 'First Round']*results.loc[i, 'First Round'] for j in secondround[i]) for i in teams ]

# Create dictionary for round three matchups, same format as round two
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 8 < 4:
        values[i] = [teams[8*floor(i/8)+j] for j in range(4,8)]
    else:
        values[i] = [teams[8*ceil(i/8)+j] for j in range(8,4)]


thirdround = dict(zip(teams, values))

# Put third round probabilities in
results['Third Round'] = [sum(df.loc[i, j]*results.loc[j, 'Second Round']*results.loc[i, 'Second Round'] for j in thirdround[i]) for i in teams]

# Create dictionary for round four matchups, same format as round three
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 16 < 8:
        values[i] = [teams[16*floor(i/16)+j] for j in range(8,16)]
    else:
        values[i] = [teams[16*ceil(i/16)+j] for j in range(16,8)]
        
fourthround = dict(zip(teams, values))

# Put fourth round probabilities in
results['Fourth Round'] = [sum(df.loc[i, j]*results.loc[j, 'Third Round']*results.loc[i, 'Third Round'] for j in fourthround[i]) for i in teams]

# Create dictionary for round five matchups, same format as round four
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 32 < 16:
        values[i] = [teams[32*floor(i/32)+j] for j in range(16,32)]
    else:
        values[i] = [teams[32*ceil(i/32)+j] for j in range(32,16)]

fifthround = dict(zip(teams, values))

# Put fifth round probabilities in
results['Fifth Round'] = [sum(df.loc[i, j]*results.loc[j, 'Fourth Round']*results.loc[i, 'Fourth Round'] for j in fifthround[i]) for i in teams]

# Create dictionary for round six matchups, same format as round five
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 64 < 32:
        values[i] = [teams[64*floor(i/64)+j] for j in range(32,64)]
    else:
        values[i] = [teams[64*ceil(i/64)+j] for j in range(64,32)]


sixthround = dict(zip(teams, values))

# Put sixth round probabilities in
results['Sixth Round'] = [sum(df.loc[i, j]*results.loc[j, 'Fifth Round']*results.loc[i, 'Fifth Round'] for j in sixthround[i]) for i in teams]






