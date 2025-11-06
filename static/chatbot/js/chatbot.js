document.addEventListener("DOMContentLoaded", () => {

    const UserName = window.loggedInUsername || "Guest";
    //Floating Button
    const chatButton = document.createElement("div");
    chatButton.id = "chat-button";
    chatButton.innerHTML = "💬";
    document.body.appendChild(chatButton);

    //chat Window
    const chatWindow = document.createElement("div");
    chatWindow.id = "chat-window";
    chatWindow.innerHTML = `
        <div id="chat-header">Bojack 🐾</div>
        <div id="chat-log"></div>
        <div id="chat-input-area">
            <input type="text" id="chat-input" placeholder="Ask about adoption...">
            <button id="chat-send">Send</button>
        </div>
    `;
    document.body.appendChild(chatWindow);

    // Toggle
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

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    //Send Message
    async function sendMessage() {
        const message = input.value.trim();
        if (!message) return;

        const chatLog = document.getElementById("chat-log");

        // User Message
        const userMessage = document.createElement("p");
        userMessage.className = "user-msg";
        userMessage.innerHTML = `<b>${UserName}:</b> ${message}`;
        chatLog.appendChild(userMessage);

        // thinking message
        const typingMessage = document.createElement("p");
        typingMessage.className = "bot-msg";
        typingMessage.id = "typing";
        typingMessage.textContent = "Bojack is Thinking...";
        chatLog.appendChild(typingMessage);

        //Fetch Response
        let data;
        try {
            const response = await fetch("/chatbot/get-response/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({ message })
            });
            data = await response.json();
        }
        catch (error) {
            typingMessage.remove();
            chatLog.appendChild(Object.assign(document.createElement("p"), {
                className: "bot-msg",
                innerHTML: "<b>Bojack:</b> Bojack is having an existential crisis. Please try again later."
            }));
            return;
        }

        await sleep(1000); // simulate typing delay

        typingMessage.remove(); // Remove typing message


        // Split bot response into sentences and display each
        const rawbotSentences = data.reply.split(/([.?!])\s+/);
        for (let i = 0; i < rawbotSentences.length; i += 2) {
            const botSentence = (rawbotSentences[i] || '') + (rawbotSentences[i + 1] || '');
            if (botSentence.trim()) {
                const p = document.createElement("p");
                p.className = "bot-msg";
                p.innerHTML = `<b>Bojack:</b> ${botSentence.trim()}`;
                chatLog.appendChild(p);
            }
        }

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