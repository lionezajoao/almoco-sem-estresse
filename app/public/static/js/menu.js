document.addEventListener("DOMContentLoaded", async function() {
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

    const mainPlate = await retrieveMainPlate(jwt);
    const salad = await retrieveSalad(jwt);
    const garrison = await retrieveGarrison(jwt);
    const followUp = await retrieveFollowUp(jwt);
    const subscribeButton = document.getElementById("add-menu-button");

    document.getElementById("logout-button").addEventListener("click", function() {
        sessionStorage.removeItem("jwt");
        window.location.href = "/login";
    });

    addFormFields(document.getElementById("card-container").querySelector('.card'), mainPlate, salad, garrison, followUp);

    let boxCount = 0; // Counter for the number of summary boxes
    let selectedMenus = []; // Array to store the selected menus
    let weekMenu = [];
    let weekChoice;

    document.getElementById("add-week-button").addEventListener("click", function() {
        weekChoice = document.getElementById("week-selector").value;
        const weekDay = document.getElementById("week-day").value;

        if (weekChoice && weekDay) { // Check if weekChoice and weekDay are not empty
            if (boxCount < 5) { // Check if the maximum number of boxes has been reached
                const weekday = handleWeekDay(weekDay);
                const mainDish = document.getElementById("main-dish").value;
                const salad = document.getElementById("salad").value;
                const sideDish = document.getElementById("side-dish").value;
                const accompaniment = document.getElementById("accompaniment").value;

                // Create a new menu object
                const menu = {
                    weekday: weekDay,
                    main_dish: mainDish,
                    salad: salad,
                    side_dish: sideDish,
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
                        <p>Guarnição: ${sideDish}</p>
                        <p>Acompanhamento: ${accompaniment}</p>
                        <button class="delete-button">Remover</button>
                    </div>
                `;

                // Set the content as the innerHTML of the box
                contentBox.innerHTML = content;

                // Append the box to the summary container
                document.getElementById("boxes-container").appendChild(contentBox);
                subscribeButton.style.display = "block";
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
                document.getElementById("side-dish").value = "";
                document.getElementById("accompaniment").value = "";

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
            } else {
                console.log("Maximum number of summary boxes reached.");
            }
        } else {
            console.log("Week choice and weekday are required to add a box.");
        }
    });
    
    document.getElementById("add-menu-button").addEventListener("click", function() {
        console.log(weekMenu);

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
                alert("Criando menu, aguarde...");
                const response = await fetch("/menu/create_menu", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "token": jwt,
                    },
                    body: JSON.stringify({ data: selectedMenus })
                });

                if (response.ok) {
                    console.log("Menu added successfully!");
                    alert("Menu enviado para o e-mail cadastrado!");
                    

                    // Clear the summary boxes
                    document.getElementById("boxes-container").innerHTML = "";
                    boxCount = 0;
                    subscribeButton.style.display = "none";

                    // Clear the selectedMenus array
                    selectedMenus = [];

                    // Reload the page
                    location.reload();
                } else {
                    console.log("Failed to add menu.");
                }
            } catch (error) {
                console.error("An error occurred while adding the menu:", error);
            }
        } else {
            console.log("No menus to add.");
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


async function retrieveMainPlate(token) {
    const data = await fetch(`/menu/get_item_by_type?type=Prato principal`, {
        headers: { token }
    });
    const mainPlate = await data.json();
    return mainPlate;
}

async function retrieveSalad(token) {
    const data = await fetch(`/menu/get_item_by_type?type=Salada`, {
        headers: { token }
    });
    const salad = await data.json();
    return salad;
}

async function retrieveGarrison(token) {
    const data = await fetch(`/menu/get_item_by_type?type=Guarnição`, {
        headers: { token }
    });
    const garrison = await data.json();
    return garrison;
}

async function retrieveFollowUp(token) {
    const data = await fetch(`/menu/get_item_by_type?type=Acompanhamento`, {
        headers: { token }
    });
    const followUp = await data.json();
    return followUp;
}

function addFormFields(formElement, mainPlate, salad, garrison, followUp) {
    const fieldData = [
        { id: 'main-dish', data: mainPlate },
        { id: 'salad', data: salad },
        { id: 'side-dish', data: garrison },
        { id: 'accompaniment', data: followUp }
    ];

    fieldData.forEach(field => {
        const select = formElement.querySelector(`#${field.id}`);
        if (select) {
            if (Array.isArray(field.data)) {
                field.data.forEach(option => {
                    const optionElement = document.createElement("option");
                    optionElement.value = option;
                    optionElement.text = option;
                    select.appendChild(optionElement);
                });
            } else {
                console.error("Field data is not an array:", field.data);
            }
        } else {
            console.error(`Select element with id '${field.id}' not found.`);
        }
    });
}
