document.addEventListener("DOMContentLoaded", async function() {
    const mainPlate = await retrieveMainPlate();
    const salad = await retrieveSalad();
    const garrison = await retrieveGarrison();
    const followUp = await retrieveFollowUp();
    const subscribeButton = document.getElementById("add-menu-button");

    addFormFields(document.getElementById("card-container").querySelector('.card'), mainPlate, salad, garrison, followUp);

    let boxCount = 0; // Counter for the number of summary boxes
    let selectedMenus = []; // Array to store the selected menus
    let menu = [];

    document.getElementById("add-week-button").addEventListener("click", function() {
        const weekChoice = document.getElementById("week-selector").value;
        const weekDay = document.getElementById("week-day").value;

        if (weekChoice && weekDay) { // Check if weekChoice and weekDay are not empty
            if (boxCount < 5) { // Check if the maximum number of boxes has been reached
                const weekday = handleWeekDay(weekDay);
                const mainDish = document.getElementById("main-dish").value;
                const salad = document.getElementById("salad").value;
                const sideDish = document.getElementById("side-dish").value;
                const accompaniment = document.getElementById("accompaniment").value;

                // Create a new menu object
                menu.push({
                    week_choice: weekChoice,
                    weekday: weekDay,
                    main_dish: mainDish,
                    salad: salad,
                    side_dish: sideDish,
                    accompaniment: accompaniment
                });

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

                    // Remove the menu from the selectedMenus array
                    selectedMenus = selectedMenus.filter(menu => menu.week_choice !== weekChoice && menu.weekday !== weekday);
                });

                boxCount++; // Increase the box count when a box is added

                // Clear the form fields
                document.getElementById("main-dish").value = "";
                document.getElementById("salad").value = "";
                document.getElementById("side-dish").value = "";
                document.getElementById("accompaniment").value = "";
            } else {
                console.log("Maximum number of summary boxes reached.");
            }
        } else {
            console.log("Week choice and weekday are required to add a box.");
        }
    });
    
    document.getElementById("add-menu-button").addEventListener("click", function() {

        
        const weekChoice = document.getElementById("week-selector").value;
        document.getElementById("week-selector").querySelector(`option[value="${weekChoice}"]`).remove();
        const weekDays = ["mon", "tue", "wed", "thu", "fri"];
        
        weekDays.forEach(day => {
            const optionElement = document.createElement("option");
            optionElement.value = day;
            optionElement.text = handleWeekDay(day);
            document.getElementById("week-day").appendChild(optionElement);
        });
        
        document.getElementById("boxes-container").innerHTML = "";
        boxCount = 0;
        subscribeButton.style.display = "none";

        selectedMenus.push(menu);

        updateWeekChecker(selectedMenus);

    });

    // Add button and code to submit the menu to the backend
    document.getElementById("finish-button").addEventListener("click", async function() {
        if (selectedMenus.length > 0) {
            try {
                const response = await fetch("/menu/create_menu", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(selectedMenus)
                });

                if (response.ok) {
                    console.log("Menu added successfully!");

                    // Clear the summary boxes
                    document.getElementById("boxes-container").innerHTML = "";
                    boxCount = 0;
                    subscribeButton.style.display = "none";

                    // Clear the selectedMenus array
                    selectedMenus = [];
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
        default:
            case "Invalid day":
    }
}

function updateWeekChecker(selectedMenus) {
    // Assuming you have 5 days in a week and you want to check if all days have been selected for a week
    const weekComplete = {
        '1': false,
        '2': false,
        '3': false,
        '4': false
    };

    // Check if all days for a week are selected
    selectedMenus.forEach(menuWeek => {
        if (menuWeek.length === 5) {
            weekComplete[menuWeek[0].week_choice] = true;
        }
    });

    // Update UI accordingly
    for (const week in weekComplete) {
        const weekElementId = `week-${week}-complete`;
        let weekElement = document.getElementById(weekElementId);
        if (!weekElement) {
            // Create the element if it does not exist
            weekElement = document.createElement("div");
            weekElement.id = weekElementId;
            // Add the weekElement to the sidebar or a specific location in your UI
        }

        weekElement.textContent = `Semana ${week}: ${weekComplete[week] ? '✓' : ''}`;
    }
}


async function retrieveMainPlate() {
    const data = await fetch(`/menu/get_item_by_type?type=Prato principal`);
    const mainPlate = await data.json();
    return mainPlate;
}

async function retrieveSalad() {
    const data = await fetch(`/menu/get_item_by_type?type=Salada`);
    const salad = await data.json();
    return salad;
}

async function retrieveGarrison() {
    const data = await fetch(`/menu/get_item_by_type?type=Guarnição`);
    const garrison = await data.json();
    return garrison;
}

async function retrieveFollowUp() {
    const data = await fetch(`/menu/get_item_by_type?type=Acompanhamento`);
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
