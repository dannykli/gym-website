let supabase;

class ExerciseBrowseDisplay {
    
    constructor() {
        this.exerciseList = document.getElementById('exerciseList');
        this.exerciseSearch = document.getElementById('exerciseSearch');
        this.exerciseDetailModal = document.getElementById('exerciseDetailModal');
        this.closeExerciseDetail = document.getElementById('closeExerciseDetail');
        this.muscleFilter = document.getElementById('muscleFilter');
        this.equipmentFilter = document.getElementById('equipmentFilter');
        this.beginnerFilter = document.getElementById('beginnerFilter');

        this.setsPerMuscle = {
            "abdominals": 3,
            "abductors": 2,
            "adductors": 2,
            "biceps": 3,
            "front delt": 3,
            "lateral delt": 3,
            "rear delt": 3,
            "calves": 4,
            "chest": 3,
            "forearms": 3,
            "glutes": 3,
            "hamstrings": 3,
            "quadriceps": 3,
            "lower back": 2,
            "middle back": 3,
            "lats": 3,
            "traps": 3,
            "triceps": 3
        }
      
        this.init();
    }
    
    async init() {
        this.attachEventListeners();
        await this.loadExerciseDatabase();
        this.processLoadedExerciseDatabase();
        this.renderExerciseList();
    }
    
    attachEventListeners() {
        this.closeExerciseDetail.addEventListener('click', () => this.closeExerciseDetailModal());
        this.muscleFilter.addEventListener('change', () => this.renderExerciseList());
        this.equipmentFilter.addEventListener('change', () => this.renderExerciseList());
        this.beginnerFilter.addEventListener('change', () => this.renderExerciseList());
        
        window.addEventListener('click', (event) => {
            if (event.target === this.exerciseDetailModal) {
                this.closeExerciseDetailModal();
            }
        });

        // Search functionality
        this.exerciseSearch.addEventListener('input', () => this.filterExercises());
    }
    
    
    capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    async loadExerciseDatabase() {
        // Show overlay
        document.getElementById("loadingOverlay").style.display = "flex";
        /*
        try {
            const response = await fetch("https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/getMinimalExercisesFromDatabase");
            if (!response.ok) {
                throw new Error("Database Load Error");
            }
            const data = await response.json();
            this.exerciseDatabase = data.exercises;
        } catch (err) {
            console.error("Error fetching exercises:", err);
        }*/


        try {
            const { data, error } = await supabase
                .from('exercises')
                .select('id, name, primary_muscle, beginner_friendly, equipment, rep_range')
                .eq('hidden', false) 
                .order('name');    

            if (error) {
                throw error;
            }

            this.exerciseDatabase = data;  // assign to your state
        } catch (err) {
            console.error("Error fetching exercises:", err);
        }
    }

    processLoadedExerciseDatabase() {
        for (const exercise of this.exerciseDatabase) {
            // primary muscle
            if (exercise.primary_muscle == "middle back" || exercise.primary_muscle == "lats") {
                exercise.primary_muscle = "back";
                console.log("processDB " + exercise.primary_muscle);
            } else if (exercise.primary_muscle == "abdominals") {
                exercise.primary_muscle = "abs";
            } else if (exercise.primary_muscle == "quadriceps") {
                exercise.primary_muscle = "quads";
            } 

            // equipment
            if (exercise.equipment == "body only") {
                if (exercise.pull_up_bar_required) {
                    exercise.equipment = "Pull-Up bar";
                } else {
                    exercise.equipment = "bodyweight";
                }
            } else if (exercise.equipment == "e-z curl bar") {
                exercise.equipment = "EZ curl bar";
            } else if (exercise.equipment == "kettlebells") {
                exercise.equipment = "Kettlebell";
            }

        }

        // Hide loading overlay
        document.getElementById("loadingOverlay").style.display = "none";
    }

    async openExerciseDetailModal(exerciseId) {
        try {
            // Show overlay
            
            document.getElementById("loadingOverlay").style.display = "flex";
            /*
            const result = await fetch('https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/getExerciseFromDatabase', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({ exerciseId }),
            });

            if (!result.ok) {
                throw new Error('Database query error');

            const exercise = await result.json();
            }*/

            const { data: exercise, error } = await supabase
                .from('exercises')
                .select('*')
                .eq('id', exerciseId)  
                .single()

            if (error) {
                throw error;
            }

            console.log(exercise);

            const equipment = this.capitalizeFirstLetter(exercise.equipment) + ((exercise.bench_required) ? ", Bench" : "") + ((exercise.pull_up_bar_required) ? ", Pull-Up bar" : "");
            
            // Fill text info
            document.getElementById('detailName').textContent = exercise.name;
            document.getElementById('detailSets').textContent = this.setsPerMuscle[exercise.primary_muscle];
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
            const images = exercise.images.map(img => "/exercise-images/" + img);
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
            console.error("Error fetching exercise");
        }
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
                    <button class="action-btn select-exercise">View details</button>
                `;

                const selectBtn = exerciseItem.querySelector('.select-exercise');

                selectBtn.addEventListener('click', () => {
                    this.openExerciseDetailModal(exercise.id);
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
}

// Initialize the programme display
document.addEventListener('DOMContentLoaded', () => {
    const PROJECT_URL = 'https://kufcgisrdhtdrggoovan.supabase.co';
    const ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt1ZmNnaXNyZGh0ZHJnZ29vdmFuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY3NjMyNDEsImV4cCI6MjA3MjMzOTI0MX0.-GvscoYdhH5teJkuDcB0a9JVlyX-5fHibuP2pCfSpdE';
    supabase = window.supabase.createClient(PROJECT_URL, ANON_KEY);
    const programmeDisplay = new ExerciseBrowseDisplay();
});

