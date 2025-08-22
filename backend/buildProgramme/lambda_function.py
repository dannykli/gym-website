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
        "rear delt": 2,
        "calves": 3,
        "chest": 3,
        "forearms": 3,
        "glutes": 3,
        "hamstrings": 3,
        "quadriceps": 3,
        "lower back": 2,
        "middle back": 3,
        "lats": 3,
        "traps": 2,
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

    training_split = []

    no_of_days = len(user_preferences["days"])
    time_per_session = user_preferences["timePerSession"]
    equipment = user_preferences["equipment"]
    excluded_muscle_groups = user_preferences["excludedMuscleGroups"]
    excluded_exercises = user_preferences["excludedExercises"]
    preferred_muscle_groups = user_preferences["preferredMuscleGroups"]

	# Validate user preferences
    validate_equipment(equipment, valid_equipment)
    validate_excluded_muscle_groups(excluded_muscle_groups, valid_muscle_groups)
    validate_preferred_muscle_groups(preferred_muscle_groups, excluded_muscle_groups, valid_muscle_groups)

	# TODO: Need to add bench required, pull up bar required, beginner friendly restrictions to query
    query = '''
        SELECT name, mechanic, equipment, primary_muscle, secondary_muscles, beginner_friendly, instructions, images, hypertrophy_score, rep_range, bench_required, pull_up_bar_required
        FROM exercises
        WHERE not hidden AND equipment = ANY(:equipment) AND primary_muscle != ALL(:excluded_muscles)
        ORDER BY id
    '''
    df = pd.read_sql(query, con=engine, 
                 params={'equipment': equipment, 
                         'excluded_muscles': excluded_muscle_groups})
    
    valid_exercises = df['name'].unique().tolist()
    validate_excluded_exercises(excluded_exercises, valid_exercises)

    # filter df by removing excluded exercises
    df = df[~df['name'].isin(excluded_exercises)]
    
	# add all muscle groups that have no eligible exercises to excluded_muscle_groups, e.g. body only, no pull up bar - lats
    eligible_muscle_groups = set(valid_muscle_groups) - set(excluded_muscle_groups)
    for muscle_group in eligible_muscle_groups:
        if len(df[df['primary_muscle'] == muscle_group]) == 0:
            excluded_muscle_groups.append(muscle_group)

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

	# Retrieve exercises for the training split
    workout_programme = []
    for day_muscle_groups in training_split:
        day_workout_exercises = []
        

    # then iterate through each list in training_split and add most optimal exercise for each muscle group 
    # until totalTime exceeds timePerSession, and, loop back round if timePerSession not close to being exceeded (i.e. is totalTime > 0.75 * timePerSession)
    # possibly need to have a flag to indicate whether we loop back round or not, and when looping back round, re-order muscle groups fom largest/most important to least
    # using reOrderMuscleGroups 

    # also need to ensure preferred_muscle_groups is ordered according to a template, so most important muscle groups of the ones preferred 
    # are at the end of the list so they get prioritised, and will prob want to reverse this list for the modifications required
    # branch, as the muscles at start of list currently get prioritised

    # if timePerSession is below a certain value, maybe 25 mins, overwrite all sets to be 2

    # define a map that defines the max. no of exercises for one muscle group on a single day

    # add all muscle groups that have no elgible exercises to excluded_muscle_groups, e.g. body only, no pull up bar - lats

    # check if preferred muscle groups contains any excluded muscle groups, in which case remove them

    # maybe define a map for the minimum number of eligible exercises depending on the number of days/time that will be used to train

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
        
    def reOrderMuscleGroups(ordered_muscle_groups, template_order = 
        ["chest", "middle back", "front delt", "quadriceps", "lats", "biceps", "triceps", "hamstrings", "lateral delt", 
        "abdominals", "rear delt", "calves", "forearms", "traps", "adductors", "lower back", "abductors", "glutes"]):
        new_ordered_muscle_groups = []
        for muscle_group in template_order:
            if muscle_group in ordered_muscle_groups:
                new_ordered_muscle_groups.append(muscle_group)
        

        

    