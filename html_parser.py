import requests
from bs4 import BeautifulSoup
import json


def schedule_json(info, times, week):
    print(info)
    jsonn = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": []
    }
    ind = 7
    for i in range(len(times)):
        for day in jsonn:
            jsonn[day].append({times[i]: info[ind]})
            ind = ind + 1
    jsonn["week"] = week
    return jsonn

def getGroups():
    result = {}
    for i in range(1, 6):
        html = requests.get(url="https://ssau.ru/rasp/faculty/492430598?course=" + str(i)).text
        soup = BeautifulSoup(html, "lxml")  #
        find_all_groups = soup.find_all("a", class_="btn-text group-catalog__group")
        for j in find_all_groups:
            result[j.text.strip()] = str(j)
    print(result)
    return json.dumps(result)

def getHTML(url):
    resultUrl = 'https://ssau.ru' + url
    html = requests.get(url=resultUrl).text
    soup = BeautifulSoup(html, "lxml")

    info = []
    testTime = []
    find_all_subjects = soup.find_all("div", class_="schedule__item")
    find_all_times = soup.find_all("div", class_="schedule__time")
    for item in find_all_subjects:
        result = ""
        tmp = BeautifulSoup(str(item), "lxml")
        lesson_names = tmp.find_all("div", class_="body-text")
        for lesson in lesson_names:
            result += lesson.text
        places = tmp.find_all("div", class_="caption-text schedule__place")
        for place in places:
            result += place.text
        teachers_and_groups = tmp.find_all("a", class_="caption-text")
        for teacher_or_group in teachers_and_groups:
            result += str(teacher_or_group)
            result += "<br>"

        info.append(result)


    for item in find_all_times:
        testTime.append(item.text)

    currentWeek = ""
    for week in soup.find_all("span", class_="h3-text week-nav-current_week"):
        currentWeek = week.text

    return json.dumps(schedule_json(info, testTime, currentWeek))
