function showCustomNotification(title, message) {
    const container = document.getElementById('notification-container');

    // Criando a notificação
    const notification = document.createElement('div');
    notification.classList.add('notification-box');

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
    }, 5000);
}
