

document.addEventListener("DOMContentLoaded", async function() {

    document.getElementById("logout-button").addEventListener("click", function() {
        sessionStorage.removeItem("jwt");
        window.location.href = "/login";
    });

    const jwt = sessionStorage.getItem("jwt");
    if (!jwt) {
        window.location.href = "/login";
    }
    
    const userData = await fetch("/auth/verify_token", {
        headers: {
            "Content-Type": "application/json",
            "token": jwt
        }
    })
    .then(response => response.json())

    if (!userData.success) {
        sessionStorage.removeItem("jwt");
        window.location.href = "/login";
    }

    const userRole = userData.role;

    if (userRole == "admin") {
        document.getElementById("admin-button").style.display = "block";
    }
    document.getElementById("admin-button").addEventListener("click", function() {
        window.location.href = "/admin";
    });

    const { mainPlate, salad, accompaniment } = handleItemsData(await getItems(jwt));
    const subscribeButton = document.getElementById("add-menu-button");

    addFormFields(document.getElementById("card-container").querySelector('.card'), mainPlate, salad, accompaniment);

    let boxCount = 0; // Counter for the number of summary boxes
    let selectedMenus = []; // Array to store the selected menus
    let weekMenu = [];
    let weekChoice;

    document.getElementById("add-week-button").addEventListener("click", function() {
        
        weekChoice = document.getElementById("week-selector").value;
        const weekDay = document.getElementById("week-day").value;

        if (!weekChoice) {
            showCustomNotification("Erro", "Selecione uma semana.", false);
            return;
        }

        if (!weekDay) {
            showCustomNotification("Erro", "Selecione um dia da semana.", false);
            return;
        }

        if (boxCount < 5) {
            const weekday = handleWeekDay(weekDay);
            const mainDish = document.getElementById("main-dish").value;
            const salad = document.getElementById("salad").value;
            const accompanimentList = document.querySelectorAll("#accompaniment");
            const accompaniment = Array.from(accompanimentList)
                .filter(select => select.value !== "")
                .map(select => select.value)
                .filter((value, index, self) => self.indexOf(value) === index);

            // Create a new menu object
            const menu = {
                weekday: weekDay,
                main_dish: mainDish,
                salad: salad,
                accompaniment: accompaniment
            };

            // Create a new box
            const contentBox = document.createElement("div");
            contentBox.classList.add("summary-box");

            // Create the content for the box
            let content = `
                <div class="content-item">
                    <p>Semana: ${weekChoice}</p>
                    <p>Dia da semana: ${weekday}</p>
                    <p>Prato Principal: ${mainDish}</p>
                    <p>Salada: ${salad}</p>
                    <p>Acompanhamentos: ${accompaniment}</p>
                    <button class="delete-button">Remover</button>
                </div>
            `;

            // Set the content as the innerHTML of the box
            contentBox.innerHTML = content;

            // Append the box to the summary container
            document.getElementById("boxes-container").appendChild(contentBox);
            subscribeButton.style.display = "block";
            document.getElementById("menu-button-label").style.display = "block";
            document.getElementById("end-request").style.display = "none";
            const weekDaySelect = document.getElementById("week-day");
            const selectedOption = weekDaySelect.querySelector(`option[value="${weekDay}"]`);
            selectedOption.remove();

            // Add event listener to delete button
            const deleteButton = contentBox.querySelector(".delete-button");
            deleteButton.addEventListener("click", function() {
                contentBox.remove();
                boxCount--; // Decrease the box count when a box is removed
                if (boxCount === 0) {
                    subscribeButton.style.display = "none";
                    document.getElementById("menu-button-label").style.display = "none";
                    document.getElementById("end-request").style.display = "block";
                }

                // Return the week day to the dropdown menu
                const optionElement = document.createElement("option");
                optionElement.value = weekDay;
                optionElement.text = handleWeekDay(weekDay);
                document.getElementById("week-day").appendChild(optionElement);
            });

            boxCount++; // Increase the box count when a box is added

            // Clear the form fields
            document.getElementById("main-dish").value = "";
            document.getElementById("salad").value = "";
            Array.from(document.querySelectorAll("#accompaniment")).forEach(select => select.value = "");

            // Find the week menu object for the selected week choice
            let weekMenuObj = weekMenu.find(obj => obj.week_choice === weekChoice);

            // If the week menu object does not exist, create a new one
            if (!weekMenuObj) {
                weekMenuObj = {
                    week_choice: weekChoice,
                    data: []
                };
                weekMenu.push(weekMenuObj);
            }

            // Add the menu object to the week menu data
            weekMenuObj.data.push(menu);
        }
    });
    
    document.getElementById("add-menu-button").addEventListener("click", function() {

        document.getElementById("week-selector").querySelector(`option[value="${weekChoice}"]`).remove();
        const weekDays = ["mon", "tue", "wed", "thu", "fri"];

        weekDays.forEach(day => {
            const weekDaySelect = document.getElementById("week-day");
            const existingOption = weekDaySelect.querySelector(`option[value="${day}"]`);
            if (!existingOption) {
                const optionElement = document.createElement("option");
                optionElement.value = day;
                optionElement.text = handleWeekDay(day);
                weekDaySelect.appendChild(optionElement);
            }
        });
        
        document.getElementById("boxes-container").innerHTML = "";
        boxCount = 0;
        subscribeButton.style.display = "none";
        document.getElementById("menu-button-label").style.display = "none";
        document.getElementById("end-request").style.display = "block";

        selectedMenus.push(...weekMenu);
        weekMenu = [];

        selectedMenus.forEach((week, index) => {
            const weekElement = document.getElementById(`week-${week.week_choice}-complete`);
            weekElement.textContent = `Semana ${week.week_choice}: ✓`;
        });
    });

    // Add button and code to submit the menu to the backend
    document.getElementById("finish-button").addEventListener("click", async function() {
        if (selectedMenus.length > 0) {
            try {
                showCustomNotification("Criando menu, aguarde...", null, true);
                const response = await fetch("/menu/create_menu", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "token": jwt,
                    },
                    body: JSON.stringify({ data: selectedMenus })
                });

                if (response.ok) {
                    showCustomNotification("Sucesso!", "Cardápio enviado para o e-mail cadastrado! Verifique a caixa de spam caso não apareça diretamente na sua caixa de entrada", true, 5000);
                    
                    document.getElementById("boxes-container").innerHTML = "";
                    boxCount = 0;
                    subscribeButton.style.display = "none";
                    document.getElementById("menu-button-label").style.display = "none";
                    document.getElementById("end-request").style.display = "block";

                    selectedMenus = [];

                    setTimeout(() => {
                        window.location.reload();
                    }, 5000);
                } else {
                    showCustomNotification("Erro ao adicionar menu.", "Entre em contato com os administradores do sistema.", false);
                }
            } catch (error) {
                console.error("An error occurred while adding the menu:", error);
            }
        }
    });
});

function showAlert(message) {
    const alertElement = document.createElement("div");
    alertElement.classList.add("alert");
    alertElement.textContent = message;
    document.body.appendChild(alertElement);
}

function handleWeekDay(weekDay) {
    switch (weekDay) {
        case "mon":
            return "Segunda-feira";
        case "tue":
            return "Terça-feira";
        case "wed":
            return "Quarta-feira";
        case "thu":
            return "Quinta-feira";
        case "fri":
            return "Sexta-feira";
        case "Segunda-feira":
            return "mon";
        case "Terça-feira":
            return "tue";
        case "Quarta-feira":
            return "wed";
        case "Quinta-feira":
            return "thu";
        case "Sexta-feira":
            return "fri";
        default:
            case "Invalid day":
    }
}

function updateWeekChecker(selectedMenus) {
    const weekComplete = {};

    // Find the maximum week number
    let maxWeek = 0;
    for (const week in selectedMenus) {
        const weekNumber = parseInt(week);
        if (weekNumber > maxWeek) {
            maxWeek = weekNumber;
        }
    }

    // Update UI accordingly
    for (let week = 1; week <= maxWeek; week++) {
        const weekElementId = `week-${week}-complete`;
        let weekElement = document.getElementById(weekElementId);
        if (!weekElement) {
            // Create the element if it does not exist
            weekElement = document.createElement("div");
            weekElement.id = weekElementId;
            // Add the weekElement to the sidebar or a specific location in your UI
        }

        weekElement.textContent = `Semana ${week}: ${selectedMenus[week] ? '✓' : ''}`;
    }
}

async function getItems(token) {
    const data = await fetch("/menu/get_all_items", {
        headers: { token }
    });
    const items = await data.json();
    return items;
}

function handleItemsData(items) {
    const mainPlate = [];
    const salad = [];
    const accompaniment = [];

    items.forEach(item => {
        if (item[1] === "Prato Principal") {
            mainPlate.push(item[0]);
        } else if (item[1] === "Saladas") {
            salad.push(item[0]);
        } else if (item[1] === "Acompanhamentos") {
            accompaniment.push(item[0]);
        }
    });

    return { mainPlate, salad, accompaniment };
}

function addFormFields(formElement, mainPlate, salad, accompaniment) {
    const fieldData = [
        { id: 'main-dish', data: mainPlate },
        { id: 'salad', data: salad },
        { id: 'accompaniment', data: accompaniment }
    ];

    fieldData.forEach(field => {
        if (Array.isArray(field.data)) {
            if (field.id == "accompaniment") { 
                const select = formElement.querySelectorAll(`#${field.id}`);
                select.forEach(select => {
                    field.data.forEach(option => {
                        const optionElement = document.createElement("option");
                        optionElement.value = option;
                        optionElement.text = option;
                        select.appendChild(optionElement);
                    });
                });
            } else {
                const select = formElement.querySelector(`#${field.id}`);
                field.data.forEach(option => {
                    const optionElement = document.createElement("option");
                    optionElement.value = option;
                    optionElement.text = option;
                    select.appendChild(optionElement);
                });
            }
        } else {
            console.error("Field data is not an array:", field.data);
        }
    });
}

function showCustomNotification(title, message, isSuccess, timeout=2000) {
    const container = document.getElementById('notification-container');

    // Creating the notification
    const notification = document.createElement('div');
    notification.classList.add('notification-box');

    // Setting the color based on success or error
    if (isSuccess) {
        notification.classList.add('success');
    } else {
        notification.classList.add('error');
    }

    // Close button
    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = '&times;';
    closeBtn.classList.add('close-btn');
    closeBtn.onclick = function() {
        container.removeChild(notification);
    };

    // Title
    const notifTitle = document.createElement('h4');
    notifTitle.textContent = title;

    // Message
    const notifMessage = document.createElement('p');
    notifMessage.textContent = message;

    // Building the notification
    notification.appendChild(closeBtn);
    notification.appendChild(notifTitle);
    notification.appendChild(notifMessage);

    // Adding the notification to the container
    container.appendChild(notification);

    // Auto remove the notification after 5 seconds
    setTimeout(() => {
        if (container.contains(notification)) {
            container.removeChild(notification);
        }
    }, timeout);
}
