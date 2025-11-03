document.addEventListener("DOMContentLoaded", () => {

    //Floating Button
    const chatButton = document.createElement("div");
    chatButton.id = "chat-button";
    chatButton.innerHTML = "💬";
    document.body.appendChild(chatButton);

    //chat Window
    const chatWindow = document.createElement("div");
    chatWindow.id = "chat-window";
    chatWindow.innerHTML = `
        <div id="chat-header">Animal Shelter Chatbot 🐾</div>
        <div id="chat-log"></div>
        <div id="chat-input-area">
            <input type="text" id="chat-input" placeholder="Ask about adoption...">
            <button id="chat-send">Send</button>
        </div>
    `;
    document.body.appendChild(chatWindow);

    //Toggle
    chatButton.addEventListener("click", () => {
        chatWindow.classList.toggle("open");
    });

    // CSRF token function
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const input = document.getElementById("chat-input");
    const sendButton = document.getElementById("chat-send");


    //Send Message
    async function sendMessage(params) {
        const message = input.value.trim();
        if (!message) return;

        const chatLog = document.getElementById("chat-log");
        chatLog.innerHTML += `<p class="user-msg"><b>You:</b> ${message}</p>`;

        //Fetch Response
        const response = await fetch("/chatbot/get-response/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")  // <-- include token here
            },
            body: JSON.stringify({ message })
        });
        const data = await response.json();

        chatLog.innerHTML += `<p class="bot-msg"><b>Bot:</b> ${data.reply}</p>`;
        input.value = "";
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // Send message on button click
    sendButton.addEventListener("click", sendMessage);

    // Send message on Enter key press
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault(); // prevent form submission
            sendMessage();
        }
    });
});