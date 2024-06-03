import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

cxData = pd.read_json('data/cxData.json', lines=False)
dhData = pd.read_json('data/dhData.json', lines=False)
runData = pd.read_json('data/runData.json', lines=False)
bikeData = pd.read_json('data/bikeData.json', lines=False)
canoeData = pd.read_json('data/canoeData.json', lines=False)
cycleXData = pd.read_json('data/cyclexData.json', lines=False)
kayakData = pd.read_json('data/kayakData.json', lines=False)

zeroTime = datetime.strptime('00:00:00.0', '%H:%M:%S.%f')

class Team:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def setDivision(self, division):
        self.division = division

    def cxLeg(self, cxTime, fin):
        self.cxTime = cxTime
        self.cxFin = fin

    def dhLeg(self, dhTime, fin):
        self.dhTime = dhTime
        self.dhFin = fin
    
    def runLeg(self, runTime, fin):
        self.runTime = runTime
        self.runFin = fin
    
    def bikeLeg(self, bikeTime, fin):
        self.bikeTime = bikeTime
        self.bikeFin = fin
    
    def canoeLeg(self, canoeTime, fin):
        self.canoeTime = canoeTime
        self.canoeFin = fin
    
    def cycleXLeg(self, cyclexTime, fin):
        self.cyclexTime = cyclexTime
        self.cycloFin = fin
    
    def kayakLeg(self, kayakTime, fin):
        self.kayakTime = kayakTime
        self.kayakFin = fin

    def totalTimes(self):
        self.cxClock = self.cxTime
        self.dhClock = self.dhTime - zeroTime + self.cxClock
        self.runClock = self.runTime - zeroTime + self.dhClock
        self.bikeClock = self.bikeTime - zeroTime + self.runClock
        self.canoeClock = self.canoeTime - zeroTime + self.bikeClock
        self.cycloClock = self.cyclexTime - zeroTime + self.canoeClock
        self.kayakClock = self.kayakTime - zeroTime + self.cycloClock
        self.totalTime = self.kayakClock
        self.totalFinish = self.cxFin + self.dhFin + self.runFin + self.bikeFin + self. canoeFin + self.cycloFin + self.kayakFin
        self.legTimes = [self.cxClock, self.dhClock, self.runClock, self.bikeClock, self.canoeClock, self.cycloClock, self.kayakClock]


def formatTime(item):
    if ":" in item[:2]:
        time = datetime.strptime(item, '%H:%M:%S.%f')
    else:
        item = '00:' + item
        time = datetime.strptime(item, '%H:%M:%S.%f')
    return time


teams = []
for idx, item in runData.iterrows():
    team = Team(item['teamName'], item['teamNum'])
    team.cxLeg(formatTime('00:00.0'), 0)
    team.dhLeg(formatTime('00:00.0'), 0)
    team.runLeg(formatTime('00:00.0'), 0)
    team.bikeLeg(formatTime('00:00.0'), 0)
    team.canoeLeg(formatTime('00:00.0'), 0)
    team.cycleXLeg(formatTime('00:00.0'), 0)
    team.kayakLeg(formatTime('00:00.0'), 0)
    teams.append(team)

for idx, item in cxData.iterrows():
    for team in teams:
        if team.number == item['teamNum']:
            if item['time'] != 0:
                time = formatTime(item['time'])
                team.cxLeg(time, 1)
            else:
                time = formatTime('00:00:00.0')
                team.cxLeg(time, 0)
            if item['division'] != '':
                team.setDivision(item['division'])

for idx, item in dhData.iterrows():
    for team in teams:
        if team.number == item['teamNum']:
            if item['time'] != 0:
                time = formatTime(item['time'])
                team.dhLeg(time, 1)
            else:
                time = formatTime('00:00:00.0')
                team.cxLeg(time, 0)
            if item['division'] != '':
                team.setDivision(item['division'])

for idx, item in runData.iterrows():
    for team in teams:
        if team.number == item['teamNum']:
            if item['time'] != 0:
                time = formatTime(item['time'])
                team.runLeg(time, 1)
            else:
                time = formatTime('00:00:00.0')
                team.cxLeg(time, 0)
            if item['division'] != '':
                team.setDivision(item['division'])

for idx, item in bikeData.iterrows():
    for team in teams:
        if team.number == item['teamNum']:
            if item['time'] != 0:
                time = formatTime(item['time'])
                team.bikeLeg(time, 1)
            else:
                time = formatTime('00:00:00.0')
                team.cxLeg(time, 0)
            if item['division'] != '':
                team.setDivision(item['division'])

for idx, item in canoeData.iterrows():
    for team in teams:
        if team.number == item['teamNum']:
            if item['time'] != 0:
                time = formatTime(item['time'])
                team.canoeLeg(time, 1)
            else:
                time = formatTime('00:00:00.0')
                team.cxLeg(time, 0)
            if item['division'] != '':
                team.setDivision(item['division'])

for idx, item in cycleXData.iterrows():
    for team in teams:
        if team.number == item['teamNum']:
            if item['time'] != 0:
                time = formatTime(item['time'])
                team.cycleXLeg(time, 1)
            else:
                time = formatTime('00:00:00.0')
                team.cxLeg(time, 0)
            if item['division'] != '':
                team.setDivision(item['division'])

for idx, item in kayakData.iterrows():
    for team in teams:
        if team.number == item['teamNum']:
            if item['time'] != 0:
                time = formatTime(item['time'])
                team.kayakLeg(time, 1)
            else:
                time = formatTime('00:00:00.0')
                team.cxLeg(time, 0)
            if item['division'] != '':
                team.setDivision(item['division'])

for team in teams:
    team.totalTimes()
teams.sort(key=lambda x:x.totalTime, reverse=False)

finishingTeams = []
for team in teams:
    if team.totalFinish == 7:
        finishingTeams.append(team)
finishingTeams.sort(key=lambda x:x.totalTime, reverse=False)

cxTimes = sorted(finishingTeams, key=lambda x:x.cxTime, reverse=False)
dhTimes = sorted(finishingTeams, key=lambda x:x.dhTime, reverse=False)
runTimes = sorted(finishingTeams, key=lambda x:x.runTime, reverse=False)
bikeTimes = sorted(finishingTeams, key=lambda x:x.bikeTime, reverse=False)
canoeTimes = sorted(finishingTeams, key=lambda x:x.canoeTime, reverse=False)
cycloTimes = sorted(finishingTeams, key=lambda x:x.cyclexTime, reverse=False)
kayakTimes = sorted(finishingTeams, key=lambda x:x.kayakTime, reverse=False)


recMixedTeams = []
for team in finishingTeams:
    if team.division == 'Recreational Mixed':
        recMixedTeams.append(team)
recMixedTeams.sort(key=lambda x:x.totalTime, reverse=False)
        
cxRMTimes = sorted(recMixedTeams, key=lambda x:x.cxTime, reverse=False)
dhRMTimes = sorted(recMixedTeams, key=lambda x:x.dhTime, reverse=False)
runRMTimes = sorted(recMixedTeams, key=lambda x:x.runTime, reverse=False)
bikeRMTimes = sorted(recMixedTeams, key=lambda x:x.bikeTime, reverse=False)
canoeRMTimes = sorted(recMixedTeams, key=lambda x:x.canoeTime, reverse=False)
cycloRMTimes = sorted(recMixedTeams, key=lambda x:x.cyclexTime, reverse=False)
kayakRMTimes = sorted(recMixedTeams, key=lambda x:x.kayakTime, reverse=False)

def getPlace(data):
    for idx, team in enumerate(data):
        if team.number == 340:
            print(len(data), idx)


getPlace(cxTimes)
getPlace(dhTimes)
getPlace(runTimes)
getPlace(bikeTimes)
getPlace(canoeTimes)
getPlace(cycloTimes)
getPlace(kayakTimes)

print('')
getPlace(cxRMTimes)
getPlace(dhRMTimes)
getPlace(runRMTimes)
getPlace(bikeRMTimes)
getPlace(canoeRMTimes)
getPlace(cycloRMTimes)
getPlace(kayakRMTimes)

print('')
getPlace(finishingTeams)
getPlace(recMixedTeams)


def avgTime(data, source):
    avg = zeroTime
    for team in source:
        avg = avg - zeroTime + getattr(team, data)
    avg = avg - zeroTime
    avgSeconds = avg.total_seconds()
    avgTime = timedelta(seconds=(avgSeconds / len(source)))
    return avgTime

cxAvg = avgTime('cxTime', finishingTeams)
dhAvg = avgTime('dhTime', finishingTeams)
runAvg = avgTime('runTime', finishingTeams)
bikeAvg = avgTime('bikeTime', finishingTeams)
canoeAvg = avgTime('canoeTime', finishingTeams)
cycloAvg = avgTime('cyclexTime', finishingTeams)
kayakAvg = avgTime('kayakTime', finishingTeams)

overallAvgClockTime = [
    cxAvg,
    cxAvg + dhAvg,
    runAvg + dhAvg + cxAvg,
    bikeAvg + runAvg + dhAvg + cxAvg,
    canoeAvg + bikeAvg + runAvg + dhAvg + cxAvg,
    cycloAvg + canoeAvg + bikeAvg + runAvg + dhAvg + cxAvg,
    kayakAvg + cycloAvg + canoeAvg + bikeAvg + runAvg + dhAvg + cxAvg
]
overallAvgClockTimeFloats = []
for item in overallAvgClockTime:
    overallAvgClockTimeFloats.append(float(item.total_seconds()))
print(overallAvgClockTimeFloats)


RMcxAvg = avgTime('cxTime', recMixedTeams)
RMdhAvg = avgTime('dhTime', recMixedTeams)
RMrunAvg = avgTime('runTime', recMixedTeams)
RMbikeAvg = avgTime('bikeTime', recMixedTeams)
RMcanoeAvg = avgTime('canoeTime', recMixedTeams)
RMcycloAvg = avgTime('cyclexTime', recMixedTeams)
RMkayakAvg = avgTime('kayakTime', recMixedTeams)

rmAvgClockTime = [
    RMcxAvg,
    RMcxAvg + RMdhAvg,
    RMrunAvg + RMdhAvg + RMcxAvg,
    RMbikeAvg + RMrunAvg + RMdhAvg + RMcxAvg,
    RMcanoeAvg + RMbikeAvg + RMrunAvg + RMdhAvg + RMcxAvg,
    RMcycloAvg + RMcanoeAvg + RMbikeAvg + RMrunAvg + RMdhAvg + RMcxAvg,
    RMkayakAvg + RMcycloAvg + RMcanoeAvg + RMbikeAvg + RMrunAvg + RMdhAvg + RMcxAvg
]
rmAvgClockTimeFloats = []
for item in rmAvgClockTime:
    rmAvgClockTimeFloats.append(float(item.total_seconds()))
print(rmAvgClockTimeFloats)

print('')
print(cxAvg)
print((cxAvg + dhAvg).total_seconds())
print(dhAvg)
print(runAvg)
print(bikeAvg)
print(canoeAvg)
print(cycloAvg)
print(kayakAvg)

print('')
print('Test')
print(RMcxAvg)
print(RMdhAvg)
print(RMrunAvg)
print(RMbikeAvg)
print(RMcanoeAvg)
print(RMcycloAvg)
print(RMkayakAvg)

print('')

wbLegTimeFlots = []
for time in finishingTeams[375].legTimes:
    wbLegTimeFlots.append(float((time - zeroTime).total_seconds()))


def secondsConvert(target, color, z, linewidth):
    timeSeconds = []
    for time in target:
        if type(time) == datetime:
            timeSeconds.append((time - zeroTime).total_seconds())
        elif type(time) == timedelta:
            timeSeconds.append(time.total_seconds())
    plt.plot(
        range(len(target)),
        target,
        color = color,
        linewidth = linewidth,
        zorder = z
    )

'''
for team in finishingTeams:
    if team.number == 340:
        secondsConvert(team.legTimes, 'red', 3, 2)
    else:
        secondsConvert(team.legTimes, 'gray', 1, 0.25)
'''

'''
for team in recMixedTeams:
    if team.number == 340:
        secondsConvert(team.legTimes, 'red', 3, 2)
    else:
        secondsConvert(team.legTimes, 'gray', 1, 0.25)
'''

for time in overallAvgClockTimeFloats:
    plt.plot(
        range(len(overallAvgClockTimeFloats)),
        overallAvgClockTimeFloats,
        color ='blue',
        linewidth = '1'
    )

for time in rmAvgClockTimeFloats:
    plt.plot(
        range(len(rmAvgClockTimeFloats)),
        rmAvgClockTimeFloats,
        color ='orange',
        linewidth = '1'
    )

for time in wbLegTimeFlots:
    plt.plot(
        range(len(wbLegTimeFlots)),
        wbLegTimeFlots,
        color ='red',
        linewidth = '1'
    )
'''
'''

plt.grid(True)
plt.show()

