class ChatInterface {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.clearBtn = document.getElementById('clearChat');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.errorDiv = document.getElementById('chatError');
        this.userPreferences = {};
				this.chatHistory = [];
				this.buildBtn = document.getElementById("buildBtn");
				this.chatMessageBox = document.getElementById("chat-input-box");
				this.retryModal = document.getElementById("retryModal");
				this.closeRetryModal = document.getElementById("closeRetryModal");
				this.okBtn = document.getElementById("okBtn");
        
        this.init();
    }
    
    init() {
			// Set time for first bot question: 
			const messageTime = document.querySelector('.chat-messages .message-time');
			const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
			
			messageTime.textContent = currentTime;

			this.clearBtn.addEventListener('click', () => this.clearChat());

			this.buildBtn.addEventListener('click', () => this.handleBuildProgramme());

			window.addEventListener('click', (event) => {
					if (event.target === this.retryModal) {
							this.retryModal.style.display = 'none';
							this.clearChat();
					}
			});

			this.closeRetryModal.addEventListener('click', () => {
					this.retryModal.style.display = 'none';
			})
	
			this.okBtn.addEventListener('click', () => {
					this.retryModal.style.display = 'none';
					this.clearChat();
			})

			// Add days of the week input to chat
			this.setUpDaysInput();
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
			this.userPreferences["days"] = selectedDays;

			// Now call function to add next bot message regarding time per session
			this.setUpTimeInput()
					}
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

		const question = `Perfect. How much time do you want to spend per workout session?`
        
        this.addMessage(question, 'bot')

		const timeSelectionInput = document.createElement('div');
        timeSelectionInput.id = "timePerSession-message";
        timeSelectionInput.className = "message user-message";

        timeSelectionInput.innerHTML = `
			<div class="message-avatar">You</div>
			<div class="message-content">
				<div id="slider-container" class="message-text">
					<div id="sliderValue">45 min</div>
					<input type="range" min="15" max="90" value="50" step="5" class="slider" id="myRange">
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

			// Hide error if previously shown
			this.errorDiv.style.display = "none";
			// Hide done button
			doneButton.style.display = "none";

			// Display timestamp of message send
			const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

			const messageTimeDiv = document.getElementById("messageTimeForTimePerSession");
			messageTimeDiv.innerHTML = currentTime;
			messageTimeDiv.style.display = "block";
			this.userPreferences["timePerSession"] = parseInt(timePerSession);

			// Now call function to add next bot message regarding time per session
			this.setUpHomeOrGymInput();
        });
	}

	async setUpHomeOrGymInput() {
		// Show typing indicator
        this.showTypingIndicator();

		const delay = Math.random() * 200 + 100;
		await this.sleep(delay);

		this.hideTypingIndicator();

		const question = `Great. Do you want to work out at the gym or at home?`
        
        this.addMessage(question, 'bot')

		const homeOrGymInput = document.createElement('div');
        homeOrGymInput.id = "homeOrGym-message";
        homeOrGymInput.className = "message user-message";

        homeOrGymInput.innerHTML = `
			<div class="message-avatar">You</div>
			<div class="message-content">
				<div id="home-or-gym-container" class="message-text">
					<label class="radio-container">Gym
						<input type="radio" name="workoutLocation" value="gym">
						<span class="radio-checkmark"></span>
					</label>
					<label class="radio-container">Home
						<input type="radio" name="workoutLocation" value="home">
						<span class="radio-checkmark"></span>
					</label>
					<button id="homeOrGymDoneButton" class="done-btn">Done</button>
				</div>
				<div id="messageTimeForHomeOrGym" class="message-time" class="widget-message-time"></div>
			</div>
        `;
        this.chatMessages.appendChild(homeOrGymInput);

		const doneButton = document.getElementById("homeOrGymDoneButton");
        doneButton.addEventListener("click", () => {

			const selected = document.querySelector('input[name="workoutLocation"]:checked');

			if (!selected) {
				this.errorDiv.textContent = "⚠️ Please select one of the options before continuing.";
				this.errorDiv.style.display = "block";
				return;
			}

			// Hide error if previously shown
    		this.errorDiv.style.display = "none";

			doneButton.style.display = "none";

			console.log(selected.value);

			const trainAtGym = selected.value == "gym";

			// disable radios
			const radios = document.querySelectorAll('input[name="workoutLocation"]');
			radios.forEach(radio => {
			radio.disabled = true;
			});

			// Display timestamp of message send
			const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

			const messageTimeDiv = document.getElementById("messageTimeForHomeOrGym")
			messageTimeDiv.innerHTML = currentTime
			messageTimeDiv.style.display = "block";

			// Display next question
			this.setUpEquipmentInput(trainAtGym)
        });
	}

	async setUpEquipmentInput(trainAtGym) {
		// Show typing indicator
        this.showTypingIndicator();

		const delay = Math.random() * 200 + 100;
		await this.sleep(delay);

		this.hideTypingIndicator();

		let question = `Awesome! What equipment do you have access to at home?`

		if (trainAtGym) {
			question = `Awesome! What equipment do you have at the gym?
						(De-select any which you don't have)`
		}
        
        this.addMessage(question, 'bot')

		const equipmentSelectionInput = document.createElement('div');
        equipmentSelectionInput.id = "equipmentSelection-message";
        equipmentSelectionInput.className = "message user-message";

        equipmentSelectionInput.innerHTML = `
			<div class="message-avatar">You</div>
			<div class="message-content">
				<div id="equipment-container" class="message-text">
					<label class="container"><input type="checkbox" value="ab roller">Ab Roller<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="bands">Bands<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="barbell">Barbell<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="bench">Bench<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="cable">Cable Machine<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="dip bar">Dip bar<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="dumbbell">Dumbbells<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="exercise ball">Exercise Ball<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="e-z curl bar">EZ Curl Bar<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="kettlebells">Kettlebells<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="pull up bar">Pull-Up bar<span class="checkmark"></span></label>
					<label class="container"><input type="checkbox" value="machine">Weight Machines<span class="checkmark"></span></label>
					<button id="equipmentDoneButton" class="done-btn">Done</button>
				</div>
				<div id="messageTimeForEquipment" class="message-time" class="widget-message-time"></div>
			</div>
        `;

        this.chatMessages.appendChild(equipmentSelectionInput);

		if (trainAtGym) {
			document.querySelectorAll('#equipment-container input').forEach(input => {
				input.checked = true;
			});
		}

		const doneButton = document.getElementById("equipmentDoneButton");
        doneButton.addEventListener("click", () => {

			const selectedEquipment = Array.from(document.querySelectorAll('#equipment-container input:checked'))
              .map(input => input.value);
   
			// Hide done button
			doneButton.style.display = "none";
			// Disable selection boxes
			document.querySelectorAll('#equipment-container label.container').forEach(label => {
				const cb = label.querySelector('input[type="checkbox"]');
				cb.disabled = true;
				label.classList.add("disabled")
			});

			// Display timestamp of message send
			const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

			const messageTimeDiv = document.getElementById("messageTimeForEquipment")
			messageTimeDiv.innerHTML = currentTime
			messageTimeDiv.style.display = "block";
			this.userPreferences["equipment"] = selectedEquipment;

			console.log(selectedEquipment)

			// Display next question
			this.setUpBeginnerInput();
        });

	}

	async setUpBeginnerInput() {
		// Show typing indicator
        this.showTypingIndicator();

		const delay = Math.random() * 200 + 100;
		await this.sleep(delay);

		this.hideTypingIndicator();

		const question = `Are you new to working out?`

        this.addMessage(question, 'bot')

		const beginnerInput = document.createElement('div');
        beginnerInput.id = "beginner-message";
        beginnerInput.className = "message user-message";

        beginnerInput.innerHTML = `
			<div class="message-avatar">You</div>
			<div class="message-content">
				<div id="beginner-container" class="message-text">
					<label class="radio-container">Yes, I'm a beginner
						<input type="radio" name="beginner" value="yes">
						<span class="radio-checkmark"></span>
					</label>
					<label class="radio-container">No, I'm experienced
						<input type="radio" name="beginner" value="no">
						<span class="radio-checkmark"></span>
					</label>
					<button id="beginnerDoneButton" class="done-btn">Done</button>
				</div>
				<div id="messageTimeForBeginner" class="message-time" class="widget-message-time"></div>
			</div>
        `;
        this.chatMessages.appendChild(beginnerInput);

		const doneButton = document.getElementById("beginnerDoneButton");
        doneButton.addEventListener("click", () => {

			const selected = document.querySelector('input[name="beginner"]:checked');

			if (!selected) {
				this.errorDiv.textContent = "⚠️ Please select one of the options before continuing.";
				this.errorDiv.style.display = "block";
				return;
			}

			// Hide error if previously shown
    		this.errorDiv.style.display = "none";

			doneButton.style.display = "none";

			console.log(selected.value);

			this.userPreferences["beginnerFriendly"] = selected.value == "yes"

			// disable radios
			const radios = document.querySelectorAll('input[name="beginner"]');
			radios.forEach(radio => {
			radio.disabled = true;
			});

			// Display timestamp of message send
			const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

			const messageTimeDiv = document.getElementById("messageTimeForBeginner")
			messageTimeDiv.innerHTML = currentTime
			messageTimeDiv.style.display = "block";
			
			// Display next question
			this.setUpVariationInput()
			
        });
	}

	async setUpVariationInput() {
		// Show typing indicator
        this.showTypingIndicator();

		const delay = Math.random() * 200 + 100;
		await this.sleep(delay);

		this.hideTypingIndicator();

		const question = `Okay great! Do you prefer having a high variety of exercises, with few repeats?`

        this.addMessage(question, 'bot')

		const variationInput = document.createElement('div');
        variationInput.id = "variation-message";
        variationInput.className = "message user-message";

        variationInput.innerHTML = `
			<div class="message-avatar">You</div>
			<div class="message-content">
				<div id="variation-container" class="message-text">
					<label class="radio-container">Yes, I like variety
						<input type="radio" name="variation" value="yes">
						<span class="radio-checkmark"></span>
					</label>
					<label class="radio-container">No, I prefer routine
						<input type="radio" name="variation" value="no">
						<span class="radio-checkmark"></span>
					</label>
					<label class="radio-container">I don't mind
						<input type="radio" name="variation" value="not bothered">
						<span class="radio-checkmark"></span>
					</label>
					<button id="variationDoneButton" class="done-btn">Done</button>
				</div>
				<div id="messageTimeForVariation" class="message-time" class="widget-message-time"></div>
			</div>
        `;
        this.chatMessages.appendChild(variationInput);

		const doneButton = document.getElementById("variationDoneButton");
        doneButton.addEventListener("click", () => {

			const selected = document.querySelector('input[name="variation"]:checked');

			if (!selected) {
				this.errorDiv.textContent = "⚠️ Please select one of the options before continuing.";
				this.errorDiv.style.display = "block";
				return;
			}

			// Hide error if previously shown
    		this.errorDiv.style.display = "none";

			doneButton.style.display = "none";

			console.log(selected.value);

			let variety_score = 0; 
			if (selected.value == "yes") {
				variety_score = 1.1;
			} if (selected.value == "not bothered") {
				variety_score = 0.5;
			}

			this.userPreferences["exerciseVariation"] = variety_score;

			// disable radios
			const radios = document.querySelectorAll('input[name="variation"]');
			radios.forEach(radio => {
				radio.disabled = true;
			});

			// Display timestamp of message send
			const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

			const messageTimeDiv = document.getElementById("messageTimeForVariation")
			messageTimeDiv.innerHTML = currentTime
			messageTimeDiv.style.display = "block";
			
			// Display next question
			this.setUpMuscleGroupInput()
			
        });
	}

	async setUpMuscleGroupInput() {
		// Show typing indicator
        this.showTypingIndicator();

		const delay = Math.random() * 200 + 100;
		await this.sleep(delay);

		this.hideTypingIndicator();

		const question = `Are there any muscle groups you'd like to avoid working out? (e.g., due to injury or preference)`

        this.addMessage(question, 'bot', true);

		// Reduce bottom padding
		const chatMessages = document.querySelector('.chat-messages');
		chatMessages.style.paddingBottom = "20px";

		// Show chat message box
		this.chatMessageBox.style.display = "block";

		// Show build button
		this.buildBtn.style.display = "block";

		// Event listeners
		this.sendBtn.addEventListener('click', () => this.sendMessage());

		this.messageInput.addEventListener('keypress', (e) => {
				if (e.key === 'Enter') {
						this.sendMessage();
				}
		});
		
		// Auto-resize input
		this.messageInput.addEventListener('input', () => this.handleInputChange());
	}

	/*
	async handleBuildProgramme() {
		// Show overlay
		document.getElementById("loadingOverlay").style.display = "flex";

		const result = await fetch('https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/populateExtraInfoJSON', {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json',
			},
			body: JSON.stringify(this.chatHistory),
		});

		if (!result.ok) {
			throw new Error('LLM API error');
		}

		const extraPreferences = await result.json();

	  this.userPreferences = { ...this.userPreferences, ...extraPreferences};
	
		const requiredKeys = ["days", "timePerSession", "equipment", "beginnerFriendly", "exerciseVariation", "excludedMuscleGroups", "preferredMuscleGroups"]
		for (const key of requiredKeys) {
			if (!(key in this.userPreferences)) {
				console.log(`Error: no ${key} key in userPreferences object`)
				this.userPreferences[key] = null;
			}
		}

		console.log(JSON.stringify(this.userPreferences, null, 2));

		// Now call lambda func to build programme
		const response = await fetch('https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/buildProgramme', {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json',
			},
			body: JSON.stringify(this.userPreferences),
		});

		console.log(response.status)

		if (response.status !== 200) {
				try {
						const response_body = await response.json();
						
						// The body is a JSON string, so we need to parse it again
						const body_data = JSON.parse(response_body.body);
						const error_message = body_data.error;
						
						if (error_message) {
								console.error(error_message);
						} 
						
				} finally {
		        // Hide loading overlay
		        document.getElementById("loadingOverlay").style.display = "none";
            // Show retry modal
						this.retryModal.style.display = 'flex';
				}
		}

		const programme = await response.json();

		console.log(JSON.stringify(programme, null, 2));

		if (response) {
				localStorage.setItem("generatedProgramme", JSON.stringify(programme));

				// Hide overlay
				document.getElementById("loadingOverlay").style.display = "none";

        location.href='/programme/'
		}
	}*/

	async handleBuildProgramme() {
		// Show overlay
		document.getElementById("loadingOverlay").style.display = "flex";

		// Timeout promise that shows retry modal
		const timeout = new Promise(resolve =>
			setTimeout(() => {
				document.getElementById("loadingOverlay").style.display = "none";
				this.retryModal.style.display = 'flex';
				resolve(); // resolve instead of reject to avoid throwing
			}, 60000) // 60s timeout
		);

		try {
    await Promise.race([
      (async () => {
				// Show overlay
				document.getElementById("loadingOverlay").style.display = "flex";

				const result = await fetch('https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/populateExtraInfoJSON', {
					method: 'POST',
					headers: {
					'Content-Type': 'application/json',
					},
					body: JSON.stringify(this.chatHistory),
				});

				if (!result.ok) {
					throw new Error('LLM API error');
				}

				const extraPreferences = await result.json();

				this.userPreferences = { ...this.userPreferences, ...extraPreferences};
			
				const requiredKeys = ["days", "timePerSession", "equipment", "beginnerFriendly", "exerciseVariation", "excludedMuscleGroups", "preferredMuscleGroups"]
				for (const key of requiredKeys) {
					if (!(key in this.userPreferences)) {
						console.log(`Error: no ${key} key in userPreferences object`)
						this.userPreferences[key] = null;
					}
				}

				console.log(JSON.stringify(this.userPreferences, null, 2));

				// Now call lambda func to build programme
				const response = await fetch('https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/buildProgramme', {
					method: 'POST',
					headers: {
					'Content-Type': 'application/json',
					},
					body: JSON.stringify(this.userPreferences),
				});

				console.log(response.status)

				if (response.status !== 200) {
						try {
								const response_body = await response.json();
								
								// The body is a JSON string, so we need to parse it again
								const body_data = JSON.parse(response_body.body);
								const error_message = body_data.error;
								
								if (error_message) {
										console.error(error_message);
								} 
								
						} finally {
								// Hide loading overlay
								document.getElementById("loadingOverlay").style.display = "none";
								// Show retry modal
								this.retryModal.style.display = 'flex';
						}
				}

				const programme = await response.json();

				console.log(JSON.stringify(programme, null, 2));

				if (response) {
						localStorage.setItem("generatedProgramme", JSON.stringify(programme));

						// Hide overlay
						document.getElementById("loadingOverlay").style.display = "none";

						location.href='/programme/'
				}
			})(),
      timeout
    ]);

		} catch (err) {
			console.error(err.message);
			document.getElementById("loadingOverlay").style.display = "none";
			this.retryModal.style.display = 'flex';
		}

	}

    async sendMessage() {
        const messageText = this.messageInput.value.trim();
        if (!messageText) return;
        
        // Add user message
        this.addMessage(messageText, 'user', true);
        
        // Clear input
        this.messageInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Get bot response
        const response = await this.getAssistantResponse();

        this.hideTypingIndicator();

        this.addMessage(response, 'bot', true);
    }

	async getAssistantResponse() {
		// Call to AWS Lambda (via API Gateway endpoint)
		const response = await fetch('https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/getAIResponse', {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json',
			},
			body: JSON.stringify(this.chatHistory),
		});

		if (!response.ok) {
			throw new Error('LLM API error');
		}

		const data = await response.json();
		return data.reply; 
	}
    
    addMessage(text, sender, recordChatHistory=false, scrollToBottom=true) {
		if (recordChatHistory) {
			let role = "user";
			if (sender == "bot") {
				role = "assistant";
			}
			const chatEntry = {
				"role": role,
				"content": text
			};
			this.chatHistory.push(chatEntry);
		}
			
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${sender === 'user' ? 'You' : 'PT'}</div>
            <div class="message-content">
                <div class="message-text">${this.escapeHtml(text)}</div>
                <div class="message-time">${currentTime}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
		if (scrollToBottom) {
			this.scrollToBottom();
		}
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
                <div class="message-avatar">PT</div>
                <div class="message-content">
                    <div class="message-text">What days of the week do you want to train on?</div>
                    <div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                </div>
            </div>
        `;
        this.hideTypingIndicator();
        this.buildBtn.style.display = "none";
        this.chatMessageBox.style.display = "none";
        this.userPreferences = {};
        this.chatHistory = [];
        // Add days of the week input to chat
        this.setUpDaysInput();
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