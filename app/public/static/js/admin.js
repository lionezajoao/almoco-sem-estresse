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
}

async function handleCreateUser(event) {
    event.preventDefault();
    alert("Criando usuário, aguarde...");

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

    console.log(data);

    const response = await fetch("/users/create_user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "token": jwt,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json());
    console.log({ response });

    if (response.success) {
        alert("Usuário criado com sucesso!");
        // window.location.reload();
    } else {
        alert("Erro ao criar usuário. Tente novamente.");
    }
    
}

function generateRandomPassword(length) {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+{}[]|:;<>,.?/";
    let password = "";
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        password += characters.charAt(randomIndex);
    }
    return password;
}
