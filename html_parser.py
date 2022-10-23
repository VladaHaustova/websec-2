import requests
from bs4 import BeautifulSoup
import json
import codecs

html = requests.get(url='https://ssau.ru/rasp?groupId=531030143').text
soup = BeautifulSoup(html, "lxml")

def schedule_json(info, times):
    jsonn = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": []
    }
    ind = 6
    for i in range(len(times)):
        for day in jsonn:
            jsonn[day].append({times[i]: info[ind]})
            ind = ind + 1

    return jsonn

def getHTML():
    info = []
    testTime = []
    find_all_subjects = soup.find_all("div", class_="schedule__item")
    find_all_times = soup.find_all("div", class_="schedule__time")

    count = 0
    for item in find_all_subjects:
        info.append(item.text)
        count = count + 1
    for item in find_all_times:
        testTime.append(item.text)
        count = count + 1
    info.pop(0)

    with codecs.open("schedule_client/schedule.txt", "w", "utf-8") as stream:
        stream.write(json.dumps(schedule_json(info, testTime), ensure_ascii=False) + u"\n")