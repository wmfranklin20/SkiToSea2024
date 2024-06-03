import pandas as pd
from datetime import datetime, timedelta
import numpy as np

'''
! runData is most complete list of teams and is run first to init as many teams as possible.

!! filter to check update total legs completed seems to be erroring, all teams are receiving 7 legs completed

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
        self.totalTeams = 0
        self.totalDivTeams = 0

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

        self.overallRank = 0
        self.divisionRank = 0


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
    def readJSON(targ, leg, team):
        for idx, item in targ.iterrows():
            if team.teamNumber == item['teamNum']:
                time = formatTime(item['time'])
                team.legTimes[leg] = time

    for team in Teams:
        totalTime = timedelta(0)

        readJSON(cxJSON, 'cx', team)
        readJSON(dhJSON, 'dh', team)
        readJSON(runJSON, 'run', team)
        readJSON(bikeJSON, 'bike', team)
        readJSON(canoeJSON, 'canoe', team)
        readJSON(cycleXJSON, 'cyclo', team)
        readJSON(kayakJSON, 'kayak', team)

        for x,y in team.legTimes.items():
            if type(y) == timedelta:
                totalTime += y
            else:
                totalTime += datetime.strptime('00:00:0.0', '%H:%M:%S.%f') - zeroTime
        team.totalTime = totalTime

initLegTimes()


def cumulativeTimes():
    for team in Teams:
        runningTimes = []
        runningTime = timedelta()
        legComplete = 0
        for x, y in team.legTimes.items():
            if y != 0:
                time = y
                runningTime += time
                runningTimes.append(runningTime)
                legComplete += 1
            else:
                time = datetime.strptime('00:00:0.0', '%H:%M:%S.%f') - zeroTime
                runningTime += time
                runningTimes.append(runningTime)
        team.totalLegs = legComplete
        for idx, x in enumerate(team.cumulativeTimes.keys()):
            team.cumulativeTimes[x] = runningTimes[idx]
cumulativeTimes()


def finishingTeams():
    finishingTeams = []
    for team in Teams:
        if team.totalLegs == 7:
            finishingTeams.append(team)
        else:
            pass
    return finishingTeams
finishingTeams()
finishingTeams = finishingTeams()

divisions = []
for team in finishingTeams:
    if team.division not in divisions:
        divisions.append(team.division)


def legRanking():

    def getRank(leg):
        teams = sorted(finishingTeams, key=lambda x:x.legTimes[leg], reverse=False)
        for team in finishingTeams:
            for idx, item in enumerate(teams):
                if team.teamNumber == item.teamNumber:
                    team.legOverallRank[leg] = idx + 1
            team.totalTeams = len(finishingTeams)

    getRank('cx')
    getRank('dh')
    getRank('run')
    getRank('bike')
    getRank('canoe')
    getRank('cyclo')
    getRank('kayak')

    def getRunningRank(leg):
        teams = sorted(finishingTeams, key=lambda x:x.cumulativeTimes[leg], reverse=False)
        for team in finishingTeams:
            for idx, item in enumerate(teams):
                if team.teamNumber == item.teamNumber:
                    team.cumulativeOverallRank[leg] = idx + 1
            team.totalTeams = len(finishingTeams)

    getRunningRank('cx')
    getRunningRank('dh')
    getRunningRank('run')
    getRunningRank('bike')
    getRunningRank('canoe')
    getRunningRank('cyclo')
    getRunningRank('kayak')

    def getDivRank(leg):
        for division in divisions:
            divTeams = []
            for team in finishingTeams:
                if team.division == division:
                    divTeams.append(team)
            divTeams.sort(key=lambda x:x.legTimes[leg], reverse=False)
            for team in finishingTeams:
                if team.division == division:
                    team.totalDivTeams = len(divTeams)
                for idx, item in enumerate(divTeams):
                    if team.teamNumber == item.teamNumber:
                        team.legDivisionRank[leg] = idx + 1

    getDivRank('cx')
    getDivRank('dh')
    getDivRank('run')
    getDivRank('bike')
    getDivRank('canoe')
    getDivRank('cyclo')
    getDivRank('kayak')

    def getDivRunningRank(leg):
        for division in divisions:
            divTeams = []
            for team in finishingTeams:
                if team.division == division:
                    divTeams.append(team)
            divTeams.sort(key=lambda x:x.cumulativeTimes[leg], reverse=False)
            for team in finishingTeams:
                if team.division == division:
                    team.totalDivTeams = len(divTeams)
                for idx, item in enumerate(divTeams):
                    if team.teamNumber == item.teamNumber:
                        team.cumulativeDivisionRank[leg] = idx + 1

    getDivRunningRank('cx')
    getDivRunningRank('dh')
    getDivRunningRank('run')
    getDivRunningRank('bike')
    getDivRunningRank('canoe')
    getDivRunningRank('cyclo')
    getDivRunningRank('kayak')

legRanking()

for team in finishingTeams:
    team.overallRank = team.cumulativeOverallRank['kayak']
    team.divisionRank = team.cumulativeDivisionRank['kayak']


finishingTeams.sort(key=lambda x:x.overallRank, reverse=False)
'''
for team in finishingTeams:
    if team.teamNumber == 340:
        print(team.teamName)
        print(team.teamNumber)
        print(team.division)
        print(team.totalTime)
        print(team.legOverallRank)
        print(team.cumulativeOverallRank)
        print(team.totalTeams)
        print(team.legDivisionRank)
        print(team.cumulativeDivisionRank)
        print(team.totalDivTeams)
        print('')
print(len(finishingTeams))
'''

def createJSON(data, path):
    objDicts = []
    for item in data:
        itemDict = item.__dict__
        objDicts.append(itemDict)

    df = pd.DataFrame(objDicts)
    jsonPath = path
    df.to_json(jsonPath, orient='records', indent=4)

createJSON(finishingTeams, 'data/TeamData.json')