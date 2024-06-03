import pandas as pd
from datetime import datetime, timedelta
import numpy as np

'''
! runData is most complete list of teams and is run first to init as many teams as possible.

Dataframe:
- leg
- name
- position
- teamNum
- teamName
- division
- time

'''
cxJSON = pd.read_json('data/cxData.json', lines=False)
dhJSON = pd.read_json('data/dhData.json', lines=False)
runJSON = pd.read_json('data/runData.json', lines=False)
bikeJSON = pd.read_json('data/bikeData.json', lines=False)
canoeJSON = pd.read_json('data/canoeData.json', lines=False)
cycleXJSON = pd.read_json('data/cyclexData.json', lines=False)
kayakJSON = pd.read_json('data/kayakData.json', lines=False)


class Team:
    def __init__(self, teamName, teamNumber):
        self.teamName = teamName
        self.teamNumber = teamNumber
        self.division = '-'
        self.totalTime = timedelta(0)
        self.totalLegs = 0

        self.legTimes = {
            'cx': 0,
            'dh': 0,
            'run': 0,
            'bike': 0,
            'canoe': 0,
            'cyclo': 0,
            'kayak': 0
        }
        self.legOverallRank = {
            'cx': 0,
            'dh': 0,
            'run': 0,
            'bike': 0,
            'canoe': 0,
            'cyclo': 0,
            'kayak': 0
        }
        self.legDivisionRank = {
            'cx': 0,
            'dh': 0,
            'run': 0,
            'bike': 0,
            'canoe': 0,
            'cyclo': 0,
            'kayak': 0
        }

        self.cumulativeTimes = {
            'cx': 0,
            'dh': 0,
            'run': 0,
            'bike': 0,
            'canoe': 0,
            'cyclo': 0,
            'kayak': 0
        }
        self.cumulativeOverallRank = {
            'cx': 0,
            'dh': 0,
            'run': 0,
            'bike': 0,
            'canoe': 0,
            'cyclo': 0,
            'kayak': 0
        }
        self.cumulativeDivisionRank = {
            'cx': 0,
            'dh': 0,
            'run': 0,
            'bike': 0,
            'canoe': 0,
            'cyclo': 0,
            'kayak': 0
        }

        self.overallRank = self.cumulativeOverallRank['kayak']
        self.divisionRank = self.cumulativeDivisionRank['kayak']


def formatTime(item):
    if ":" in item[:2]:
        time = datetime.strptime(item, '%H:%M:%S.%f') - zeroTime
    else:
        item = '00:' + item
        time = datetime.strptime(item, '%H:%M:%S.%f') - zeroTime
    return time
zeroTime = datetime.strptime('00:00:00.0', '%H:%M:%S.%f')

###

Teams = []

def initTeams():
    for idx, item in runJSON.iterrows():
        team = Team(item['teamName'], item['teamNum'])
        Teams.append(team)
initTeams()

def initDivisions():
    for idx, team in enumerate(Teams):
        for idx, item in cxJSON.iterrows():
            if team.teamNumber == item['teamNum']:
                team.division = item['division']
        if team.division == '':
            for idx, item in dhJSON.iterrows():
                if team.teamNumber == item['teamNum']:
                    team.division = item['division']
        if team.division == '':
            for idx, item in bikeJSON.iterrows():
                if team.teamNumber == item['teamNum']:
                    team.division = item['division']
initDivisions()
    
def initLegTimes():
    for team in Teams:
        totTime = []
        totalTime = timedelta(0)
        for idx, item in cxJSON.iterrows():
            if team.teamNumber == item['teamNum']:
                time = formatTime(item['time'])
                team.legTimes['cx'] = time
                totTime.append(time)
                team.totalLegs += 1
        for idx, item in dhJSON.iterrows():
            if team.teamNumber == item['teamNum']:
                time = formatTime(item['time'])
                team.legTimes['dh'] = time
                totTime.append(time)
                team.totalLegs += 1
        for idx, item in runJSON.iterrows():
            if team.teamNumber == item['teamNum']:
                time = formatTime(item['time'])
                team.legTimes['run'] = time
                totTime.append(time)
                team.totalLegs += 1
        for idx, item in bikeJSON.iterrows():
            if team.teamNumber == item['teamNum']:
                time = formatTime(item['time'])
                team.legTimes['bike'] = time
                totTime.append(time)
                team.totalLegs += 1
        for idx, item in canoeJSON.iterrows():
            if team.teamNumber == item['teamNum']:
                time = formatTime(item['time'])
                team.legTimes['canoe'] = time
                totTime.append(time)
                team.totalLegs += 1
        for idx, item in cycleXJSON.iterrows():
            if team.teamNumber == item['teamNum']:
                time = formatTime(item['time'])
                team.legTimes['cyclo'] = time
                totTime.append(time)
                team.totalLegs += 1
        for idx, item in kayakJSON.iterrows():
            if team.teamNumber == item['teamNum']:
                time = formatTime(item['time'])
                team.legTimes['kayak'] = time
                totTime.append(time)
                team.totalLegs += 1
        for x,y in team.legTimes.items():
            if type(y) == timedelta:
                totalTime += y
            else:
                totalTime += datetime.strptime('00:00:0.0', '%H:%M:%S.%f') - zeroTime
        team.totalTime = totalTime

initLegTimes()

Teams.sort(key=lambda x:x.teamNumber, reverse=False)
for team in Teams:
    print(team.teamName)
    print(team.teamNumber)
    print(team.division)
    print(team.totalTime)
    print(team.totalLegs)
    print('')
print(len(Teams))
'''
'''
