import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

def re_order_muscle_groups(ordered_muscle_groups, template_order = 
    ["chest", "middle back", "front delt", "quadriceps", "lats", "biceps", "triceps", "hamstrings", "lateral delt", 
    "abdominals", "rear delt", "calves", "forearms", "traps", "adductors", "lower back", "abductors", "glutes"]):
    new_ordered_muscle_groups = []
    for muscle_group in template_order:
        if muscle_group in ordered_muscle_groups:
            new_ordered_muscle_groups.append(muscle_group)
    return new_ordered_muscle_groups

def connect_to_database():
     # Load environment variables from the .env file
    load_dotenv()

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    engine = create_engine(DATABASE_URL)

    return engine

def get_ordered_programme(workout_programme, days, df, muscle_group_ordering):
    df['order_score'] = (df['primary_muscle'].map(muscle_group_ordering) + 
        df['mechanic'].apply(lambda x: 0.5 if x == "isolation" else 0))

    final_programme = {
        "monday": "rest",
        "tuesday": "rest",
        "wednesday": "rest",
        "thursday": "rest",
        "friday": "rest",
        "saturday": "rest",
        "sunday": "rest"
    }

    for day_programme, day in zip(workout_programme, days):
        day_muscle_groups = []
        for muscle_group, _ in day_programme:
            day_muscle_groups.append(muscle_group)
        day_df = df[df['name'].isin(day_muscle_groups)].copy()
        day_df['no_of_sets'] = day_df['name'].map(dict(day_programme))
        day_df = day_df.sort_values(
            ['order_score', 'name'], 
            ascending=[True, True]
        )
        # Can filter out any non-needed columns here
        final_programme[day] = day_df.to_dict('records')
      
    return final_programme
