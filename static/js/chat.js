document.addEventListener('DOMContentLoaded', () => {
    greetUser ();
    getMachineFailurePrediction();
});

document.getElementById('send-button').addEventListener('click', sendMessage);

function greetUser () {
    fetch('/greet')
        .then(response => response.json())
        .then(data => {
            addMessageToChat('GenDrive', data.greeting);
        });
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    addMessageToChat('You', userInput);
    document.getElementById('user-input').value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: userInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            addMessageToChat('GenDrive', data.response);
        } else {
            addMessageToChat('GenDrive', 'No response received.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function getMachineFailurePrediction() {
    fetch('/predict')
        .then(response => response.json())
        .then(data => {
            const predictionResult = document.getElementById('prediction-result');
            const warningSign = document.getElementById('warning-sign');
            const normalbehaviour = document.getElementById('prediction-value');

           // predictionResult.textContent = data.prediction;
            if (data.prediction === 0) {
                normalbehaviour.style.display = 'block'; // Show warning sign
            } else {
                normalbehaviour.style.display = 'none'; // Hide warning sign
            }
            if (data.prediction === 1) {
                warningSign.style.display = 'block'; // Show warning sign
            } else {
                warningSign.style.display = 'none'; // Hide warning sign
            }
        })
        .catch(error => console.error('Error:', error));

    setTimeout(getMachineFailurePrediction, 1000); // Update every 1 second
}

function addMessageToChat(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + (sender === 'You' ? 'user' : 'bot');
    messageElement.textContent = `${sender}: ${message}`;
    document.getElementById('messages').appendChild(messageElement);
    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight; // Auto-scroll
}

