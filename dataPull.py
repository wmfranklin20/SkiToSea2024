import requests, string, json
from datetime import datetime
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd

cxURL = 'https://skitosea.pacificmultisports.com/results/2024/final#0_F4A330'
dhURL = 'https://skitosea.pacificmultisports.com/results/2024/final#0_CBE6EC'
runURL = 'https://skitosea.pacificmultisports.com/results/2024/final#0_B81135'
bikeURL = 'https://skitosea.pacificmultisports.com/results/2024/final#0_401157'
canoeURL = 'https://skitosea.pacificmultisports.com/results/2024/final#0_DB10DD'
cyclexURL = 'https://skitosea.pacificmultisports.com/results/2024/final#0_D2DD81'
kayakURL = 'https://skitosea.pacificmultisports.com/results/2024/final#0_EB0DBC'

class teamLeg:
    def __init__(self, leg, name, position, teamNum, teamName, division, time):
        self.leg = leg
        self.name = name
        self.position = position
        self.teamNum = teamNum
        self.teamName = teamName
        self.division = division
        self.time = time

def dataPull(url, leg):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=5)

    soup = BeautifulSoup(r.html.raw_html, 'html.parser')
    main = soup.find('table')
    rows = main.findAll(class_='Hover LastRecordLine')

    teams = []
    for idx, row in enumerate(rows):
        data = row.findAll('td')
        if len(data) == 8:
            place = idx + 1
            teamNum = int(data[2].text)
            name = data[3].text
            teamName = data[5].text
            division = ''
            time = data[6].text
        elif len(data) == 9:
            place = idx + 1
            teamNum = int(data[2].text)
            name = data[3].text
            teamName = data[5].text
            division = data[6].text
            time = data[7].text
        
        team = teamLeg(leg, name, place, teamNum, teamName, division, time)
        teams.append(team)

    return teams

def createJSON(data, path):
    objDicts = []
    for item in data:
        itemDict = item.__dict__
        objDicts.append(itemDict)

    df = pd.DataFrame(objDicts)
    jsonPath = path
    df.to_json(jsonPath, orient='records', indent=4)


cxTimes = dataPull(cxURL, 'CrossCountry Ski')
createJSON(cxTimes, 'cxData.json')    

dhTimes = dataPull(dhURL, 'Downhill Ski')
createJSON(dhTimes, 'dhData.json')    

runTimes = dataPull(runURL, 'Running')
createJSON(runTimes, 'runData.json')    

bikeTimes = dataPull(bikeURL, 'Road Bike')
createJSON(bikeTimes, 'bikeData.json')    

canoeTimes = dataPull(canoeURL, 'Canoe')
createJSON(canoeTimes, 'canoeData.json')    

cyclexTimes = dataPull(cyclexURL, 'Cyclocross')
createJSON(cyclexTimes, 'cyclexData.json')    

kayakTimes = dataPull(kayakURL, 'Kayak')
createJSON(kayakTimes, 'kayakData.json')    
'''
'''

