import pandas as pd
import numpy as np
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
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 4 < 2:
        values[i] = [teams[4*floor(i/4)+2],teams[4*floor(i/4)+3]]
    else:
        values[i] = [teams[4*ceil(i/4)-4],teams[4*ceil(i/4)-3]]

secondround = dict(zip(teams, values))
#print(secondround)

# Put second round probabilities in
results['Second Round'] = [sum(df.loc[i, j]*results.loc[j, 'First Round']*results.loc[i, 'First Round'] for j in secondround[i]) for i in teams ]


# Create dictionary for round three matchups, same format as round two
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 8 < 4:
        values[i] = [teams[8*floor(i/8)+4],teams[8*floor(i/8)+5],teams[8*floor(i/8)+6],teams[8*floor(i/8)+7]]
    else:
        values[i] = [teams[8*ceil(i/8)-8],teams[8*ceil(i/8)-7],teams[8*ceil(i/8)-6],teams[8*ceil(i/8)-5]]

thirdround = dict(zip(teams, values))
#print(thirdround)

# Put second round probabilities in
results['Third Round'] = [sum(df.loc[i, j]*results.loc[j, 'Second Round']*results.loc[i, 'Second Round'] for j in thirdround[i]) for i in teams]
#print(results.head(8).iloc[:,0:3])

values = [0] * len(teams)
for i in range(len(teams)):
    if i % 16 < 8:
        values[i] = [teams[16*floor(i/16)+8],teams[16*floor(i/16)+9],teams[16*floor(i/16)+10],teams[16*floor(i/16)+11],teams[16*floor(i/16)+12],teams[16*floor(i/16)+13],teams[16*floor(i/16)+14],teams[16*floor(i/16)+15]]
    else:
        values[i] = [teams[16*ceil(i/16)-16],teams[16*ceil(i/16)-15],teams[16*ceil(i/16)-14],teams[16*ceil(i/16)-13],teams[16*ceil(i/16)-12],teams[16*ceil(i/16)-11],teams[16*ceil(i/16)-10],teams[16*ceil(i/16)-9]]

fourthround = dict(zip(teams, values))



results['Fourth Round'] = [sum(df.loc[i, j]*results.loc[j, 'Third Round']*results.loc[i, 'Third Round'] for j in fourthround[i]) for i in teams]
print(results.head(16).iloc[:,0:4])





