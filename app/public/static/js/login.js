window.addEventListener('DOMContentLoaded', () => {
    const token = sessionStorage.getItem('jwt');
    if (token) {
        fetch('/auth/verify_token', {
            headers: { token }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/menu';
            }
        })
        .catch(error => {
            sessionStorage.removeItem('jwt');
        });
    }
});

let email = '';

function handleLogin(event) {
    event.preventDefault();
    const form = document.getElementById('loginForm');
    fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: form.email.value,
            password: form.password.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            sessionStorage.setItem('jwt', data.token);
            window.location.href = '/menu';
        } else {
            showCustomNotification('Falha no Login', 'Email ou senha inválidos', false);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function handleForgotPassword(event) {
    event.preventDefault();
    showCustomNotification('Redefinição de Senha', 'Enviando instruções para redefinir a senha...', true)
    const form = document.getElementById('forgot-password-form');
    email = form.email.value;
    fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: form.email.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showCustomNotification('Redefinição de Senha', 'Instruções para redefinir a senha enviadas para o seu email.', true);
            document.getElementById('forgot-password-form').style.display = 'none';
            document.getElementById('new-password-form').style.display = 'none';
            document.getElementById('code-check-form').style.display = 'block';
        } else {
            showCustomNotification('Falha na Redefinição de Senha', 'Falha ao enviar as instruções para redefinir a senha.', false);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function handleCodeCheck(event) {
    event.preventDefault();
    const form = document.getElementById('code-check-form');
    fetch(form.action, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "code": form.code.value
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('code-check-form').style.display = 'none';
            document.getElementById('new-password-form').style.display = 'block';
        } else {
            showCustomNotification('Falha na Redefinição de Senha', 'Falha ao redefinir a senha.', false);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function handleNewPassword(event) {
    event.preventDefault();
    const form = document.getElementById('new-password-form');

    if (form.password.value !== form.passwordConfirm.value) {
        showCustomNotification('Falha na Redefinição de Senha', 'As senhas não coincidem.', false);
        return;
    }

    fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email,
            password: form.password.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showCustomNotification('Redefinição de Senha', 'Senha redefinida com sucesso.', true);
            setTimeout(() => {
                window.location.href = '/login';
            }, 1000);
        } else {
            showCustomNotification('Falha na Redefinição de Senha', 'Falha ao redefinir a senha.', false);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function showCustomNotification(title, message, isSuccess) {
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
    }, 5000);
}