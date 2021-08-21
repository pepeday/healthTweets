import requests
import xml.etree.ElementTree as et
from copy import copy

from requests.models import Response



class heatIndex:
    def __init__(self):
        
        self._url = "https://www.dom.org.cy/AWS/OpenData/CyDoM.xml"
        self._stationList = ['PAPHOS','LEFKOSIA','LIMASSOL','LCLK']
        self._observationNames = ['Air Temperature (1.2m)', 'Relative Humidity (1.2m)', 'Recom. Light Work Load',
                            'Recom. Medium Work Load', 'Recom. Heavy Work Load']
    
    def getResponse(self):
        if self._url:
            response = requests.get(self._url).content
            return self.dictify(et.fromstring(response))
        else:
            return False
    
    def getTweet(self, extractedValues:dict):
        values=[]
        for station in extractedValues.keys():
            if self.checkIfExceeding(extractedValues[station]):
                values.append(f'''{station}: {extractedValues[station]['Air Temperature (1.2m)']}°C / {extractedValues[station]['Relative Humidity (1.2m)']} %💧
🟨 {extractedValues[station]['Recom. Light Work Load']}% 🟧 {extractedValues[station]['Recom. Medium Work Load']}% 🟥 {extractedValues[station]['Recom. Heavy Work Load']}%''')
            text=f'''⚠️#WARNING #HEATINDEX ⚠️
Ψηλές Θερμοκρασίες 🌡️

{"""

""".join(values)}


Πηγή 👉 https://www.dom.org.cy/'''
        return text

    def dictify(self, r, root=True):
        if root:
            return {r.tag: self.dictify(r, False)}
        d = copy(r.attrib)
        if r.text:
            d["_text"] = r.text
        for x in r.findall("./*"):
            if x.tag not in d:
                d[x.tag] = []
            d[x.tag].append(self.dictify(x, False))
        return d

    def extractValues(self, retrievedData:dict, stationList: list, observationNames: list):
        resultsDict = {}
        for i in retrievedData['meteorology']['observations']:
            if i['station_code'][0]['_text'] in stationList:
                for j in i['observation']:
                    if j['observation_name'][0]['_text'] in observationNames:
                        if i['station_code'][0]['_text'] not in resultsDict.keys():
                            resultsDict[i['station_code'][0]['_text']] = {}
                        else:
                            pass
                        resultsDict[i['station_code'][0]['_text']][j['observation_name'][0]['_text']] = \
                        j['observation_value'][0]['_text']
        return resultsDict

    def checkIfAnyIsExceeding(self,extractedValues: dict) -> bool:
        allExceeding=False
        for station in extractedValues.keys():
            allExceeding = self.checkIfExceeding(extractedValues[station]) or allExceeding
        return allExceeding

    def checkIfExceeding(self, extractedStation: dict) -> bool:
        for observation in extractedStation.keys():
            if 'Recom.' in observation:
                if int(extractedStation[observation])<100:
                    return True
        return False

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self,url:str):
        self._url=url

    @property
    def stationList(self):
        return self._stationList

    @stationList.setter
    def stationList(self,stationList:list):
        self._stationList=stationList


    @property
    def observationNames(self):
        return self._observationNames

    @observationNames.setter
    def observationNames(self,observationNames:list):
        self._observationNames=observationNames