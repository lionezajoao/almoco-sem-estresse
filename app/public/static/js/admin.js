document.addEventListener("DOMContentLoaded", async function() {
    await handleToken();
    document.getElementById("logout-button").addEventListener("click", function() {
        sessionStorage.removeItem("jwt");
        window.location.href = "/login";
    });
});

async function handleToken() {
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

    if (userRole !== "admin") {
        sessionStorage.removeItem("jwt");
        window.location.href = "/login";
    }

    return jwt;
}

function loadUserForm() {
    document.getElementById("new-user-form").style.display = "block";
    document.getElementById("users-list").style.display = "none";
    document.getElementById("new-dish-form").style.display = "none";
}

async function loadUserList() {
    document.getElementById("new-user-form").style.display = "none";
    document.getElementById("new-dish-form").style.display = "none";
    
    const jwt = await handleToken();
    const table = document.getElementById("users-list");
    table.innerHTML = "";
    
    const response = await fetch("/users/list_all_users", {
        headers: {
            "Content-Type": "application/json",
            "token": jwt
        }
    })
    .then(response => response.json());

    
    const header = document.createElement("tr");
    header.innerHTML = `
        <th>Nome</th>
        <th>Email</th>
        <th>Papel</th>
        <th></th>
    `;

    table.appendChild(header);
    
    response.forEach(user => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${user[1]}</td>
            <td>${user[0]}</td>
            <td>${user[2]}</td>
            <td><button class="delete-user">Remover</button></td>
        `;
        table.appendChild(row);
    });

    const buttons = document.querySelectorAll(".delete-user");
    buttons.forEach((button, index) => {
        button.addEventListener("click", function() {
            handleDeleteUser(response[index][0]);
        });
    });
    document.getElementById("users-list").style.display = "block";
}

async function handleDeleteUser(userEmail) {
    const jwt = await handleToken();

    const response = await fetch("/users/delete_user", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "token": jwt,
        },
        body: JSON.stringify({ email: userEmail})
    })
    .then(response => response.json());

    if (response.success) {
        showCustomNotification("Usuário removido com sucesso!", null, true);
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    } else {
        showCustomNotification("Erro ao remover usuário. Tente novamente.", null, false);
    }
}

async function handleCreateUser(event) {
    event.preventDefault();
    showCustomNotification("Criando usuário, aguarde...", null, false);

    const jwt = await handleToken();
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const role = document.getElementById("role").value;

    const data = {
        name,
        email,
        role,
        password: generateRandomPassword(Math.floor(Math.random() * 10) + 8)
    }

    const response = await fetch("/users/create_user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "token": jwt,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json());

    if (response.success) {
        showCustomNotification("Usuário criado com sucesso!", null, true);
                
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    } else {
        showCustomNotification("Erro ao criar usuário. Tente novamente.", null, false);
    }
    
}

function addIngredientField() {
    const container = document.getElementById('ingredient-fields-container');
    container.style.display = 'block';

    const groupDiv = document.createElement('div');
    groupDiv.className = 'form-group';

    const ingredientInput = document.createElement('input');
    ingredientInput.type = 'text';
    ingredientInput.name = 'ingredientName';
    ingredientInput.placeholder = 'Ingrediente';
    ingredientInput.required = true;
    groupDiv.appendChild(ingredientInput);

    const typeInput = document.createElement('select');
    typeInput.id = 'ingredient-type';
    typeInput.name = 'ingredient-type';
    typeInput.required = true;

    const options = [
        { value: 'Frios', text: 'Frios' },
        { value: 'Proteína', text: 'Proteína' },
        { value: 'Hortifruti', text: 'Hortifruti' },
        { value: 'Mercearia', text: 'Mercearia' }
    ];

    options.forEach(option => {
        const newOption = document.createElement('option');
        newOption.value = option.value;
        newOption.text = option.text;
        typeInput.appendChild(newOption);
    });

    groupDiv.appendChild(typeInput);

    container.appendChild(groupDiv);
}



function loadNewItemForm(event) {
    const form = document.getElementById("new-dish-form");
    document.getElementById("users-list").style.display = "none";
    document.getElementById("new-user-form").style.display = "none";

    form.style.display = "block";

    form.addEventListener("submit", handleNewItem(event));

}

async function handleNewItem(event) {
    event.preventDefault();
    showCustomNotification("Criando novo item, aguarde...", null, false);

    const jwt = await handleToken();
    const name = document.getElementById("dishName").value;
    const dishType = document.getElementById("dishType").value;
    const ingredients = document.getElementsByName("ingredientName");
    const ingredientTypes = document.getElementsByName("ingredient-type");

    const ingredientList = [];
    for (let i = 0; i < ingredients.length; i++) {
        ingredientList.push({
            name: ingredients[i].value,
            type: ingredientTypes[i].value
        });
    }

    const data = {
        name,
        type: dishType,
        ingredients: ingredientList
    }

    const response = await fetch("/menu/add_new_item", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "token": jwt,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json());

    if (response.success) {
        showCustomNotification("Item criado com sucesso!", null, true);
                
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    } else {
        showCustomNotification("Erro ao criar item. Tente novamente.", null, false);
    }
}

function generateRandomPassword(length) {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$&";
    let password = "";
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        password += characters.charAt(randomIndex);
    }
    return password;
}


function showCustomNotification(title, message, isSuccess) {
    const container = document.getElementById('notification-container');

    // Criando a notificação
    const notification = document.createElement('div');
    notification.classList.add('notification-box');

    // Definindo a cor com base no sucesso ou erro
    if (isSuccess) {
        notification.classList.add('success');
    } else {
        notification.classList.add('error');
    }

    // Botão de fechar
    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = '&times;';
    closeBtn.classList.add('close-btn');
    closeBtn.onclick = function() {
        container.removeChild(notification);
    };

    // Título
    const notifTitle = document.createElement('h4');
    notifTitle.textContent = title;

    // Mensagem
    const notifMessage = document.createElement('p');
    notifMessage.textContent = message;

    // Montando a notificação
    notification.appendChild(closeBtn);
    notification.appendChild(notifTitle);
    notification.appendChild(notifMessage);

    // Adicionando a notificação ao container
    container.appendChild(notification);

    // Auto remover a notificação após 5 segundos
    setTimeout(() => {
        if (container.contains(notification)) {
            container.removeChild(notification);
        }
    }, 2000);
}
