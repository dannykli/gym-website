const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const buildButton = document.getElementById('build-button')

let assistantIntro = `Before we build your perfect programme, let's sort out the last few details.
                First up — are there any muscle groups you'd like to avoid? 
                Maybe due to an injury, a preference, or something else?`

let chatHistory = [
  {
    "role": "assistant",
    "content": assistantIntro
  }
];

addMessageToChat('assistant', assistantIntro)

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const userMessage = userInput.value.trim();
  if (!userMessage) return;

  // Display user message
  addMessageToChat('user', userMessage);
  chatHistory.push({ role: 'user', content: userMessage });

  userInput.value = '';

  // Show assistant is thinking...
  addMessageToChat('assistant', '...');

  try {
    // === TODO: Replace with call to your Lambda ===
    const assistantReply = await getAssistantResponse(chatHistory);
    // =============================================

    // Remove placeholder
    removeLastMessage();

    // Display assistant response
    addMessageToChat('assistant', assistantReply);
    chatHistory.push({ role: 'assistant', content: assistantReply });

  } catch (err) {
    console.error(err);
    removeLastMessage();
    addMessageToChat('assistant', 'Sorry, something went wrong.');
  }
});

function addMessageToChat(sender, text) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('message', `${sender}-message`);
  msgDiv.textContent = text;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLastMessage() {
  const last = chatBox.lastElementChild;
  if (last) chatBox.removeChild(last);
}

// === Placeholder function for your Lambda integration ===
async function getAssistantResponse(chatHistory) {
  // Example call to your AWS Lambda (via API Gateway endpoint)
  const response = await fetch('https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/getAIResponse', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(chatHistory),
  });

  if (!response.ok) {
    throw new Error('LLM API error');
  }

  const data = await response.json();
  return data.reply; // Adjust based on your Lambda's response shape
}

buildButton.addEventListener("click", async () => {
  const result = await fetch('https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/populateExtraInfoJSON', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(chatHistory),
  });

  if (!result.ok) {
    throw new Error('LLM API error');
  }

  const extraPreferences = await result.json()

  console.log(JSON.stringify(extraPreferences.body, null, 2));
});