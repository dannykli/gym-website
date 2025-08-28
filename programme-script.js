
        class ProgrammeDisplay {
            constructor() {
                this.weeklySchedule = document.getElementById('weeklySchedule');
                this.printBtn = document.getElementById('printBtn');
                this.editBtn = document.getElementById('editBtn');
                this.databaseModal = document.getElementById('databaseModal');
                this.closeDatabaseModal = document.getElementById('closeDatabaseModal');
                this.exerciseList = document.getElementById('exerciseList');
                this.exerciseSearch = document.getElementById('exerciseSearch');
                this.exerciseDetailModal = document.getElementById('exerciseDetailModal');
                this.closeExerciseDetail = document.getElementById('closeExerciseDetail');

                
                this.editMode = false;
                this.currentDay = null;
                this.currentExercise = null;
                
                // Sample programme data
                const jsonString = localStorage.getItem("generatedProgramme");
                this.programmeData = JSON.parse(jsonString);

                console.log(this.programmeData);
                
                /*
                this.programmeData = {
                    "monday": [
                        {
                            "id": 1,
                            "name": "Barbell Bench Press",
                            "rep_range": "8-12",
                            "no_of_sets": 3,
                            "primary_muscle": "chest"
                        },
                        {
                            "id": 2,
                            "name": "Incline Dumbbell Press",
                            "rep_range": "10-15",
                            "no_of_sets": 3,
                            "primary_muscle": "chest"
                        },
                        {
                            "id": 3,
                            "name": "Tricep Dips",
                            "rep_range": "12-15",
                            "no_of_sets": 3,
                            "primary_muscle": "triceps"
                        }
                    ],
                    "tuesday": "rest",
                    "wednesday": [
                        {
                            "id": 4,
                            "name": "Deadlift",
                            "rep_range": "5-8",
                            "no_of_sets": 4,
                            "primary_muscle": "back"
                        },
                        {
                            "id": 5,
                            "name": "Pull-ups",
                            "rep_range": "8-12",
                            "no_of_sets": 3,
                            "primary_muscle": "back"
                        },
                        {
                            "id": 6,
                            "name": "Barbell Rows",
                            "rep_range": "10-12",
                            "no_of_sets": 3,
                            "primary_muscle": "back"
                        }
                    ],
                    "thursday": "rest",
                    "friday": [
                        {
                            "id": 7,
                            "name": "Squats",
                            "rep_range": "8-12",
                            "no_of_sets": 4,
                            "primary_muscle": "legs"
                        },
                        {
                            "id": 8,
                            "name": "Romanian Deadlift",
                            "rep_range": "10-15",
                            "no_of_sets": 3,
                            "primary_muscle": "hamstrings"
                        },
                        {
                            "id": 9,
                            "name": "Calf Raises",
                            "rep_range": "15-20",
                            "no_of_sets": 4,
                            "primary_muscle": "calves"
                        }
                    ],
                    "saturday": "rest",
                    "sunday": "rest"
                };*/
                
                // Sample exercise database
                this.exerciseDatabase = [
                    {
                        "id": 1,
                        "name": "Barbell Bench Press",
                        "rep_range": "8-12",
                        "no_of_sets": 3,
                        "primary_muscle": "chest"
                    },
                    {
                        "id": 2,
                        "name": "Incline Dumbbell Press",
                        "rep_range": "10-15",
                        "no_of_sets": 3,
                        "primary_muscle": "chest"
                    },
                    {
                        "id": 3,
                        "name": "Tricep Dips",
                        "rep_range": "12-15",
                        "no_of_sets": 3,
                        "primary_muscle": "triceps"
                    },
                    {
                        "id": 4,
                        "name": "Deadlift",
                        "rep_range": "5-8",
                        "no_of_sets": 4,
                        "primary_muscle": "back"
                    },
                    {
                        "id": 5,
                        "name": "Pull-ups",
                        "rep_range": "8-12",
                        "no_of_sets": 3,
                        "primary_muscle": "back"
                    },
                    {
                        "id": 6,
                        "name": "Barbell Rows",
                        "rep_range": "10-12",
                        "no_of_sets": 3,
                        "primary_muscle": "back"
                    },
                    {
                        "id": 7,
                        "name": "Squats",
                        "rep_range": "8-12",
                        "no_of_sets": 4,
                        "primary_muscle": "legs"
                    },
                    {
                        "id": 8,
                        "name": "Romanian Deadlift",
                        "rep_range": "10-15",
                        "no_of_sets": 3,
                        "primary_muscle": "hamstrings"
                    },
                    {
                        "id": 9,
                        "name": "Calf Raises",
                        "rep_range": "15-20",
                        "no_of_sets": 4,
                        "primary_muscle": "calves"
                    },
                    {
                        "id": 10,
                        "name": "Dumbbell Curls",
                        "rep_range": "10-12",
                        "no_of_sets": 3,
                        "primary_muscle": "biceps"
                    },
                    {
                        "id": 11,
                        "name": "Shoulder Press",
                        "rep_range": "8-12",
                        "no_of_sets": 3,
                        "primary_muscle": "shoulders"
                    },
                    {
                        "id": 12,
                        "name": "Lunges",
                        "rep_range": "10-12",
                        "no_of_sets": 3,
                        "primary_muscle": "legs"
                    }
                ];
                
                this.init();
            }
            
            init() {
                this.renderProgramme();
                this.attachEventListeners();
            }
            
            attachEventListeners() {
                this.printBtn.addEventListener('click', () => this.printProgramme());
                this.editBtn.addEventListener('click', () => this.toggleEditMode());
                this.closeDatabaseModal.addEventListener('click', () => this.closeModal());
                this.closeExerciseDetail.addEventListener('click', () => this.closeExerciseDetailModal());
                
                // Close exercise search modal when clicking outside
                window.addEventListener('click', (event) => {
                    if (event.target === this.databaseModal) {
                        this.closeModal();
                    }
                });

                // Close exercise detail modal when clicking outside
                window.addEventListener('click', (event) => {
                    if (event.target === this.exerciseDetailModal) {
                      this.closeExerciseDetailModal();
                    }
                });
                                  
                // Search functionality
                this.exerciseSearch.addEventListener('input', () => this.filterExercises());
            }
            
            renderProgramme() {
                const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
                const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                
                this.weeklySchedule.innerHTML = '';
                
                days.forEach((day, index) => {
                    console.log(this.programmeData);
                    console.log(day);
                    console.log(this.programmeData[day]);
                    const dayColumn = this.createDayColumn(dayNames[index], day, this.programmeData[day]);
                    console.log(dayColumn);
                    this.weeklySchedule.appendChild(dayColumn);
                });
            }
            
            createDayColumn(dayName, dayKey, dayData) {
                const dayColumn = document.createElement('div');
                dayColumn.className = 'day-column';
                dayColumn.setAttribute('data-day', dayKey);
                
                const dayHeader = document.createElement('div');
                dayHeader.className = 'day-header';
                dayHeader.textContent = dayName;
                
                const dayContent = document.createElement('div');
                dayContent.className = 'day-content';
                
                if (dayData === 'rest') {
                    const restDay = document.createElement('div');
                    restDay.className = 'rest-day';
                    restDay.textContent = 'Rest Day';
                    dayContent.appendChild(restDay);
                    
                    if (this.editMode) {
                        const makeWorkoutBtn = document.createElement('button');
                        makeWorkoutBtn.className = 'add-exercise-btn';
                        makeWorkoutBtn.innerHTML = '<i class="fas fa-plus"></i> Add Exercises';
                        makeWorkoutBtn.addEventListener('click', () => {
                            this.openDatabaseModal(dayKey);
                        });
                        dayContent.appendChild(makeWorkoutBtn);
                    }
                } else if (Array.isArray(dayData)) {
                    dayData.forEach(exercise => {
                        const exerciseCard = this.createExerciseCard(exercise, dayKey);
                        dayContent.appendChild(exerciseCard);
                    });
                    
                    if (this.editMode) {
                        const addExerciseBtn = document.createElement('button');
                        addExerciseBtn.className = 'add-exercise-btn';
                        addExerciseBtn.innerHTML = '<i class="fas fa-plus"></i> Add Exercise';
                        addExerciseBtn.addEventListener('click', () => {
                            this.openDatabaseModal(dayKey);
                        });
                        dayContent.appendChild(addExerciseBtn);
                    }
                }
                
                dayColumn.appendChild(dayHeader);
                dayColumn.appendChild(dayContent);
                
                return dayColumn;
            }
            
            createExerciseCard(exercise, dayKey) {
                const card = document.createElement('div');
                card.className = 'exercise-card';
                card.setAttribute('data-exercise-id', exercise.id);
                
                const exerciseName = document.createElement('div');
                exerciseName.className = 'exercise-name';
                exerciseName.textContent = exercise.name;
                
                const exerciseDetails = document.createElement('div');
                exerciseDetails.className = 'exercise-details';
                
                const setsReps = document.createElement('span');
                setsReps.className = 'exercise-sets-reps';
                setsReps.textContent = `${exercise.no_of_sets} x ${exercise.rep_range}`;
                
                const muscleGroup = document.createElement('span');
                muscleGroup.className = 'exercise-muscle';
                
                let muscle = exercise.primary_muscle;
                if (muscle == "lats" || muscle == "middle back") {
                    muscle = "back";
                } else if (muscle == "abdominals") {
                    muscle = "abs"
                } else if (muscle == "quadriceps") {
                    muscle = "quads"
                } 
                muscleGroup.textContent = this.capitalizeFirstLetter(muscle);
                
                exerciseDetails.appendChild(setsReps);
                exerciseDetails.appendChild(muscleGroup);
                
                // Edit controls
                const editControls = document.createElement('div');
                editControls.className = 'edit-controls';
                
                const swapBtn = document.createElement('button');
                swapBtn.className = 'edit-btn swap';
                swapBtn.innerHTML = '<i class="fas fa-exchange-alt"></i>';
                swapBtn.setAttribute('data-action', 'swap');
                swapBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.currentExercise = exercise;
                    this.openDatabaseModal(dayKey, true);
                });
                
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'edit-btn delete';
                deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
                deleteBtn.setAttribute('data-action', 'delete');
                deleteBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.deleteExercise(dayKey, exercise.id);
                });
                
                editControls.appendChild(swapBtn);
                editControls.appendChild(deleteBtn);
                
                card.appendChild(exerciseName);
                card.appendChild(exerciseDetails);
                card.appendChild(editControls);

                card.addEventListener('click', () => {
                    this.openExerciseDetailModal(exercise.id);
                });

                return card;
            }
            
            capitalizeFirstLetter(string) {
                return string.charAt(0).toUpperCase() + string.slice(1);
            }
            
            printProgramme() {
                window.print();
            }
            
            toggleEditMode() {
                this.editMode = !this.editMode;
                document.body.classList.toggle('edit-mode');
                this.editBtn.textContent = this.editMode ? 'Done Editing' : 'Edit';
                this.renderProgramme();
            }
            
            openDatabaseModal(dayKey, isSwap = false) {
                this.currentDay = dayKey;
                this.isSwap = isSwap;
                this.databaseModal.style.display = 'flex';
                this.renderExerciseList();
            }

            openExerciseDetailModal(exerciseId) { 
                this.exerciseDetailModal.style.display = 'flex';
            }
            
            closeModal() {
                this.databaseModal.style.display = 'none';
                this.exerciseSearch.value = '';
            }

            closeExerciseDetailModal() {
                this.exerciseDetailModal.style.display = 'none';
            }
            
            renderExerciseList() {
                this.exerciseList.innerHTML = '';
                
                this.exerciseDatabase.forEach(exercise => {
                    const exerciseItem = document.createElement('div');
                    exerciseItem.className = 'exercise-item';
                    exerciseItem.setAttribute('data-exercise-id', exercise.id);
                    
                    exerciseItem.innerHTML = `
                        <div>
                            <div class="exercise-name">${exercise.name}</div>
                            <div>${this.capitalizeFirstLetter(exercise.primary_muscle)} • ${exercise.no_of_sets} x ${exercise.rep_range}</div>
                        </div>
                        <button class="action-btn select-exercise">Select</button>
                    `;
                    
                    exerciseItem.querySelector('.select-exercise').addEventListener('click', () => {
                        if (this.isSwap) {
                            this.swapExercise(this.currentDay, this.currentExercise.id, exercise);
                        } else {
                            this.addExerciseToDay(this.currentDay, exercise);
                        }
                        this.closeModal();
                    });
                    
                    this.exerciseList.appendChild(exerciseItem);
                });
            }
            
            filterExercises() {
                const searchTerm = this.exerciseSearch.value.toLowerCase();
                const items = this.exerciseList.querySelectorAll('.exercise-item');
                
                items.forEach(item => {
                    const name = item.querySelector('.exercise-name').textContent.toLowerCase();
                    if (name.includes(searchTerm)) {
                        item.style.display = 'flex';
                    } else {
                        item.style.display = 'none';
                    }
                });
            }
            
            addExerciseToDay(dayKey, exercise) {
                if (this.programmeData[dayKey] === "rest") {
                    this.programmeData[dayKey] = [exercise];
                } else {
                    this.programmeData[dayKey].push(exercise);
                }
                this.renderProgramme();
            }
            
            deleteExercise(dayKey, exerciseId) {
                if (confirm("Are you sure you want to remove this exercise?")) {
                    this.programmeData[dayKey] = this.programmeData[dayKey].filter(ex => ex.id !== exerciseId);
                    
                    // If no exercises left, set day to rest
                    if (this.programmeData[dayKey].length === 0) {
                        this.programmeData[dayKey] = "rest";
                    }
                    
                    this.renderProgramme();
                }
            }
            
            swapExercise(dayKey, oldExerciseId, newExercise) {
                const index = this.programmeData[dayKey].findIndex(ex => ex.id === oldExerciseId);
                if (index !== -1) {
                    this.programmeData[dayKey][index] = newExercise;
                    this.renderProgramme();
                }
            }
            
            // Method to update programme data (for integration with your app)
            updateProgrammeData(newData) {
                this.programmeData = newData;
                this.renderProgramme();
            }
        }

        // Initialize the programme display
        document.addEventListener('DOMContentLoaded', () => {
            const programmeDisplay = new ProgrammeDisplay();
            
            // Example of how to update with new data
            // programmeDisplay.updateProgrammeData(yourProgrammeData);
        });

        // Utility function to load programme data from external source
        function loadProgrammeData(data) {
            const display = new ProgrammeDisplay();
            display.updateProgrammeData(data);
        }