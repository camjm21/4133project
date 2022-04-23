# PART A
import pandas as pd
import requests
import io
from math import *
from gurobipy import *

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
        values[i] = [teams[4*ceil(i/4)-j] for j in range(4,2, -1)]

secondround = dict(zip(teams, values))

# Put second round probabilities in
results['Second Round'] = [sum(df.loc[i, j]*results.loc[j, 'First Round']*results.loc[i, 'First Round'] for j in secondround[i]) for i in teams ]

# Create dictionary for round three matchups, same format as round two
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 8 < 4:
        values[i] = [teams[8*floor(i/8)+j] for j in range(4,8)]
    else:
        values[i] = [teams[8*ceil(i/8)-j] for j in range(8,4, -1)]


thirdround = dict(zip(teams, values))

# Put third round probabilities in
results['Third Round'] = [sum(df.loc[i, j]*results.loc[j, 'Second Round']*results.loc[i, 'Second Round'] for j in thirdround[i]) for i in teams]

# Create dictionary for round four matchups, same format as round three
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 16 < 8:
        values[i] = [teams[16*floor(i/16)+j] for j in range(8,16)]
    else:
        values[i] = [teams[16*ceil(i/16)-j] for j in range(16,8, -1)]
        
fourthround = dict(zip(teams, values))

# Put fourth round probabilities in
results['Fourth Round'] = [sum(df.loc[i, j]*results.loc[j, 'Third Round']*results.loc[i, 'Third Round'] for j in fourthround[i]) for i in teams]

# Create dictionary for round five matchups, same format as round four
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 32 < 16:
        values[i] = [teams[32*floor(i/32)+j] for j in range(16,32)]
    else:
        values[i] = [teams[32*ceil(i/32)-j] for j in range(32,16, -1)]

fifthround = dict(zip(teams, values))

# Put fifth round probabilities in
results['Fifth Round'] = [sum(df.loc[i, j]*results.loc[j, 'Fourth Round']*results.loc[i, 'Fourth Round'] for j in fifthround[i]) for i in teams]

# Create dictionary for round six matchups, same format as round five
values = [0] * len(teams)
for i in range(len(teams)):
    if i % 64 < 32:
        values[i] = [teams[64*floor(i/64)+j] for j in range(32,64)]
    else:
        values[i] = [teams[64*ceil(i/64)-j] for j in range(64,32, -1)]


sixthround = dict(zip(teams, values))

# Put sixth round probabilities in
results['Sixth Round'] = [sum(df.loc[i, j]*results.loc[j, 'Fifth Round']*results.loc[i, 'Fifth Round'] for j in sixthround[i]) for i in teams]



# ****** PART C STARTS HERE *********



# Create model and Indices
m = Model("March Madness")
rounds = results.columns.tolist()
weights = {'First Round' : 1, 'Second Round' : 2, 'Third Round' :4, 'Fourth Round' : 8, 'Fifth Round' : 16, 'Sixth Round' : 32}

# Create decision variables
x = m.addVars(teams, rounds, vtype = GRB.BINARY, name = 'x')

# Create objective function
m.setObjective(quicksum(weights[k] * x[i, k] * results.loc[i, k] for i in teams for k in rounds), GRB.MAXIMIZE)


# Create constraints

# Round 1 Constraints
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Duke', 'N Dakota St']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['VA Commonwealth', 'UCF']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Mississippi St', 'Liberty']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Virginia Tech', 'St Louis']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Maryland', 'Belmont']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['LSU', 'Yale']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Louisville', 'Minnesota']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Michigan St', 'Bradley']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Gonzaga', 'F Dickinson']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Syracuse', 'Baylor']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Marquette', 'Murray St']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Florida St', 'Vermont']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Buffalo', 'Arizona St']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Texas Tech', 'N Kentucky']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Nevada', 'Florida']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Michigan', 'Montana']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Virginia', 'Gardner Webb']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Mississippi', 'Oklahoma']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Wisconsin', 'Oregon']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Kansas St', 'UC Irvine']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Villanova', "St Mary's CA"]) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Purdue', 'Old Dominion']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Cincinnati', 'Iowa']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Tennessee', 'Colgate']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['North Carolina', 'Iona']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Utah St', 'Washington']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Auburn', 'New Mexico St']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Kansas', 'Northeastern']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Iowa St', 'Ohio St']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Houston', 'Georgia St']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Wofford', 'Seton Hall']) == 1)
m.addConstr(quicksum(x[i, 'First Round'] for i in ['Kentucky', 'Abilene Chr']) == 1)

# Round 2 Constraints
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Duke', 'N Dakota St', 'VA Commonwealth', 'UCF']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Mississippi St', 'Liberty', 'Virginia Tech', 'St Louis']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Maryland', 'Belmont', 'LSU', 'Yale']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Louisville', 'Minnesota', 'Michigan St', 'Bradley']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Gonzaga', 'F Dickinson', 'Syracuse', 'Baylor']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Marquette', 'Murray St', 'Florida St', 'Vermont']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Buffalo', 'Arizona St', 'Texas Tech', 'N Kentucky']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Nevada', 'Florida', 'Michigan', 'Montana']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Virginia', 'Gardner Webb', 'Mississippi', 'Oklahoma']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Wisconsin', 'Oregon', 'Kansas St', 'UC Irvine']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Villanova', "St Mary's CA", 'Purdue', 'Old Dominion']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Cincinnati', 'Iowa', 'Tennessee', 'Colgate']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['North Carolina', 'Iona', 'Utah St', 'Washington']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Auburn', 'New Mexico St', 'Kansas', 'Northeastern']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Iowa St', 'Ohio St', 'Houston', 'Georgia St']) == 1)
m.addConstr(quicksum(x[i, 'Second Round'] for i in ['Wofford', 'Seton Hall', 'Kentucky', 'Abilene Chr']) == 1)

# Round 3 Constraints
m.addConstr(quicksum(x[i, 'Third Round'] for i in ['Duke', 'N Dakota St', 'VA Commonwealth', 'UCF', 'Mississippi St', 'Liberty', 'Virginia Tech', 'St Louis']) == 1)
m.addConstr(quicksum(x[i, 'Third Round'] for i in ['Maryland', 'Belmont', 'LSU', 'Yale', 'Louisville', 'Minnesota', 'Michigan St', 'Bradley']) == 1)
m.addConstr(quicksum(x[i, 'Third Round'] for i in ['Gonzaga', 'F Dickinson', 'Syracuse', 'Baylor', 'Marquette', 'Murray St', 'Florida St', 'Vermont']) == 1)
m.addConstr(quicksum(x[i, 'Third Round'] for i in ['Buffalo', 'Arizona St', 'Texas Tech', 'N Kentucky', 'Nevada', 'Florida', 'Michigan', 'Montana']) == 1)
m.addConstr(quicksum(x[i, 'Third Round'] for i in ['Virginia', 'Gardner Webb', 'Mississippi', 'Oklahoma', 'Wisconsin', 'Oregon', 'Kansas St', 'UC Irvine']) == 1)
m.addConstr(quicksum(x[i, 'Third Round'] for i in ['Villanova', "St Mary's CA", 'Purdue', 'Old Dominion', 'Cincinnati', 'Iowa', 'Tennessee', 'Colgate']) == 1)
m.addConstr(quicksum(x[i, 'Third Round'] for i in ['North Carolina', 'Iona', 'Utah St', 'Washington', 'Auburn', 'New Mexico St', 'Kansas', 'Northeastern']) == 1)
m.addConstr(quicksum(x[i, 'Third Round'] for i in ['Iowa St', 'Ohio St', 'Houston', 'Georgia St', 'Wofford', 'Seton Hall', 'Kentucky', 'Abilene Chr']) == 1)

# Round 4 Constraints
m.addConstr(quicksum(x[i, 'Fourth Round'] for i in teams[0:16]) == 1)
m.addConstr(quicksum(x[i, 'Fourth Round'] for i in teams[16:32]) == 1)
m.addConstr(quicksum(x[i, 'Fourth Round'] for i in teams[32:48]) == 1)
m.addConstr(quicksum(x[i, 'Fourth Round'] for i in teams[48:64]) == 1)

# Round 5 Constraints
m.addConstr(quicksum(x[i, 'Fifth Round'] for i in teams[0:32]) == 1)
m.addConstr(quicksum(x[i, 'Fifth Round'] for i in teams[32:64]) == 1)

# Round 6 Constraints
m.addConstr(quicksum(x[i, 'Sixth Round'] for i in teams) == 1)

# Elimination Constraints
m.addConstrs(quicksum(x[i, k] for k in rounds[1:6]) <= 5*x[i, "First Round"] for i in teams)
m.addConstrs(quicksum(x[i, k] for k in rounds[2:6]) <= 4*x[i, "Second Round"] for i in teams)
m.addConstrs(quicksum(x[i, k] for k in rounds[3:6]) <= 3*x[i, "Third Round"] for i in teams)
m.addConstrs(quicksum(x[i, k] for k in rounds[4:6]) <= 2*x[i, "Fourth Round"] for i in teams)
m.addConstrs(quicksum(x[i, k] for k in rounds[5:6]) <= x[i, "Fifth Round"] for i in teams)



#Run optimization and print results
m.optimize()

for v in m.getVars():
   print("%s %g" % (v.varName, v.x))




