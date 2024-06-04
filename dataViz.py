import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

teamData = pd.read_json('data/TeamData.json', lines=False)


def totalTimeLineChart():
    for idx, team in teamData.iterrows():
        times = []
        for idx, time in enumerate(team['cumulativeTimes']):
            time = (team['cumulativeTimes'][time])
            time/3_600_000
            times.append(time)
        plt.plot(
            range(len(times)),
            times,
            color = 'gray',
            linewidth = 0.25
        )
    plt.grid(True)
    plt.show() 

def legTimeLineChart():
    for idx, team in teamData.iterrows():
        times = []
        for idx, time in enumerate(team['legTimes']):
            time = (team['legTimes'][time])
            time = time/3_600_000
            times.append(time)
        plt.plot(
            range(len(times)),
            times,
            color = 'gray',
            linewidth = 0.25
        )
    plt.grid(True)
    plt.show() 

def LineChart(attr, timeScale, teamNumb):
    legs = [
        'cx',
        'dh',
        'run',
        'bike',
        'canoe',
        'cyclo',
        'kayak'
    ]

    avgTimes = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    baseAvgTimes = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    for idx, team in teamData.iterrows():
        for idx, time in enumerate(team[attr]):
            time = team[attr][time]
            if timeScale == 'minutes':
                time = time/60_000
            elif timeScale == 'hours':
                time = time/3_600_000
            elif timeScale == 'rank':
                time = time
            avgTimes[idx] += time


    for idx, time in enumerate(avgTimes):
        avgTimes[idx] = time / len(teamData)


    plt.plot(
        legs,
        avgTimes,
        color='red',
        linewidth = 2,
        zorder = 3,
        linestyle = 'dashed'
    )

    for idx, team in teamData.iterrows():
        times = []
        for idx, time in enumerate(team[attr]):
            time = (team[attr][time])
            if timeScale == 'minutes':
                time = time/60_000 
            elif timeScale == 'hours':
                time = time/3_600_000 
            elif timeScale == 'rank':
                time = time
            times.append(time)
        if team['teamNumber'] == teamNumb:
            plt.plot(
                legs,
                times,
                color = 'orangered',
                linewidth = 4,
                zorder = 3
            )
        elif team['division'] == 'Recreational Mixed':            
            plt.plot(
                legs,
                times,
                color = 'lightsalmon',
                linewidth = 1,
                zorder = 2
            )

        else:
            plt.plot(
                legs,
                times,
                color = 'gainsboro',
                linewidth = 0.25,
            )
    plt.xlabel('leg')
    plt.ylabel(timeScale)
    plt.title(attr)
    plt.grid(True)
    plt.show() 



#totalTimeLineChart()
#legTimeLineChart()
LineChart('legTimes', 'hours', 340)