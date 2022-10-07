let myData;

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

function generateTable() {
    let ind = 0;
    for (let i of myData["monday"]) {
        rows[ind].insertCell().appendChild(document.createTextNode(Object.keys(i)[0] + ''));
        ind++;
    }

    ind = 0;
    for (const [key, value] of Object.entries(myData)) {
        for (let i of value) {
            rows[ind].insertCell().appendChild(document.createTextNode(value[ind][Object.keys(value[ind])[0]]));
            ind++;
        }
        ind = 0;
    }   
}


