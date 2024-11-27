let employeesVacations = [];  // Список всех отпусков

// Добавление строки для нового сотрудника
function addEmployeeRow() {
    const tableBody = document.getElementById("tableBody");
    const rowId = employeesVacations.length + 1;
    const row = document.createElement("tr");
    row.innerHTML = `
        <td><input type="text" placeholder="Имя сотрудника"></td>
        <td><input type="date"></td>
        <td><input type="date"></td>
        <td><button onclick="addVacation(${rowId})">Добавить</button></td>
    `;
    tableBody.appendChild(row);
}

// Добавление отпуска для сотрудника
function addVacation(rowId) {
    const row = document.getElementById("tableBody").children[rowId - 1];
    const employee = row.cells[0].querySelector("input").value;
    const startDate = row.cells[1].querySelector("input").value;
    const endDate = row.cells[2].querySelector("input").value;

    if (!employee || !startDate || !endDate) {
        alert("Пожалуйста, заполните все поля.");
        return;
    }

    const start = new Date(startDate);
    const end = new Date(endDate);
    employeesVacations.push({ employee, start, end });

    saveVacationsLocally();  // Автосохранение данных без скачивания
    generateCalendar();  // Перерисовка календаря
}

// Сохранение данных в localStorage
function saveVacationsLocally() {
    const csvContent = "Сотрудник,Дата начала,Дата окончания\n" +
        employeesVacations.map(v => `${v.employee},${v.start.toLocaleDateString()},${v.end.toLocaleDateString()}`).join("\n");
    localStorage.setItem('vacationData', csvContent);  // Сохранение в localStorage
    alert("Данные успешно сохранены в localStorage.");
}

// Генерация календаря
function generateCalendar() {
    const calendarDiv = document.getElementById("calendar");
    calendarDiv.innerHTML = "";
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let day = 1; day <= daysInMonth; day++) {
        const dayDiv = document.createElement("div");
        dayDiv.classList.add("day");
        dayDiv.innerText = day;

        highlightVacations(day, dayDiv);
        calendarDiv.appendChild(dayDiv);
    }
}

// Подсветка дней, которые являются отпускными
function highlightVacations(day, dayDiv) {
    employeesVacations.forEach(vacation => {
        const start = vacation.start.getDate();
        const end = vacation.end.getDate();
        if (day >= start && day <= end) {
            dayDiv.classList.add("red");
        }
    });
}

// Формирование отчета для всех сотрудников или по отдельному сотруднику
function generateReport(employeeName = "") {
    const reportDiv = document.getElementById("report");
    reportDiv.innerHTML = "<h2>Отчет по отпускам</h2>";

    employeesVacations.forEach(vacation => {
        if (!employeeName || vacation.employee === employeeName) {
            const reportItem = document.createElement("p");
            reportItem.textContent = `${vacation.employee}: ${vacation.start.toLocaleDateString()} - ${vacation.end.toLocaleDateString()}`;
            reportDiv.appendChild(reportItem);
        }
    });
}

generateCalendar();
