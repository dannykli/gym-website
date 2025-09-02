import json
import pandas as pd
from sqlalchemy import text
import os
import sys

from get_training_split.get_1_day_training_split import get_1_day_training_split
from get_training_split.get_2_day_training_split import get_2_day_training_split
from get_training_split.get_3_day_training_split import get_3_day_training_split
from get_training_split.get_4_day_training_split import get_4_day_training_split
from get_training_split.get_5_day_training_split import get_5_day_training_split
from get_training_split.get_6_day_training_split import get_6_day_training_split

from validate_user_preferences import validate_excluded_muscle_groups
from validate_user_preferences import validate_preferred_muscle_groups
from validate_user_preferences import validate_equipment

from get_exercises import get_exercises

from lambda_function_utils import re_order_muscle_groups
from lambda_function_utils import connect_to_database
from lambda_function_utils import get_ordered_programme

def lambda_handler(event, context):
    try:
        user_preferences = json.loads(event["body"])
        
    except (KeyError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "headers": { 
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Invalid or missing JSON body"})
        }

    valid_muscle_groups = ["abdominals", "abductors", "adductors", "biceps", "front delt", "lateral delt", "rear delt",
                   "calves", "chest", "forearms", "glutes", "hamstrings", "quadriceps", "lower back",
                   "middle back", "lats", "traps", "triceps"]
    
    valid_equipment = ["body only", "bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "dip bar", "dumbbell", "bench", "pull up bar"]
    

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
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 4,
        6: 4,
        7: 0
    }
    
    muscle_group_ordering_for_exercises = {
        "abdominals": 13,
        "abductors": 15,
        "adductors": 16,
        "biceps": 10,
        "front delt": 7,
        "lateral delt": 12,
        "rear delt": 8,
        "calves": 17,
        "chest": 4,
        "forearms": 18,
        "glutes": 2,
        "hamstrings": 3,
        "quadriceps": 1,
        "lower back": 14,
        "middle back": 5,
        "lats": 6,
        "traps": 11,
        "triceps": 9
    }

    # Store user preferences
    days = user_preferences["days"]
    no_of_days = len(days)
    time_per_session = user_preferences["timePerSession"]
    equipment = user_preferences["equipment"]
    beginner_friendly = user_preferences["beginnerFriendly"]
    variability_multiplier = user_preferences["exerciseVariation"]
    excluded_muscle_groups = user_preferences["excludedMuscleGroups"]
    preferred_muscle_groups = user_preferences["preferredMuscleGroups"]

	# Validate user preferences
    equipment = validate_equipment(equipment, valid_equipment)
    excluded_muscle_groups = validate_excluded_muscle_groups(excluded_muscle_groups, valid_muscle_groups)
    preferred_muscle_groups = validate_preferred_muscle_groups(preferred_muscle_groups, excluded_muscle_groups, valid_muscle_groups)

    # Order preferred_muscle_groups to prioritise more important muscles
    preferred_muscle_groups = re_order_muscle_groups(preferred_muscle_groups)
    
    # Connect to database
    engine = connect_to_database()

    # Get exercises from database
    pull_up_bar_clause = "AND NOT pull_up_bar_required" if "pull up bar" not in equipment else ""
    bench_clause = "AND NOT bench_required" if "bench" not in equipment else ""
    beginner_clause = "AND beginner_friendly" if beginner_friendly else ""

    query = text(f'''
        SELECT id, name, mechanic, equipment, primary_muscle, secondary_muscles, 
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
    ''')

    df = pd.read_sql(query, con=engine, 
                 params={'equipment': equipment, 
                         'excluded_muscles': excluded_muscle_groups})
    
	# Add all muscle groups that have no eligible exercises to excluded_muscle_groups, e.g. body only, no pull up bar - lats
    eligible_muscle_groups = set(valid_muscle_groups) - set(excluded_muscle_groups)
    for muscle_group in eligible_muscle_groups:
        if len(df[df['primary_muscle'] == muscle_group]) == 0:
            excluded_muscle_groups.append(muscle_group)
    
    # Check that there are sufficient muscle groups to attempt to generate programme
    if len(set(valid_muscle_groups) - set(excluded_muscle_groups)) < min_num_eligible_muscle_groups[no_of_days]:
        return {
            "statusCode": 400,
            "headers": { 
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Too few eligible exercises to generate programme"})
        }

    # Get the training split
    if no_of_days == 0:
        return {
            "statusCode": 400,
            "headers": { 
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Number of days is zero"})
        }
    elif no_of_days == 1:
        # FULL BODY x1
        training_split = get_1_day_training_split(excluded_muscle_groups, preferred_muscle_groups)
    elif no_of_days == 2:
        # FULL BODY x2
        training_split = get_2_day_training_split(excluded_muscle_groups, preferred_muscle_groups, time_per_session, time_per_set)
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
            "body": json.dumps({"error": "Number of days is seven. At least one rest day required"})
        }
    
    # Get the exercises for the training split
    (_, workout_programme),  (_, error) = list(get_exercises(
        df, training_split, valid_muscle_groups, max_sets_per_muscle_per_day, 
        max_sets_per_muscle_per_week, time_per_set, variability_multiplier, time_per_session
    ).items())

    print(workout_programme)

    # Return if error ocurred during programme generation
    if error is not None:
        return error
    
    # Order the exercises for each day and construct final programme
    programme = get_ordered_programme(workout_programme, days, df, muscle_group_ordering_for_exercises)

    print(programme)

    return {
        "statusCode": 200,
        "headers": { 
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(programme)
    }
    

        

    