import requests
import json


class airQuality():
    def __init__(self,url:str=None) -> None:
        self._url: str = 'https://www.airquality.dli.mlsi.gov.cy/all_stations_data_PM'
        self.stations = ['station_7', 'station_1', 'station_3', 'station_5']
        self.limits = {
            'pollutant_5': [50, 100, 200],  # PM10
            'pollutant_6001': [25, 50, 100],  # PM25
            'pollutant_7': [100, 140, 180],  # O3
            'pollutant_8': [100, 150, 200],  # NO2
            'pollutant_1': [150, 250, 350],  # SO2
            'pollutant_10': [7000, 15000, 20000],  # CO
            'pollutant_20': [5, 10, 15]  # C6H6
        }
        self.limitRanges = ['Low', 'Moderate 🟨', 'High 🟧', 'Very High 🟥']
 

    def getData(self) -> dict:
        
        data = json.loads(requests.get(self._url).content)
        if data:
            return data
        else:
            return False

    def getTweet(self, results_dict: dict):
        if results_dict:
            results = []
            for stationName in results_dict:
                tweetPart = f'{stationName}:'
                for pollutantName in results_dict[stationName]:
                    tweetPart = f"{tweetPart}\n{pollutantName}: {results_dict[stationName][pollutantName]['value']}, {results_dict[stationName][pollutantName]['level']}"
                results.append(tweetPart)
            results = '\n\n'.join(results)
            tweet = f'⚠️ #WARNING #AIRQUALITY ⚠️\n{results}\n\nΠηγή TEE - Κλάδος Ποιότητας αέρα 👉 https://www.airquality.dli.mlsi.gov.cy/ '
            return tweet
        else:
            return False

    def checkPollutants(self, data):
        results = {}
        for station in data['data']:
            if station in self.stations:
                stationName = data['data'][station]['name_el'].split()[0]
                for pollutant in data['data'][station]['pollutants']:
                    if pollutant in self.limits.keys():
                        pollutantName = data['data'][station]['pollutants'][pollutant]['notation']
                        level = self.compareValue(float(data['data'][station]['pollutants'][pollutant]['value']),
                                                  pollutant)
                        if level != "Low" and level != "Moderate 🟨":
                            if stationName not in results.keys():
                                results[data['data'][station]['name_el'].split()[0]] = {}
                            if pollutantName not in results[stationName].keys():
                                results[stationName][pollutantName] = {}
                            results[stationName][pollutantName][
                                'value'] = f"{round(float(data['data'][station]['pollutants'][pollutant]['value']))} μg/m³"
                            results[stationName][pollutantName]['level'] = level
        if results != {}:
            return results
        else:
            return False

    def compareValue(self, value: float, pollutant: str) -> str:
        if pollutant in self.limits.keys():
            for i in range(len(self.limits[pollutant])):
                if value > self.limits[pollutant][i] and i == len(self.limits[pollutant]):
                    return (self.limitRanges[-1])
                elif value < self.limits[pollutant][i]:
                    return (self.limitRanges[i])

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self,url:str):
        self._url=url
