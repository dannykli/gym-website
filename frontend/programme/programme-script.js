
class ProgrammeDisplay {
    constructor() {
        this.weeklySchedule = document.getElementById('weeklySchedule');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.editBtn = document.getElementById('editBtn');
        this.databaseModal = document.getElementById('databaseModal');
        this.closeDatabaseModal = document.getElementById('closeDatabaseModal');
        this.exerciseList = document.getElementById('exerciseList');
        this.exerciseSearch = document.getElementById('exerciseSearch');
        this.exerciseDetailModal = document.getElementById('exerciseDetailModal');
        this.closeExerciseDetail = document.getElementById('closeExerciseDetail');
        this.muscleFilter = document.getElementById('muscleFilter');
        this.equipmentFilter = document.getElementById('equipmentFilter');
        this.beginnerFilter = document.getElementById('beginnerFilter');
        this.confirmExerciseModal = document.getElementById('confirmExerciseModal');
        this.closeConfirmModal = document.getElementById('closeConfirmModal');
        this.confirmMessage = document.getElementById('confirmMessage');
        this.confirmSets = document.getElementById('confirmSets');
        this.confirmExerciseBtn = document.getElementById('confirmExerciseBtn');
        
        this.editFirstTime = true;
        this.editMode = false;
        this.currentDay = null;
        this.currentExercise = null;
        
        // Sample programme data
        const jsonString = localStorage.getItem("generatedProgramme");
        this.programmeData = JSON.parse(jsonString || '{}');
        
        this.init();
    }
    
    init() {
        this.renderProgramme();
        this.attachEventListeners();
    }
    
    attachEventListeners() {
        this.downloadBtn.addEventListener('click', () => this.downloadProgramme());
        this.editBtn.addEventListener('click', () => this.toggleEditMode());
        this.closeDatabaseModal.addEventListener('click', () => this.closeModal());
        this.closeExerciseDetail.addEventListener('click', () => this.closeExerciseDetailModal());
        this.muscleFilter.addEventListener('change', () => this.renderExerciseList());
        this.equipmentFilter.addEventListener('change', () => this.renderExerciseList());
        this.beginnerFilter.addEventListener('change', () => this.renderExerciseList());
        
        window.addEventListener('click', (event) => {
            if (event.target === this.confirmExerciseModal) {
                this.confirmExerciseModal.style.display = 'none';
            }
            if (event.target === this.databaseModal) {
                this.closeModal();
            }
            if (event.target === this.exerciseDetailModal) {
                this.closeExerciseDetailModal();
            }
        });

        // Search functionality
        this.exerciseSearch.addEventListener('input', () => this.filterExercises());

        this.closeConfirmModal.addEventListener('click', () => {
            this.confirmExerciseModal.style.display = 'none';
        });

        this.confirmExerciseBtn.addEventListener('click', () => {
            if (this.isDelete) {
                this.deleteExercise();
                this.isDelete = false;
            } else {
                const sets = Math.min(9, Math.max(1, parseInt(this.confirmSets.value) || 3));

                const formattedExercise = {
                    id: this.selectedExercise.id,
                    name: this.selectedExercise.name,
                    rep_range: this.selectedExercise.rep_range,
                    no_of_sets: sets,
                    primary_muscle: this.selectedExercise.primary_muscle
                };

                if (this.isSwap) {
                    this.swapExercise(this.currentDay, this.currentExercise.id, formattedExercise);
                } else {
                    this.addExerciseToDay(this.currentDay, formattedExercise);
                }
            }

            this.confirmExerciseModal.style.display = 'none';
            this.closeModal(); // close the database modal too
        });

    }
    
    renderProgramme() {
        const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        
        this.weeklySchedule.innerHTML = '';
        
        days.forEach((day, index) => {
            const dayColumn = this.createDayColumn(dayNames[index], day, this.programmeData[day]);
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
        if (muscle === "lats" || muscle === "middle back") {
            muscle = "back";
        } else if (muscle === "abdominals") {
            muscle = "abs"
        } else if (muscle === "quadriceps") {
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
            this.confirmMessage.innerHTML = `Delete <strong id="exercise">${exercise.name}</strong> on <strong>${this.capitalizeFirstLetter(dayKey)}</strong>?`;
            document.getElementById('confirmSets').style.display = 'none';
            document.querySelector('label[for="confirmSets"]').style.display = 'none';
            this.isDelete = true;
            this.dayKey = dayKey;
            this.deletedExercise = exercise;
            this.confirmExerciseModal.style.display = 'flex';
        });
        
        editControls.appendChild(swapBtn);
        editControls.appendChild(deleteBtn);
        
        card.appendChild(exerciseName);
        card.appendChild(exerciseDetails);
        card.appendChild(editControls);

        card.addEventListener('click', () => {
            this.openExerciseDetailModal(exercise.id, exercise.no_of_sets);
        });

        return card;
    }
    
    capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    
    async downloadProgramme() {
        const viewportWidth = window.innerWidth;

        if (viewportWidth <= 1400) {
            // Small screen → use PNG for continuous content
            this.downloadAsPNG();
        } else {
            // Large screen → PDF is fine
            this.downloadAsPDF();
        }
    }

    async downloadAsPDF() {
        const { jsPDF } = window.jspdf;
        const element = document.getElementById("programmeContent");
        
        // Use html2canvas to capture
        const canvas = await html2canvas(element, { scale: 2 });
        const imgData = canvas.toDataURL("image/png");

        // Create PDF
        const pdf = new jsPDF("p", "mm", "a4");
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

        pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
        pdf.save("fitness-programme.pdf");
    }

    async downloadAsPNG() {
        const element = document.getElementById("programmeContent");

        // Capture the entire container
        const canvas = await html2canvas(element, {
            scale: 2, 
            scrollY: -window.scrollY, // ensures full content is captured even if scrolled
        });

        // Convert canvas to PNG data
        const imgData = canvas.toDataURL("image/png");

        // Trigger download
        const link = document.createElement("a");
        link.href = imgData;
        link.download = "fitness-programme.png";
        link.click();
    }
    
    async toggleEditMode() {
        if (this.editFirstTime) {
            // Show overlay
            document.getElementById("loadingOverlay").style.display = "flex";
            // load database
            await this.loadExerciseDatabase();
            this.processLoadedExerciseDatabase();
            this.editFirstTime = false;
        }
        this.editMode = !this.editMode;
        document.body.classList.toggle('edit-mode');
        this.editBtn.textContent = this.editMode ? 'Done Editing' : 'Edit';
        this.renderProgramme();
        // Hide overlay
        document.getElementById("loadingOverlay").style.display = "none";
    }

    async loadExerciseDatabase() {
        try {
            const response = await fetch("https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/getMinimalExercisesFromDatabase");
            if (!response.ok) {
                throw new Error("Database Load Error");
            }
            const data = await response.json();
            this.exerciseDatabase = data.exercises;
        } catch (err) {
            console.error("Error fetching exercises:", err);
        }
    }

    processLoadedExerciseDatabase() {
        for (const exercise of this.exerciseDatabase) {
            // primary muscle
            if (exercise.primary_muscle === "middle back" || exercise.primary_muscle === "lats") {
                exercise.primary_muscle = "back";
            } else if (exercise.primary_muscle === "abdominals") {
                exercise.primary_muscle = "abs";
            } else if (exercise.primary_muscle === "quadriceps") {
                exercise.primary_muscle = "quads";
            } 

            // equipment
            if (exercise.equipment == "body only") {
                if (exercise.pull_up_bar_required) {
                    exercise.equipment = "Pull-Up bar";
                } else {
                    exercise.equipment = "bodyweight";
                }
            } else if (exercise.equipment === "e-z curl bar") {
                exercise.equipment = "EZ curl bar";
            } else if (exercise.equipment === "kettlebells") {
                exercise.equipment = "Kettlebell";
            }
        }
    }
    
    openDatabaseModal(dayKey, isSwap = false) {
        this.currentDay = dayKey;
        this.isSwap = isSwap;
        this.databaseModal.style.display = 'flex';
        this.renderExerciseList();
    }

    async openExerciseDetailModal(exerciseId, exerciseSets) {
        
        try {
            // Show overlay
            document.getElementById("loadingOverlay").style.display = "flex";

            const result = await fetch('https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/getExerciseFromDatabase', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({ exerciseId }),
            });

            if (!result.ok) {
                throw new Error('Database query error');
            }

            const exercise = await result.json();

            console.log(exercise);

            const equipment = this.capitalizeFirstLetter(exercise.equipment) + ((exercise.bench_required) ? ", Bench" : "") + ((exercise.pull_up_bar_required) ? ", Pull-Up bar" : "");
            
            // Fill text info
            document.getElementById('detailName').textContent = exercise.name;
            document.getElementById('detailSets').textContent = exerciseSets;
            document.getElementById('detailReps').textContent = exercise.rep_range;
            document.getElementById('detailPrimary').textContent = this.capitalizeFirstLetter(exercise.primary_muscle);
            document.getElementById('detailSecondary').textContent = exercise.secondary_muscles.map(muscle => this.capitalizeFirstLetter(muscle))?.join(", ") || "None";
            document.getElementById('detailBeginner').textContent = exercise.beginner_friendly ? "Yes" : "No";
            document.getElementById('detailEquipment').textContent = equipment;
            const instructionList = document.getElementById('detailInstructions');

            // Clear previous instructions
            instructionList.innerHTML = '';

            // Add each instruction as a list item
            exercise.instructions.forEach(inst => {
                const li = document.createElement('li');
                li.textContent = inst;
                instructionList.appendChild(li);
            });

            // Images (carousel)
            const images = exercise.images.map(img => "../exercise-images/" + img);
            const track = document.getElementById('detailImageTrack');
            track.innerHTML = "";
            images.forEach(imgUrl => {
                const img = document.createElement('img');
                img.src = imgUrl;
                track.appendChild(img);
            });

            let currentIndex = 0;
            const prevBtn = document.getElementById('prevImage');
            const nextBtn = document.getElementById('nextImage');

            const updateCarousel = () => {
                track.style.transform = `translateX(-${currentIndex * 100}%)`;
            };

            prevBtn.onclick = () => {
                currentIndex = (currentIndex === 0) ? exercise.images.length - 1 : currentIndex - 1;
                updateCarousel();
            };

            nextBtn.onclick = () => {
                currentIndex = (currentIndex + 1) % exercise.images.length;
                updateCarousel();
            };

            // Video
            const videoContainer = document.getElementById('detailVideoContainer');
            videoContainer.innerHTML = exercise.video 
                ? `<iframe src="${exercise.video}" frameborder="0" allowfullscreen></iframe>`
                : "<p>No video available.</p>";

            // Hide overlay
            document.getElementById("loadingOverlay").style.display = "none";

            // Show modal
            this.exerciseDetailModal.style.display = 'flex';
        } catch {
            console.error("Error fetching exercise:", err);
        }
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

        const searchTerm = this.exerciseSearch.value.toLowerCase();
        const muscle = this.muscleFilter.value;
        const equipment = this.equipmentFilter.value;
        const beginner = this.beginnerFilter.value;
        
        this.exerciseDatabase
            .filter(exercise => {
                const matchesSearch = exercise.name.toLowerCase().includes(searchTerm);
                const matchesMuscle = !muscle || exercise.primary_muscle === muscle;
                const matchesEquipment = !equipment || exercise.equipment === equipment;
                const matchesBeginner = !beginner || exercise.beginner_friendly?.toString() === beginner;

                return matchesSearch && matchesMuscle && matchesEquipment && matchesBeginner;
            })
            .forEach(exercise => {
                const exerciseItem = document.createElement('div');
                exerciseItem.className = 'exercise-item';
                exerciseItem.setAttribute('data-exercise-id', exercise.id);

                let beginnerTag = '';
                if (exercise.beginner_friendly) {
                    beginnerTag = `<span class="tag beginner">Beginner friendly</span>`;
                }

                exerciseItem.innerHTML = `
                    <div>
                        <div class="exercise-name">${exercise.name}</div>
                        <div class="exercise-tags">
                            <span class="tag muscle">${this.capitalizeFirstLetter(exercise.primary_muscle)}</span>
                            <span class="tag equipment">${this.capitalizeFirstLetter(exercise.equipment)}</span>
                            ${beginnerTag}
                        </div>
                    </div>
                    <button class="action-btn select-exercise">Select</button>
                `;

                const selectBtn = exerciseItem.querySelector('.select-exercise');

                selectBtn.addEventListener('click', () => {
                    this.selectedExercise = exercise; // store exercise

                    if (this.isSwap) {
                        this.confirmMessage.innerHTML =
                            `Swap <strong id="exercise">${this.currentExercise.name}</strong> with <strong id="exercise">${exercise.name}</strong> on <strong>${this.capitalizeFirstLetter(this.currentDay)}</strong>?`;
                    } else {
                        this.confirmMessage.innerHTML =
                            `Add <strong id="exercise">${exercise.name}</strong> to <strong>${this.capitalizeFirstLetter(this.currentDay)}</strong>?`;
                    }

                    this.confirmSets.value = 3; // default
                    this.confirmExerciseModal.style.display = 'flex';
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
    
    deleteExercise() {
        this.programmeData[this.dayKey] = this.programmeData[this.dayKey].filter(ex => ex.id !== this.deletedExercise.id);
        
        // If no exercises left, set day to rest
        if (this.programmeData[this.dayKey].length === 0) {
            this.programmeData[this.dayKey] = "rest";
        }
        
        this.renderProgramme();
    }
    
    swapExercise(dayKey, oldExerciseId, newExercise) {
        const index = this.programmeData[dayKey].findIndex(ex => ex.id === oldExerciseId);
        if (index !== -1) {
            this.programmeData[dayKey][index] = newExercise;
            this.renderProgramme();
        }
    }
}

// Initialize the programme display
document.addEventListener('DOMContentLoaded', () => {
    const programmeDisplay = new ProgrammeDisplay();
});