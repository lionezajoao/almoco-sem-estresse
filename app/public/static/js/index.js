document.addEventListener("DOMContentLoaded", async function() {
    const mainPlate = await retrieveMainPlate();
    const salad = await retrieveSalad();
    const garrison = await retrieveGarrison();
    const followUp = await retrieveFollowUp();
    const subscribeButton = document.getElementById("submit-menu-button");

    addFormFields(document.getElementById("card-container").querySelector('.card'), mainPlate, salad, garrison, followUp);

    let boxCount = 0; // Counter for the number of summary boxes

    document.getElementById("add-menu-button").addEventListener("click", function() {
        const weekDay = document.getElementById("week-day").value;
        

        if (weekDay) { // Check if weekDay is not empty
            if (boxCount < 5) { // Check if the maximum number of boxes has been reached
                const weekday = handleWeekDay(weekDay);
                const mainDish = document.getElementById("main-dish").value;
                const salad = document.getElementById("salad").value;
                const sideDish = document.getElementById("side-dish").value;
                const accompaniment = document.getElementById("accompaniment").value;
    
                // Create a new box
                const contentBox = document.createElement("div");
                contentBox.classList.add("summary-box");
    
                // Create the content for the box
                let content = `
                    <div class="content-item">
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
                document.getElementById("summary-container").appendChild(contentBox);
                subscribeButton.style.display = "block";
    
                // Remove selected weekday from dropdown options
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
    
                    // Add removed weekday back to dropdown options
                    const optionElement = document.createElement("option");
                    optionElement.value = weekDay;
                    optionElement.text = handleWeekDay(weekDay);
                    weekDaySelect.appendChild(optionElement);
                });
    
                boxCount++; // Increase the box count when a box is added
            } else {
                console.log("Maximum number of summary boxes reached.");
            }
        } else {
            console.log("Weekday is required to add a box.");
        }
    });

    // Add button and code to subscribe to the backend
    document.getElementById("submit-menu-button").addEventListener("click", async function() {
        try {
            const response = await fetch("/subscribe", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: document.getElementById("email-input").value
                })
            });
            if (response.ok) {
                console.log("Subscribed successfully!");
            } else {
                console.log("Failed to subscribe.");
            }
        } catch (error) {
            console.error("An error occurred while subscribing:", error);
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
