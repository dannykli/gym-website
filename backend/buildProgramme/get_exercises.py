import json

def order_muscle_groups_sets(ordered_muscle_groups_sets, template_order = 
    ["chest", "middle back", "front delt", "quadriceps", "lats", "biceps", "triceps", "hamstrings", "lateral delt", 
    "abdominals", "rear delt", "calves", "forearms", "traps", "adductors", "lower back", "abductors", "glutes"]):
    new_ordered_muscle_groups = []
    for muscle_group in template_order:
        match = [(muscle, sets) for muscle, sets in ordered_muscle_groups_sets if muscle == muscle_group]
        if len(match) == 1:
            new_ordered_muscle_groups.append(match[0])
    return new_ordered_muscle_groups

def get_time_for_one_set(time_per_set, muslce_group, body_only):
    time = time_per_set[muslce_group]
    if body_only:
        time -= 1
    return time

def get_exercises(df, training_split, valid_muscle_groups, max_sets_per_muscle_per_day, 
    max_sets_per_muscle_per_week, time_per_set, variability_multiplier, time_per_session):

    result = {
        "workout_programme": [],
        "error": None
    }

    # Add new column to track how many times each exercise has been used so far
    df['no_of_uses'] = 0

    # Track sets per muscle per week to perform a final check that the porgramme meets the saftey/imbalance criteria
    sets_per_muscle_per_week = {}

    for muscle_group in valid_muscle_groups:
        sets_per_muscle_per_week[muscle_group] = 0

    # variable to track if a suitable programme is unable to be generated
    error_encountered = False

	# Retrieve exercises for the training split
    workout_programme = []
    for day_muscle_groups, is_modified in training_split:
        if error_encountered:
            break

        day_workout_exercises = []
        # Set column to track whether an exercise has been used in the daily workout to ensure repeat exercises don't occur
        df['used_in_workout'] = False 

        sets_per_muscle_per_day = {}
        for muscle_group in valid_muscle_groups:
            sets_per_muscle_per_day[muscle_group] = 0

        # variable for tracking current time the workout takes to complete
        time = 0

        finished_daily_workout = False
        while not finished_daily_workout:

            # First go through muscle groups in order and get the exercises
            for muscle_group, no_of_sets in day_muscle_groups:
                if time >= time_per_session:
                    finished_daily_workout = True
                    break

                possible_exercises_df = df[
                    (df['primary_muscle'] == muscle_group) 
                    & 
                    ~df['used_in_workout']
                ].copy()

                # If no eligible exercises or the maximum number of sets for the muscle_group has been reached,
                # then remove tuple from day muscle groups and go to next tuple
                if (len(possible_exercises_df) == 0 or 
                    sets_per_muscle_per_day[muscle_group] + no_of_sets > max_sets_per_muscle_per_day[muscle_group]):
                    day_muscle_groups.remove((muscle_group, no_of_sets))
                    print(f"Removed: {muscle_group, no_of_sets}")
                    continue
                    
                # Override no. of sets to 2 if time per session is <= 25 mins
                if time_per_session <= 25:
                    no_of_sets = 2

                # Add column to calculate suitability score = hypertrophy score - k * no. of uses
                possible_exercises_df['suitability_score'] = (possible_exercises_df['hypertrophy_score'] - 
                    possible_exercises_df['no_of_uses'] * variability_multiplier)
                max_score = possible_exercises_df['suitability_score'].max()

                # Get exercises with max suitability score
                possible_exercises_df = possible_exercises_df[possible_exercises_df['suitability_score'] == max_score]

                # Randomly select one of these exercises
                selected_exercise = possible_exercises_df.sample(n=1)

                exercise_name = selected_exercise['name'].iloc[0]
                # Increment no. of uses for the selected exercise and set used to true
                df.loc[df['name'] == exercise_name, 'no_of_uses'] += 1
                df.loc[df['name'] == exercise_name, 'used_in_workout'] = True

                body_only = selected_exercise['equipment'].iloc[0] == "body only"
                time += get_time_for_one_set(time_per_set, muscle_group, body_only) * no_of_sets

                # Add sets
                sets_per_muscle_per_day[muscle_group] += no_of_sets

                # Append exercise to daily workout
                day_workout_exercises.append((exercise_name, no_of_sets))

            # If not finished 
            if not finished_daily_workout:
                # If day split is unmodfified and close enough to required time, stop.
                # If muscle groups array has ran out, stop.
                if not is_modified and time > 0.75 * time_per_session or len(day_muscle_groups) == 0:
                    finished_daily_workout = True 
                # Otherwise reorder day muscle groups and continue adding exercises
                else:
                    day_muscle_groups = order_muscle_groups_sets(day_muscle_groups)
                    print(day_muscle_groups)
        
        for muscle_group, daily_sets in sets_per_muscle_per_day.items():
            sets_per_muscle_per_week[muscle_group] += daily_sets
        
        if time < 0.6 * time_per_session:
            print("Training split: ", training_split)
            print("Exercises: ", day_workout_exercises)
            error_encountered = True
            result["error"] = {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": 
                        "Error when generating the programme - "
                        "insufficient exercises to meet minimum daily standard"
                    })
            }
        
        workout_programme.append(day_workout_exercises)
    
    for muscle_group, weekly_sets in sets_per_muscle_per_week.items():
        print(muscle_group, weekly_sets)
        if weekly_sets > max_sets_per_muscle_per_week[muscle_group]:
            result["error"] = {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": 
                        "Error when generating the programme - "
                        "programme deemed imbalanced/unsafe"
                    })
            }
    
    result["workout_programme"] = workout_programme

    return result
    
