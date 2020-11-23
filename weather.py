import requests
import json
from datetime import datetime, timedelta, date
import csv
from sys import argv

url = "https://weather2020-weather-v1.p.rapidapi.com/zip/e8ecee8ff60c478f8a36280fea0524fe/02482"

headers = {
    "x-rapidapi-key": argv[1],
    # "x-rapidapi-key": "b773b77d47msh87e30978e201745p16f04ajsnf2e30f23932c",
    "x-rapidapi-host": "weather2020-weather-v1.p.rapidapi.com",
}

response = requests.get(url, headers=headers).text
a = json.loads(response)
today = date.today().strftime("%Y-%m-%d")
if len(argv) == 3:
    inputDate = datetime.strptime(argv[2], "%Y-%m-%d")
else:
    inputDate = datetime.strptime(today, "%Y-%m-%d")


def getWeatherData():
    with open("out.txt", "w", newline="", encoding="utf-8") as new_data_file:
        csv_writer = csv.writer(new_data_file)

        for data in a:
            timestampStart = datetime.fromtimestamp(data["startDate"])
            timestampEnd = timestampStart + timedelta(days=6)
            csv_writer.writerow(
                [
                    timestampStart.strftime("%Y-%m-%d"),
                    timestampEnd.strftime("%Y-%m-%d"),
                    data["conditions"][0]["tag"],
                ]
            )


def checkWeatherData():
    with open("out.txt", "r") as data_file:
        savedData = []
        weatherDates = csv.reader(data_file)
        for line in weatherDates:
            savedData.append(line)
        if savedData:
            if datetime.strptime(today, "%Y-%m-%d") > datetime.strptime(
                savedData[0][1], "%Y-%m-%d"):
                getWeatherData()
        else:
            getWeatherData()



checkWeatherData()

inRange = False
with open("out.txt", "r") as data_file:
    weatherDates = csv.reader(data_file)

    for line in weatherDates:
        if inputDate >= datetime.strptime(
            line[0], "%Y-%m-%d"
        ) and inputDate <= datetime.strptime(line[1], "%Y-%m-%d"):
            if "rain" in line[2]:
                print("Będzie padać")
                inRange = True
                break
            else:
                print("Nie będzie padać")
                inRange = True
                break
    if not inRange:
        print("Nie wiem")
