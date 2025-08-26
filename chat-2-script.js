class ChatInterface {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.clearBtn = document.getElementById('clearChat');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.errorDiv = document.getElementById('chatError')
        this.userpreferences = {}
        
        this.init();
    }
    
    init() {
        // Add days of the week input to chat
		this.setUpDaysInput()
        

        // Event listeners
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        this.clearBtn.addEventListener('click', () => this.clearChat());
        
        // Auto-resize input
        this.messageInput.addEventListener('input', () => this.handleInputChange());
    }

	setUpDaysInput() {
		const daysSelectionInput = document.createElement('div');
        daysSelectionInput.id = "days-message";
        daysSelectionInput.className = "message user-message";

        daysSelectionInput.innerHTML = `
			<div class="message-avatar">You</div>
			<div class="message-content">
				<div id="days-container" class="message-text">
					<label class="container"><input type="checkbox" id="monday">Monday<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" id="tuesday">Tuesday<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" id="wednesday">Wednesday<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" id="thursday">Thursday<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" id="friday">Friday<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" id="saturday">Saturday<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" id="sunday">Sunday<span class="checkmark"></span></label>
					<button id="daysDoneButton" class="done-btn">Done</button>
				</div>
				<div id="messageTimeForDays" class="message-time" class="widget-message-time"></div>
			</div>
        `;
        this.chatMessages.appendChild(daysSelectionInput);
		const doneButton = document.getElementById("daysDoneButton");
        doneButton.addEventListener("click", () => {

            const selectedDays = Array.from(document.querySelectorAll('#days-container input:checked'))
              .map(input => input.id);
            
            if (selectedDays.length == 0) {
				this.errorDiv.textContent = "⚠️ Please select at least one day before continuing.";
				this.errorDiv.style.display = "block";
				return;
			} else if (selectedDays.length == 7) {
				this.errorDiv.textContent = "⚠️ Please leave at least one rest day before continuing.";
				this.errorDiv.style.display = "block";
				return;
			} else {
				// Hide error if previously shown
    			this.errorDiv.style.display = "none";
				// Hide done button
				doneButton.style.display = "none";
				// Disable selection boxes
				document.querySelectorAll('#days-container label.container').forEach(label => {
					const cb = label.querySelector('input[type="checkbox"]');
					cb.disabled = true;
					label.classList.add("disabled")
				});

				// Display timestamp of message send
				const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

				const messageTimeDiv = document.getElementById("messageTimeForDays")
				messageTimeDiv.innerHTML = currentTime
				messageTimeDiv.style.display = "block";
				this.userpreferences["days"] = selectedDays;

				// Now call function to add next bot message regarding home/gym
				this.setUpHomeOrGymInput()
			}

            console.log(selectedDays);
        });
	}

	sleep(ms) {
		return new Promise(resolve => setTimeout(resolve, ms));
	}

	async setUpTimeInput() {
		// Show typing indicator
        this.showTypingIndicator();

		const delay = Math.random() * 200 + 100;
		await this.sleep(delay);

		this.hideTypingIndicator();

		const question = `Perfect, how much time do you want to spend per workout session?`
        
        this.addMessage(question, 'bot')


		const timeSelectionInput = document.createElement('div');
        timeSelectionInput.id = "timePerSession-message";
        timeSelectionInput.className = "message user-message";

        timeSelectionInput.innerHTML = `
			<div class="message-avatar">You</div>
			<div class="message-content">
				<div id="slider-container" class="message-text">
					<div id="sliderValue">50 min</div>
					<input type="range" min="15" max="90" value="50" class="slider" id="myRange">
					<button id="timeDoneButton" class="done-btn">Done</button>
				</div>
				<div id="messageTimeForTimePerSession" class="message-time" class="widget-message-time"></div>
			</div>
        `;
        this.chatMessages.appendChild(timeSelectionInput);

		const slider = document.getElementById("myRange");
		const sliderValue = document.getElementById("sliderValue");

		slider.addEventListener("input", () => {
			sliderValue.textContent = slider.value + " min";
		});

		const doneButton = document.getElementById("timeDoneButton");
        doneButton.addEventListener("click", () => {

            const timePerSession = slider.value;

			doneButton.style.display = "none";

			// Need to disable slider
			slider.disabled = true;

			// Display timestamp of message send
			const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

			const messageTimeDiv = document.getElementById("messageTimeForTimePerSession")
			messageTimeDiv.innerHTML = currentTime
			messageTimeDiv.style.display = "block";
			this.userpreferences["timePerSession"] = timePerSession;

            console.log(timePerSession);
        });
	}

	async setUpHomeOrGymInput() {
		// Show typing indicator
        this.showTypingIndicator();

		const delay = Math.random() * 200 + 100;
		await this.sleep(delay);

		this.hideTypingIndicator();

		const question = `Great, do you want to work out at the gym or at home?`
        
        this.addMessage(question, 'bot')

		
		const homeOrGymInput = document.createElement('div');
        homeOrGymInput.id = "homeOrGym-message";
        homeOrGymInput.className = "message user-message";

        homeOrGymInput.innerHTML = `
			<div class="message-avatar">You</div>
			<div class="message-content">
				<div id="slider-container" class="message-text">
					<div id="sliderValue">50 min</div>
					<input type="range" min="15" max="90" value="50" class="slider" id="myRange">
					<button id="homeOrGymDoneButton" class="done-btn">Done</button>
				</div>
				<div id="messageTimeForTimePerSession" class="message-time" class="widget-message-time"></div>
			</div>
        `;
        this.chatMessages.appendChild(timeSelectionInput);

		const slider = document.getElementById("myRange");
		const sliderValue = document.getElementById("sliderValue");

		slider.addEventListener("input", () => {
			sliderValue.textContent = slider.value + " min";
		});

		const doneButton = document.getElementById("timeDoneButton");
        doneButton.addEventListener("click", () => {

            const timePerSession = slider.value;

			doneButton.style.display = "none";

			// Need to disable slider
			slider.disabled = true;

			// Display timestamp of message send
			const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

			const messageTimeDiv = document.getElementById("messageTimeForTimePerSession")
			messageTimeDiv.innerHTML = currentTime
			messageTimeDiv.style.display = "block";
			this.userpreferences["timePerSession"] = timePerSession;

            console.log(timePerSession);


        });
	}
    
    sendMessage() {
        const messageText = this.messageInput.value.trim();
        if (!messageText) return;
        
        // Add user message
        this.addMessage(messageText, 'user');
        
        // Clear input
        this.messageInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Simulate bot response
        setTimeout(() => {
            this.hideTypingIndicator();
            this.generateBotResponse(messageText);
        }, 1000 + Math.random() * 2000); // Random delay between 1-3 seconds
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${sender === 'user' ? 'You' : 'AI'}</div>
            <div class="message-content">
                <div class="message-text">${this.escapeHtml(text)}</div>
                <div class="message-time">${currentTime}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    generateBotResponse(userMessage) {
        // Simple response generation (replace with actual AI integration)
        const responses = [
            "That's an interesting point! Can you tell me more?",
            "I understand what you're saying. Here's my perspective...",
            "Thanks for sharing that with me. Let me think about this...",
            "That's a great question! Based on what you've told me...",
            "I appreciate you bringing this up. Here's what I think...",
            "Interesting! I'd love to explore this topic further with you.",
            "Thank you for the message! I'm here to help with whatever you need."
        ];
        
        // Simple keyword-based responses
        const lowerMessage = userMessage.toLowerCase();
        let response;
        
        if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
            response = "Hello! It's great to chat with you. How are you doing today?";
        } else if (lowerMessage.includes('help')) {
            response = "I'm here to help! What do you need assistance with?";
        } else if (lowerMessage.includes('bye') || lowerMessage.includes('goodbye')) {
            response = "Goodbye! It was nice chatting with you. Feel free to come back anytime!";
        } else if (lowerMessage.includes('how are you')) {
            response = "I'm doing well, thank you for asking! How about you?";
        } else if (lowerMessage.includes('weather')) {
            response = "I don't have access to real-time weather data, but you could check a weather app or website for current conditions!";
        } else {
            response = responses[Math.floor(Math.random() * responses.length)];
        }
        
        this.addMessage(response, 'bot');
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    clearChat() {
        // Keep the initial welcome message
        this.chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">AI</div>
                <div class="message-content">
                    <div class="message-text">Hello! How can I help you today?</div>
                    <div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                </div>
            </div>
        `;
        this.hideTypingIndicator();
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    handleInputChange() {
        // Enable/disable send button based on input
        this.sendBtn.disabled = !this.messageInput.value.trim();
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatInterface();
});

// Add some utility functions for potential future use
const ChatUtils = {
    formatTime: (date) => {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    
    formatDate: (date) => {
        return date.toLocaleDateString();
    },
    
    generateId: () => {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
};