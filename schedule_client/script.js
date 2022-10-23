let myData;
let headers = document.querySelector(".headers-row");

fetch('http://127.0.0.1:2000/schedule.txt')
    .then((res) => {
        return res.json();
    })
    .then((data) => {
        console.log(data);
        myData = data;
        generateTable();
    })

let table = document.querySelector('.schedule-table');
let rows = [];
for (let i = 0; i < 6; i++) {
    rows.push(table.insertRow());
}

function generateTable(){
    let myDate = new Date();
    let day = myDate.getDay();
    let resultSchedule = {};

    headers.insertCell().appendChild(document.createTextNode("Время"));
    
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
            rows[ind].insertCell().appendChild(document.createTextNode(value[ind][Object.keys(value[ind])[0]]));
            ind++;
        }
        ind = 0;
    }  
}

window.addEventListener('resize', (event) => {
    for (let i = 0; i < rows.length; i++) {
        rows[i].innerHTML = "";
    }
    headers.innerHTML = "";
    generateTable();
});