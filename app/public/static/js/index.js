document.addEventListener("DOMContentLoaded", function() {
    // Load an initial card
    addCard();

    document.getElementById("add-card-button").addEventListener("click", addCard);
    document.getElementById("remove-card-button").addEventListener("click", removeCard);
});

function addCard() {
    const cardContainer = document.getElementById("card-container");
    const newCard = document.createElement("div");
    newCard.className = "card";
    newCard.innerHTML = '<form class="card-form"></form>';
    cardContainer.appendChild(newCard);

    addFormFields(newCard.querySelector('.card-form'));
}

function removeCard() {
    const cardContainer = document.getElementById("card-container");
    const cards = cardContainer.getElementsByClassName("card");

    if (cards.length > 1) {
        cardContainer.removeChild(cards[cards.length - 1]);
    }
}

function addFormFields(formElement) {
    // Define the fields you want in each form
    const fields = [
        { name: 'name', type: 'text', placeholder: 'Name' },
        { name: 'email', type: 'email', placeholder: 'Email' },
        { name: 'message', type: 'text', placeholder: 'Message' }
        // Add more fields as needed
    ];

    fields.forEach(field => {
        const input = document.createElement("input");
        input.type = field.type;
        input.name = field.name;
        input.placeholder = field.placeholder;
        formElement.appendChild(input);
    });
}
