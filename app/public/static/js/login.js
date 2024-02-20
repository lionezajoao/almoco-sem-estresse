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
            document.getElementById('loginWarning').style.display = 'block';
            setTimeout(() => {
                document.getElementById('loginWarning').style.display = 'none';
            }, 1000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

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