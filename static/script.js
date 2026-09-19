const input = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const chatBox = document.querySelector(".chat-box");

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});


async function sendMessage() {

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    // Show user's message
    chatBox.innerHTML += `
        <div class="message user">
            <div class="bubble">${message}</div>
        </div>
    `;

    input.value = "";

    try {

        // Send message to Flask
        const response = await fetch("/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        // Get AI response
        const data = await response.json();

        // Format AI response
        const formattedResponse = formatAIResponse(data.response);

        // Show AI response
        chatBox.innerHTML += `
            <div class="message agent">
                <div class="avatar">AI</div>

                <div class="bubble">
                    ${formattedResponse}
                </div>
            </div>
        `;

    } catch (error) {

        chatBox.innerHTML += `
            <div class="message agent">
                <div class="avatar">AI</div>

                <div class="bubble">
                    Sorry, I couldn't connect to the AI service.
                </div>
            </div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}


// Convert basic Markdown from Gemini into HTML
function formatAIResponse(text) {

    return text
        .replace(/^### (.*)$/gm, "<h3>$1</h3>")
        .replace(/^## (.*)$/gm, "<h3>$1</h3>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/^\* (.*)$/gm, "<li>$1</li>")
        .replace(/\n/g, "<br>");
}