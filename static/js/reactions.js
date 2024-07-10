document.getElementById('chat-box').style.display = 'none';

document.querySelectorAll('.message-button').forEach(button => {
    button.addEventListener('click', () => {
        const friendId = button.getAttribute('data-friend-id');
        fetch(`/friends/chat/${friendId}/`)
            .then(response => response.json())
            .then(data => {
                console.log(data);

                document.getElementById('chat-box').style.display = 'flex';
                document.getElementById('chat-messages').innerHTML = data.messages.map(message => {
                    if (message.is_sender) {
                        return `
                            <div class="message sent-message">
                                <p>${message.content}</p>
                                <span class="message-details">You</span>
                            </div>`;
                    } else {
                        return `
                            <div class="message received-message">
                                <p>${message.content}</p>
                                <span class="message-details">${message.sender}</span>
                            </div>`;
                    }
                }).join('');

                const chatMessages = document.getElementById('chat-messages');
                chatMessages.scrollTop = chatMessages.scrollHeight;

                document.getElementById('chat-send-button').onclick = () => {
                    const message = document.getElementById('chat-input').value;
                    fetch(`/friends/send_message/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': '{{ csrf_token }}'
                        },
                        body: JSON.stringify({ receiver_id: friendId, message: message })
                    }).then(() => {
                        document.getElementById('chat-input').value = '';
                        fetch(`/friends/chat/${friendId}/`)
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('chat-messages').innerHTML = data.messages.map(message => {
                                    if (message.is_sender) {
                                        return `
                                            <div class="message sent-message">
                                                <p>${message.content}</p>
                                                <span class="message-details">You</span>
                                            </div>`;
                                    } else {
                                        return `
                                            <div class="message received-message">
                                                <p>${message.content}</p>
                                                <span class="message-details">${message.sender}</span>
                                            </div>`;
                                    }
                                }).join('');

                                chatMessages.scrollTop = chatMessages.scrollHeight;
                            });
                    });
                };
            })
            .catch(error => console.error('Ошибка при получении данных чата:', error));
    });
});
