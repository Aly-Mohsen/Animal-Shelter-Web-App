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
    const chatLog = document.getElementById("chat-log");

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    //Send Message
    async function sendMessage() {
        const message = input.value.trim();
        if (!message) return;

        // User Message
        appendMessage(UserName, message, "user-msg");
        // const userMessage = document.createElement("p");
        // userMessage.className = "user-msg";
        // userMessage.innerHTML = `<b>${UserName}:</b> ${message}`;
        // chatLog.appendChild(userMessage);

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

            if (!response.ok || typeof data.reply !== "string"){
                throw new Error("Invalid chatbot response");
            }
        }
        catch (error) {
            typingMessage.remove();

            appendMessage(
                "Bojack",
                "Bojack is having an existential crisis. Please try again later.",
                "bot-msg"
            );

            return;
        }

        await sleep(1000); // simulate typing delay

        typingMessage.remove(); // Remove typing message


        // Split bot response into sentences and display each
        const sentences = data.reply.match(/[^.!?]+[.!?]*\s*/g) || [];

        for (const sentence of sentences) {
            if (sentence.trim()) {
                appendMessage("Bojack", sentence.trim(), "bot-msg");
            }
        }

        input.value = "";
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // Appends messages to the chat log
    function appendMessage(speaker, message, className) {
        const paragraph = document.createElement("p");
        paragraph.className = className;

        const label = document.createElement("b");
        label.textContent = `${speaker}:`;

        paragraph.appendChild(label);
        paragraph.appendChild(document.createTextNode(` ${message}`));

        chatLog.appendChild(paragraph);
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