import pandas as pd
import datetime
import requests
import io
import tools

class covidCY:
    def __init__(self):
        csvDataUrl: str = "https://opendata.ecdc.europa.eu/covid19/vaccine_tracker/csv/data.csv"
        #self.csvFile = 'covidData.csv'
        self.data = requests.get(csvDataUrl).content


    def text(self) -> str:
        df = pd.read_csv(io.BytesIO(self.data), encoding='utf-8')
        #df = pd.read_csv(self.csvFile, encoding='utf-8')
        df = df[(df['Region'] == 'CY') & (df['TargetGroup'] == 'ALL')]

        population = df['Population'].iloc[-1]
        firstDose = (df['FirstDose'].sum())/population
        secondDose = (df['SecondDose'].sum())/population

        week = df['YearWeekISO'].iloc[-1]
        monday = datetime.datetime.strptime(week + '-1', '%G-W%V-%u') + datetime.timedelta(days=7)
        monday = monday.strftime('%d/%m/%Y')

        return f'''ℹ️ #INFO #COVID19 ℹ️
Ποσοστό του πληθυσμού που 💉 μέχρι τις {monday} στην 🇨🇾:
1η δόση: {tools.progressBar(firstDose)} {round(firstDose*100,1)}%
2η δόση: {tools.progressBar(secondDose)} {round(secondDose*100,1)}%
Πηγή 👉 https://data.europa.eu/data/datasets/covid-19-vaccine-tracker?locale=en'''