import pytest
import json
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.buildProgramme.lambda_function import lambda_handler

DUMP_DIR = os.path.join(os.path.dirname(__file__), "build_programme_lambda_outputs")

class TestBuildProgrammeLambdaFunction:
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

    def get_time_per_set(self, muscle, body_only):
        return self.time_per_set[muscle] - (1 if body_only else 0)

    def test_1_day_beginner_45_mins_no_equipment(self):
        test_name = "1_day_beginner_45_mins_no_equipment"

        days = ["monday"]
        time = 45
        equipment = []
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    def test_1_day_beginner_90_mins_no_equipment(self):
        test_name = "1_day_beginner_90_mins_no_equipment"

        days = ["tuesday"]
        time = 90
        equipment = []
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    def test_1_day_beginner_90_mins_bench_pullupbar_dumbbell(self):
        test_name = "1_day_beginner_90_mins_bench_pullupbar_dumbbell"

        days = ["tuesday"]
        time = 90
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    def test_1_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders(self):
        test_name = "1_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders"

        days = ["tuesday"]
        time = 45
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["quadriceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_2_day_beginner_45_mins_no_equipment(self):
        test_name = "2_day_beginner_45_mins_no_equipment"

        days = ["monday", "sunday"]
        time = 45
        equipment = []
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    def test_2_day_beginner_45_mins_no_equipment_high_variation(self):
        test_name = "2_day_beginner_45_mins_no_equipment_high_variation"

        days = ["monday", "sunday"]
        time = 45
        equipment = []
        is_beginner = True
        exercise_variation = 1.1 # > 1.0 means guaranteed to select the one used less if only difference of 1 in hypertrophy score
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_2_day_beginner_90_mins_all_equipment(self):
        test_name = "2_day_beginner_90_mins_all_equipment"

        days = ["tuesday", "thursday"]
        time = 90
        equipment = ["bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "medicine ball", "dip bar", "dumbbell", "bench", "pull up bar"]
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_2_day_90_mins_bench_pullupbar_dumbbell(self):
        test_name = "2_day_90_mins_bench_pullupbar_dumbbell"

        days = ["tuesday", "friday"]
        time = 90
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    def test_2_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders(self):
        test_name = "2_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders"

        days = ["tuesday", "wednesday"]
        time = 45
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["quadriceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")
    
    
    def test_3_day_beginner_20_mins_no_equipment(self):
        test_name = "3_day_beginner_20_mins_no_equipment"

        days = ["monday", "tuesday", "sunday"]
        time = 20
        equipment = []
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_3_day_beginner_45_mins_no_equipment_high_variation(self):
        test_name = "3_day_beginner_45_mins_no_equipment_high_variation"

        days = ["monday", "tuesday", "friday"]
        time = 45
        equipment = []
        is_beginner = True
        exercise_variation = 1.1 # > 1.0 means guaranteed to select the one used less if only difference of 1 in hypertrophy score
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    def test_3_day_beginner_90_mins_all_equipment(self):
        test_name = "3_day_beginner_90_mins_all_equipment"

        days = ["tuesday", "wednesday", "thursday"]
        time = 90
        equipment = ["bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "medicine ball", "dip bar", "dumbbell", "bench", "pull up bar"]
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_3_day_90_mins_bench_pullupbar_dumbbell(self):
        test_name = "3_day_90_mins_bench_pullupbar_dumbbell"

        days = ["tuesday", "friday", "saturday"]
        time = 90
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_3_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders(self):
        test_name = "3_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders"

        days = ["tuesday", "wednesday", "thursday"]
        time = 45
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["quadriceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")


    def test_4_day_beginner_20_mins_no_equipment(self):
        test_name = "4_day_beginner_20_mins_no_equipment"

        days = ["monday", "tuesday", "wednesday", "sunday"]
        time = 20
        equipment = []
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_4_day_beginner_45_mins_no_equipment_high_variation(self):
        test_name = "4_day_beginner_45_mins_no_equipment_high_variation"

        days = ["monday", "tuesday", "friday", "saturday"]
        time = 45
        equipment = []
        is_beginner = True
        exercise_variation = 1.1 # > 1.0 means guaranteed to select the one used less if only difference of 1 in hypertrophy score
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    def test_4_day_beginner_90_mins_all_equipment(self):
        test_name = "4_day_beginner_90_mins_all_equipment"

        days = ["tuesday", "wednesday", "thursday", "friday"]
        time = 90
        equipment = ["bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "medicine ball", "dip bar", "dumbbell", "bench", "pull up bar"]
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_4_day_90_mins_bench_pullupbar_dumbbell(self):
        test_name = "4_day_90_mins_bench_pullupbar_dumbbell"

        days = ["tuesday", "friday", "saturday", "sunday"]
        time = 90
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_4_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders(self):
        test_name = "4_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders"

        days = ["tuesday", "wednesday", "thursday", "friday"]
        time = 45
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["quadriceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    def test_5_day_beginner_20_mins_no_equipment(self):
        test_name = "5_day_beginner_20_mins_no_equipment"

        days = ["monday", "tuesday", "wednesday", "saturday", "sunday"]
        time = 20
        equipment = []
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_5_day_beginner_45_mins_no_equipment_high_variation(self):
        test_name = "5_day_beginner_45_mins_no_equipment_high_variation"

        days = ["monday", "tuesday", "friday", "saturday", "sunday"]
        time = 45
        equipment = []
        is_beginner = True
        exercise_variation = 1.1 # > 1.0 means guaranteed to select the one used less if only difference of 1 in hypertrophy score
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        assert response["statusCode"] == 400
        assert response_body["error"] == "Error when generating the programme - programme deemed imbalanced/unsafe"

    def test_5_day_beginner_90_mins_all_equipment(self):
        test_name = "5_day_beginner_90_mins_all_equipment"

        days = ["tuesday", "wednesday", "thursday", "friday", "sunday"]
        time = 90
        equipment = ["bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "medicine ball", "dip bar", "dumbbell", "bench", "pull up bar"]
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_5_day_90_mins_bench_pullupbar_dumbbell(self):
        test_name = "5_day_90_mins_bench_pullupbar_dumbbell"

        days = ["monday", "tuesday", "friday", "saturday", "sunday"]
        time = 90
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_5_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders(self):
        test_name = "5_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders"

        days = ["tuesday", "wednesday", "thursday", "friday", "saturday"]
        time = 45
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["quadriceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    def test_6_day_beginner_20_mins_no_equipment(self):
        test_name = "6_day_beginner_20_mins_no_equipment"

        days = ["monday", "tuesday", "wednesday", "friday", "saturday", "sunday"]
        time = 20
        equipment = []
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_6_day_beginner_45_mins_no_equipment_high_variation(self):
        test_name = "6_day_beginner_45_mins_no_equipment_high_variation"

        days = ["monday", "tuesday", "wednesday", "friday", "saturday", "sunday"]
        time = 45
        equipment = []
        is_beginner = True
        exercise_variation = 1.1 # > 1.0 means guaranteed to select the one used less if only difference of 1 in hypertrophy score
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        assert response["statusCode"] == 400
        assert response_body["error"] == "Error when generating the programme - programme deemed imbalanced/unsafe"

    def test_6_day_beginner_90_mins_all_equipment(self):
        test_name = "6_day_beginner_90_mins_all_equipment"

        days = ["tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        time = 90
        equipment = ["bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "medicine ball", "dip bar", "dumbbell", "bench", "pull up bar"]
        is_beginner = True
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_6_day_90_mins_bench_pullupbar_dumbbell(self):
        test_name = "6_day_90_mins_bench_pullupbar_dumbbell"

        days = ["monday", "tuesday", "wednesday", "friday", "saturday", "sunday"]
        time = 90
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = []
        preferred_muscles = []

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")

    
    def test_6_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders(self):
        test_name = "6_day_45_mins_bench_pullupbar_dumbbell_exclude_quads_prefer_shoulders"

        days = ["tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        time = 45
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["quadriceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        has_bench = "bench" in equipment
        has_pull_up_bar = "pull up bar" in equipment

        assert response["statusCode"] == 200
        exercises = {}
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            # Check days
            if day in days:
                exercises[day] = []

                day_programme = response_body[day]

                t = 0
                prev_order_score = 0
                for exercise in day_programme:
                    t += exercise["no_of_sets"] * self.get_time_per_set(exercise["primary_muscle"], exercise["equipment"] == "body only")
                    # Check equipment
                    assert exercise["equipment"] in (equipment + ["body only"])
                    if not has_bench:
                        assert not exercise["bench_required"]
                    if not has_pull_up_bar:
                        assert not exercise["pull_up_bar_required"]
                    # Check excluded muscle groups
                    assert exercise["primary_muscle"] not in excluded_muscles
                    # Check beginner friendly
                    if is_beginner:
                        assert exercise["beginner_friendly"]
                    # Check ordering
                    assert exercise["order_score"] >= prev_order_score
                    prev_order_score = exercise["order_score"]
                    
                    exercises[day].append(exercise['name'])
                # Check time
                assert t < time + 12 and t >= 0.6 * time
            else:
                assert response_body[day] == "rest"

        print(exercises)

        # Debug dump logic
        os.makedirs(DUMP_DIR, exist_ok=True)
        dump_path = os.path.join(DUMP_DIR, f"{test_name}.json")

        if not os.path.exists(dump_path):
            with open(dump_path, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Debug dump saved at {dump_path}")


    def test_7_days(self):
        test_name = "test_7_days"

        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        time = 45
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["quadriceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])


        assert response["statusCode"] == 400
        print(test_name, "message:", response_body["error"])
    
    def test_0_days(self):
        test_name = "test_0_days"

        days = []
        time = 45
        equipment = ["bench", "pull up bar", "dumbbell"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["quadriceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        assert response["statusCode"] == 400
        print(test_name, "message:", response_body["error"])
    
    def test_3_days_exclude_chest_tris_qauds_no_equipment(self):
        test_name = "test_3_days_exclude_chest_tris_qauds_no_equipment"

        days = ["monday", "tuesday", "wednesday"]
        time = 45
        equipment = []
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["chest", "triceps", "quadriceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        assert response["statusCode"] == 400
        print(test_name, "message:", response_body["error"])

    def test_most_excluded_and_all_equipment(self):
        test_name = "test_most_excluded_and_all_equipment"

        days = ["monday", "tuesday", "wednesday"]
        time = 45
        equipment = ["bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "medicine ball", "dip bar", "dumbbell", "bench", "pull up bar"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["abdominals", "abductors", "adductors", "biceps", "front delt", "lateral delt", "rear delt",
                   "calves", "chest", "forearms", "glutes", "hamstrings", "quadriceps", "lower back",
                   "middle back", "lats"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        assert response["statusCode"] == 400
        print(test_name, "message:", response_body["error"])

    def test_chest_traps_forearms_only_and_all_equipment(self):
        test_name = "test_chest_traps_forearms_only_and_all_equipment"

        days = ["monday", "tuesday", "wednesday"]
        time = 60
        equipment = ["bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "medicine ball", "dip bar", "dumbbell", "bench", "pull up bar"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["abdominals", "abductors", "adductors", "biceps", "front delt", "lateral delt", "rear delt",
                   "calves", "glutes", "hamstrings", "quadriceps", "lower back",
                   "middle back", "lats", "triceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        assert response["statusCode"] == 400
        print(test_name, "message:", response_body["error"])

    def test_1_day_forearms_only_and_all_equipment(self):
        test_name = "test_chest_only_and_all_equipment"

        days = ["monday"]
        time = 60
        equipment = ["bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
              "e-z curl bar", "medicine ball", "dip bar", "dumbbell", "bench", "pull up bar"]
        is_beginner = False
        exercise_variation = 0.5
        excluded_muscles = ["abdominals", "abductors", "adductors", "biceps", "front delt", "lateral delt", "rear delt",
                   "calves", "chest", "forearms", "glutes", "hamstrings", "quadriceps", "lower back",
                   "middle back", "lats", "traps", "triceps"]
        preferred_muscles = ["shoulders"]

        test_event = {
            "body": json.dumps({
                "days": days,
                "timePerSession": time,
                "equipment": equipment,
                "beginnerFriendly": is_beginner,
                "exerciseVariation": exercise_variation,
                "excludedMuscleGroups": excluded_muscles,
                "preferredMuscleGroups": preferred_muscles
            })
        }

        context = None
        response = lambda_handler(test_event, context)
        response_body = json.loads(response["body"])

        assert response["statusCode"] == 400
        print(test_name, "message:", response_body["error"])
    




