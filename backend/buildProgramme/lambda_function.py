import json
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

from .get_training_split import get_1_day_training_split
from .get_training_split import get_2_day_training_split
from .get_training_split import get_3_day_training_split
from .get_training_split import get_4_day_training_split
from .get_training_split import get_5_day_training_split
from .get_training_split import get_6_day_training_split

from .validate_user_preferences import validate_excluded_muscle_groups
from .validate_user_preferences import validate_preferred_muscle_groups
from .validate_user_preferences import validate_equipment
from .validate_user_preferences import validate_excluded_exercises

# Temporary main to test lambda function
user_preferences = {
    "days": ["monday"],
    "timePerSession": 
}

def lambda_handler(event, context):
    # TODO implement
    try:
        user_preferences = json.loads(event["body"])
        
    except (KeyError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid or missing JSON body"})
        }

    # Load environment variables from the .env file
    load_dotenv()

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    engine = create_engine(DATABASE_URL)

    valid_muscle_groups = ["abdominals", "abductors", "adductors", "biceps", "front delt", "lateral delt", "rear delt",
                   "calves", "chest", "forearms", "glutes", "hamstrings", "quadriceps", "lower back",
                   "middle back", "lats", "traps", "triceps"]
    
    valid_equipment = ["body only", "bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "medicine ball", "dip bar", "dumbbell"]
    

    sets_per_muscle = {
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

    time_per_set = {
        "abdominals": 2.5,
        "abductors": 3,
        "adductors": 3,
        "biceps": 3,
        "front delt": 3.5,
        "lateral delt": 2.5,
        "rear delt": 2.5,
        "calves": 3,
        "chest": 4,
        "forearms": 2.5,
        "glutes": 3.5,
        "hamstrings": 3.5,
        "quadriceps": 4,
        "lower back": 3,
        "middle back": 4,
        "lats": 3.5,
        "traps": 2.5,
        "triceps": 3
    }

    max_sets_per_muscle_per_day = {
        "abdominals": 12,
        "abductors": 6,
        "adductors": 6,
        "biceps": 10,
        "front delt": 6,
        "lateral delt": 6,
        "rear delt": 6,
        "calves": 9,
        "chest": 12,
        "forearms": 9,
        "glutes": 18,
        "hamstrings": 12,
        "quadriceps": 15,
        "lower back": 6,
        "middle back": 12,
        "lats": 12,
        "traps": 6,
        "triceps": 10
    }

    # used to validate safety/imbalances of final programme
    max_sets_per_muscle_per_week = {
        "abdominals": 25,
        "abductors": 15,
        "adductors": 15,
        "biceps": 21,
        "front delt": 15,
        "lateral delt": 18,
        "rear delt": 12,
        "calves": 25,
        "chest": 27,
        "forearms": 20,
        "glutes": 30,
        "hamstrings": 25,
        "quadriceps": 28,
        "lower back": 15,
        "middle back": 21,
        "lats": 21,
        "traps": 16,
        "triceps": 21
    }

    min_num_eligible_muscle_groups = {
        1: 3,
        2: 5,
        3: 6,
        4: 7,
        5: 8,
        6: 8
    }

    no_of_days = len(user_preferences["days"])
    time_per_session = user_preferences["timePerSession"]
    equipment = user_preferences["equipment"]
    beginner_friendly = user_preferences["beginnerFriendly"]
    variability_multiplier = user_preferences["exerciseVariation"]
    excluded_muscle_groups = user_preferences["excludedMuscleGroups"]
    excluded_exercises = user_preferences["excludedExercises"]
    preferred_muscle_groups = user_preferences["preferredMuscleGroups"]

	# Validate user preferences
    validate_equipment(equipment, valid_equipment)
    validate_excluded_muscle_groups(excluded_muscle_groups, valid_muscle_groups)
    validate_preferred_muscle_groups(preferred_muscle_groups, excluded_muscle_groups, valid_muscle_groups)

    # Order preferred_muscle_groups to prioritise more important muscles
    preferred_muscle_groups = reOrderMuscleGroups(preferred_muscle_groups)
    
    # Get exercises from database
    pull_up_bar_clause = "AND NOT pull_up_bar_required" if "pull up bar" not in equipment else ""
    bench_clause = "AND NOT bench_required" if "bench" not in equipment else ""
    beginner_clause = "AND beginner_friendly" if beginner_friendly else ""

    query = f'''
        SELECT name, mechanic, equipment, primary_muscle, secondary_muscles, 
            beginner_friendly, instructions, images, hypertrophy_score, 
            rep_range, bench_required, pull_up_bar_required
        FROM exercises
        WHERE NOT hidden 
            AND equipment = ANY(:equipment) 
            AND primary_muscle != ALL(:excluded_muscles) 
            {beginner_clause}
            {pull_up_bar_clause}
            {bench_clause}
        ORDER BY id
    '''
    df = pd.read_sql(query, con=engine, 
                 params={'equipment': equipment, 
                         'excluded_muscles': excluded_muscle_groups})
    
    print(df.head())
    
    # validate names of excluded exercises
    valid_exercises = df['name'].unique().tolist()
    validate_excluded_exercises(excluded_exercises, valid_exercises)

    # filter df by removing excluded exercises
    df = df[~df['name'].isin(excluded_exercises)]
    
	# add all muscle groups that have no eligible exercises to excluded_muscle_groups, e.g. body only, no pull up bar - lats
    eligible_muscle_groups = set(valid_muscle_groups) - set(excluded_muscle_groups)
    for muscle_group in eligible_muscle_groups:
        if len(df[df['primary_muscle'] == muscle_group]) == 0:
            excluded_muscle_groups.append(muscle_group)
    
    if len(set(valid_muscle_groups) - set(excluded_muscle_groups)) < min_num_eligible_muscle_groups[no_of_days]:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Too few eligible exercises to generate programme"})
        }

    if no_of_days == 0:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Number of days is zero"})
        }
    elif no_of_days == 1:
        # FULL BODY x1
        training_split = get_1_day_training_split(excluded_muscle_groups, preferred_muscle_groups, sets_per_muscle)
    elif no_of_days == 2:
        # FULL BODY x2
        training_split = get_2_day_training_split(excluded_muscle_groups, preferred_muscle_groups, time_per_session, sets_per_muscle)
    elif no_of_days == 3:
        # PUSH/PULL/LEGS subject to modification if excluded muscle groups dictate
        training_split = get_3_day_training_split(excluded_muscle_groups, preferred_muscle_groups, sets_per_muscle)
    elif no_of_days == 4:
        # UPPER/LOWER x2 subject to modification if excluded muscle groups dictate
        training_split = get_4_day_training_split(excluded_muscle_groups, preferred_muscle_groups, sets_per_muscle)
    elif no_of_days == 5:
        # PUSH/PULL/LEGS/UPPER/LOWER subject to modification if excluded muscle groups dictate
        training_split = get_5_day_training_split(excluded_muscle_groups, preferred_muscle_groups, sets_per_muscle)
    elif no_of_days == 6:
        # PUSH/PULL/LEGS x ARNOLD subject to modification if excluded muscle groups dictate
        training_split = get_6_day_training_split(excluded_muscle_groups, preferred_muscle_groups, sets_per_muscle)
    elif no_of_days == 7:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Number of days is seven. At least one rest day required."})
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
                ]

                # If no eligible exercises or the maximum number of sets for the muscle_group has been reached,
                # then remove tuple from day muscle groups and go to next tuple
                if (len(possible_exercises_df) == 0 or 
                    sets_per_muscle_per_day[muscle_group] + no_of_sets > max_sets_per_muscle_per_day[muscle_group]):
                    day_muscle_groups.remove(muscle_group, no_of_sets)
                    continue
                    
                # Override no. of sets to 2 if time per session is <= 25 mins
                if time_per_session <= 25:
                    no_of_sets = 2

                time += time_per_set(muscle_group) * no_of_sets

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

                # Add sets
                sets_per_muscle_per_day[muscle_group] += no_of_sets

                # Append exercise to daily workout
                day_workout_exercises.append(selected_exercise, no_of_sets)

            # If not finished 
            if not finished_daily_workout:
                # If day split is unmodfified and close enough to required time, stop.
                # If muscle groups array has ran out, stop.
                if not is_modified and time > 0.75 * time_per_session or len(day_muscle_groups) == 0:
                    finished_daily_workout = True 
                # Otherwise reorder day muscle groups and continue adding exercises
                else:
                    day_muscle_groups = reOrderMuscleGroups(day_muscle_groups)
        
        for muscle_group, daily_sets in sets_per_muscle_per_day:
            sets_per_muscle_per_week[muscle_group] += daily_sets
        
        if time < 0.6 * time_per_session:
            error_encountered = True
        
        workout_programme.append(day_workout_exercises)
    
    for muscle_group, weekly_sets in sets_per_muscle_per_day:
        if weekly_sets > max_sets_per_muscle_per_week[muscle_group]:
            error_encountered = True 
    
    if error_encountered:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Error when generating the programme"})
        }
    
    # No errors encountered, generate data structure to return



        

    # then iterate through each list in training_split and add most optimal exercise for each muscle group 
    # until totalTime exceeds timePerSession, and, loop back round if timePerSession not close to being exceeded (i.e. is totalTime > 0.75 * timePerSession)
    # possibly need to have a flag to indicate whether we loop back round or not, and when looping back round, re-order muscle groups fom largest/most important to least
    # using reOrderMuscleGroups 

    # also need to ensure preferred_muscle_groups is ordered according to a template, so most important muscle groups of the ones preferred 
    # are at the end of the list so they get prioritised, and will prob want to reverse this list for the modifications required
    # branch, as the muscles at start of list currently get prioritised

    # if timePerSession is below a certain value, maybe 25 mins, overwrite all sets to be 2


    # maybe define a map for the minimum number of eligible exercises depending on the number of days/time that will be used to train

    def reOrderMuscleGroups(ordered_muscle_groups, template_order = 
        ["chest", "middle back", "front delt", "quadriceps", "lats", "biceps", "triceps", "hamstrings", "lateral delt", 
        "abdominals", "rear delt", "calves", "forearms", "traps", "adductors", "lower back", "abductors", "glutes"]):
        new_ordered_muscle_groups = []
        for muscle_group in template_order:
            if muscle_group in ordered_muscle_groups:
                new_ordered_muscle_groups.append(muscle_group)
        return new_ordered_muscle_groups


    return {
        "statusCode": 200,
        "body": json.dumps(training_split)
    }
        

    def orderMuscleGroups(possible_muscle_groups, excluded_muscle_groups, preffered_muscle_groups):
        ordered_muscle_groups = preferred_muscle_groups
        for muscle_group in possible_muscle_groups:
            if muscle_group not in ordered_muscle_groups and muscle_group not in excluded_muscle_groups:
                ordered_muscle_groups.append(muscle_group)
        return ordered_muscle_groups
    
        

        

    