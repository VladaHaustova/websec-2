let myData;
let currentUrl = '/rasp?groupId=531030143';
let currentWeek = "1";
let myDate = new Date();
let day = myDate.getDay();

fetch("/groups")
    .then((res) => {
        return res.json();
    })
    .then((data) => {
        console.log(data);
        let searchList = document.querySelector("#search-list");
        for (const [key, value] of Object.entries(data)) {
            let group = document.createElement("option");
            group.value = key;
            searchList.appendChild(group);
        }
        let inputElem = document.querySelector("#search-input");
        inputElem.addEventListener("change", () => {
            for (const [key, value] of Object.entries(data)) {
                let tmpTag = document.createElement("div");
                tmpTag.innerHTML = value;
                let tmpLink = tmpTag.querySelector("a");
                if (inputElem.value === key) {
                    updateData(tmpLink.href);
                    document.querySelector(".schedule-title").innerHTML = key;
                    break;
                }
            }
        })
    })

fetch("/teachers")
    .then((res) => {
        return res.json();
    })
    .then((data) => {
        console.log(data);
        let groupsList = document.querySelector("#search-list");
        for (const [key, value] of Object.entries(data)) {
            let group = document.createElement("option");
            group.value = key;
            groupsList.appendChild(group);
        }
        let inputElem = document.querySelector("#search-input");
        inputElem.addEventListener("change", () => {
            for (const [key, value] of Object.entries(data)) {
                let tmpLink = document.createElement("a");
                tmpLink.href = "#";
                if (inputElem.value === key) {
                    updateData(value);
                    document.querySelector(".schedule-title").innerHTML = key;
                    break;
                }
            }
        })
    })

function updateData(url = '/rasp?groupId=531030143') {
    fetch(url)
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            console.log(data);
            currentWeek = data["week"];
            currentWeek = currentWeek.slice(0, 3);
            currentWeek = currentWeek.replace(/\s/g, "");
            delete data["week"];
            myData = data;
            currentUrl += "&selectedWeek=" + currentWeek;
            generateTable();
        })
}

let rows = [];

function generateTable(changeDay = false, nextDay = false) {
    let table = document.querySelector('.schedule-table');
    table.innerHTML = "";
    let headers = table.insertRow();
    headers.classList.add("headers-row");
    rows = [];
    for (let i = 0; i < 6; i++) {
        rows.push(table.insertRow());
    }
    let resultSchedule = {};

    headers.insertCell().appendChild(document.createTextNode("Время"));
    if (changeDay) {
        nextDay ? (day === 6 ? day = 1 : day++) : (day === 1 ? day = 6 : day--);
    }
    if (window.screen.width < 481) {
        switch (day) {
            case 0:
                headers.insertCell().appendChild(document.createTextNode("Понедельник"));
                resultSchedule["monday"] = myData["monday"];
                break;
            case 1:
                headers.insertCell().appendChild(document.createTextNode("Понедельник"));
                resultSchedule["monday"] = myData["monday"];
                break;
            case 2:
                headers.insertCell().appendChild(document.createTextNode("Вторник"));
                resultSchedule["tuesday"] = myData["tuesday"];
                break;
            case 3:
                headers.insertCell().appendChild(document.createTextNode("Среда"));
                resultSchedule["wednesday"] = myData["wednesday"];
                break;
            case 4:
                headers.insertCell().appendChild(document.createTextNode("Четверг"));
                resultSchedule["thursday"] = myData["thursday"];
                break;
            case 5:
                headers.insertCell().appendChild(document.createTextNode("Пятница"));
                resultSchedule["friday"] = myData["friday"];
                break;
            case 6:
                headers.insertCell().appendChild(document.createTextNode("Суббота"));
                resultSchedule["saturday"] = myData["saturday"];
                break;
    
        }
    } else {
        headers.insertCell().appendChild(document.createTextNode("Понедельник"));
        headers.insertCell().appendChild(document.createTextNode("Вторник"));
        headers.insertCell().appendChild(document.createTextNode("Среда"));
        headers.insertCell().appendChild(document.createTextNode("Четверг"));
        headers.insertCell().appendChild(document.createTextNode("Пятница"));
        headers.insertCell().appendChild(document.createTextNode("Суббота"));
    }

    let ind = 0;
    for (let i of myData["monday"]) {
        rows[ind].insertCell().appendChild(document.createTextNode(Object.keys(i)[0] + ''));
        ind++;
    }

    ind = 0;
    for (const [key, value] of Object.entries(window.screen.width < 481 ? resultSchedule : myData)) {
        for (let i of value) {
            let day = document.createElement("div");
            day.innerHTML = value[ind][Object.keys(value[ind])[0]]
            rows[ind].insertCell().appendChild(day);
            ind++;
        }
        ind = 0;
    }

    let links = document.querySelectorAll("a");
    for (let link of links) {
        let hrefLink = link.href;
        link.href = "#";
        link.addEventListener("click", () => {
            currentUrl = hrefLink;
            updateData(currentUrl);
        })
    }
}

updateData();

window.addEventListener('resize', (event) => {
    for (let i = 0; i < rows.length; i++) {
        rows[i].innerHTML = "";
    }
    document.querySelector(".headers-row").innerHTML = "";
    generateTable();
});

document.querySelector("#nextWeek").addEventListener("click", () => {
    let isWeekSelectedInURL = false;
    let ind = 0;
    for (let char in currentUrl) {
        if (char === "&") {
            isWeekSelectedInURL = true;
            break;
        }
    }
})

function changePage(goNextPage) {
    let ind = 0;
    let count = 0;
    let previousBtn = document.querySelector("#previousWeek");
    for (let i = 0; i < currentUrl.length; i++) {
        if (currentUrl[i] === "=") {
            count++;
            if (count === 2) {
                ind = i;
                break;
            }
        }
    }
    if (goNextPage) currentWeek = parseInt(currentWeek) + 1 + "";
    else currentWeek = parseInt(currentWeek) - 1 + "";
    if (currentWeek === "1") {
        previousBtn.style.visibility = "hidden";
    } else {
        previousBtn.style.visibility = "visible";
    }
    currentUrl = currentUrl.slice(0, ind + 1) + currentWeek;
    updateData(currentUrl);
    console.log(currentUrl);
}