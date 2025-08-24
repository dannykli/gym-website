import pytest
import json
import sys
import os
import pandas as pd
from sqlalchemy import text

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.buildProgramme.lambda_function_utils import re_order_muscle_groups
from backend.buildProgramme.lambda_function_utils import connect_to_database
from backend.buildProgramme.lambda_function_utils import get_ordered_programme

class TestLambdaFunctionUtils:
    def test_re_order_muscle_groups(self):
        muscle_groups = [
            "abdominals", "abductors", "adductors", "biceps", "chest", "forearms"
        ]
        result = re_order_muscle_groups(muscle_groups)
        expected = [
            "chest", "biceps", "abdominals", "forearms", "adductors", "abductors"
        ]
        assert result == expected
    
    def test_validate_preferred_muscle_groups(self):
        engine = connect_to_database()
        query = text(f'''
            SELECT name, mechanic, equipment, primary_muscle, secondary_muscles, 
                beginner_friendly, instructions, images, hypertrophy_score, 
                rep_range, bench_required, pull_up_bar_required
            FROM exercises
            WHERE NOT hidden 
                AND equipment = ANY(:equipment) 
                AND primary_muscle != ALL(:excluded_muscles)
            ORDER BY id
        ''')
        equipment = ["body only"]
        excluded_muscle_groups = []
        days = ["monday"]

        muscle_group_ordering = {
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

        workout_programme = [[('Incline Push-Up', 2), ('Bodyweight Squat', 2), 
            ('Standing Towel Triceps Extension', 2), ('Cocoons', 2), ('Push-Up Wide', 2), 
            ('Bodyweight Walking Lunge', 2), ('Incline Push-Up Close-Grip', 2), 
            ('Reverse Crunch', 2), ('Push-Up', 2), ('Leg Pull-In', 2)]]

        df = pd.read_sql(query, con=engine, 
                    params={'equipment': equipment, 
                            'excluded_muscles': excluded_muscle_groups})
        result = get_ordered_programme(workout_programme, days, df, muscle_group_ordering)
        print(result)
        expected = {'monday': [{'name': 'Bodyweight Squat', 'mechanic': 'compound', 'equipment': 'body only', 'primary_muscle': 'quadriceps', 'secondary_muscles': ['glutes', 'hamstrings'], 'beginner_friendly': True, 'instructions': ['Stand with your feet shoulder width apart. You can place your hands behind your head. This will be your starting position.', 'Begin the movement by flexing your knees and hips, sitting back with your hips.', 'Continue down to full depth if you are able,and quickly reverse the motion until you return to the starting position. As you squat, keep your head and chest up and push your knees out.'], 'images': ['Bodyweight_Squat/0.jpg', 'Bodyweight_Squat/1.jpg'], 'hypertrophy_score': 1, 'rep_range': '12-20', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 1.0, 'no_of_sets': 2}, {'name': 'Bodyweight Walking Lunge', 'mechanic': 'compound', 'equipment': 'body only', 'primary_muscle': 'quadriceps', 'secondary_muscles': ['calves', 'glutes', 'hamstrings'], 'beginner_friendly': True, 'instructions': ['Begin standing with your feet shoulder width apart and your hands on your hips.', 'Step forward with one leg, flexing the knees to drop your hips. Descend until your rear knee nearly touches the ground. Your posture should remain upright, and your front knee should stay above the front foot.', 'Drive through the heel of your lead foot and extend both knees to raise yourself back up.', 'Step forward with your rear foot, repeating the lunge on the opposite leg.'], 'images': ['Bodyweight_Walking_Lunge/0.jpg', 'Bodyweight_Walking_Lunge/1.jpg'], 'hypertrophy_score': 1, 'rep_range': '12-20', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 1.0, 'no_of_sets': 2}, {'name': 'Incline Push-Up', 'mechanic': 'compound', 'equipment': 'body only', 'primary_muscle': 'chest', 'secondary_muscles': ['shoulders', 'triceps'], 'beginner_friendly': True, 'instructions': ['Stand facing bench or sturdy elevated platform. Place hands on edge of bench or platform, slightly wider than shoulder width.', 'Position forefoot back from bench or platform with arms and body straight. Arms should be perpendicular to body. Keeping body straight, lower chest to edge of box or platform by bending arms.', 'Push body up until arms are extended. Repeat.'], 'images': ['Incline_Push-Up/0.jpg', 'Incline_Push-Up/1.jpg'], 'hypertrophy_score': 2, 'rep_range': '10-15', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 4.0, 'no_of_sets': 2}, {'name': 'Push-Up', 'mechanic': 'compound', 'equipment': 'body only', 'primary_muscle': 'chest', 'secondary_muscles': ['shoulders', 'triceps'], 'beginner_friendly': True, 'instructions': ['Lie on the floor face down and place your hands about 36 inches apart while holding your torso up at arms length.', 'Next, lower yourself downward until your chest almost touches the floor as you inhale.', 'Now breathe out and press your upper body back up to the starting position while squeezing your chest.', 'After a brief pause at the top contracted position, you can begin to lower yourself downward again for as many repetitions as needed.'], 'images': ['Pushups/0.jpg', 'Pushups/1.jpg'], 'hypertrophy_score': 2, 'rep_range': '10-15', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 4.0, 'no_of_sets': 2}, {'name': 'Push-Up Wide', 'mechanic': 'compound', 'equipment': 'body only', 'primary_muscle': 'chest', 'secondary_muscles': ['abdominals', 'shoulders', 'triceps'], 'beginner_friendly': True, 'instructions': ['With your hands wide apart, support your body on your toes and hands in a plank position. Your elbows should be extended and your body straight. Do not allow your hips to sag. This will be your starting position.', 'To begin, allow the elbows to flex, lowering your chest to the floor as you inhale.', 'Using your pectoral muscles, press your upper body back up to the starting position by extending the elbows. Exhale as you perform this step.', 'After pausing at the contracted position, repeat the movement for the prescribed amount of repetitions.'], 'images': ['Push-Up_Wide/0.jpg', 'Push-Up_Wide/1.jpg'], 'hypertrophy_score': 2, 'rep_range': '10-15', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 4.0, 'no_of_sets': 2}, {'name': 'Incline Push-Up Close-Grip', 'mechanic': 'compound', 'equipment': 'body only', 'primary_muscle': 'triceps', 'secondary_muscles': ['chest', 'shoulders'], 'beginner_friendly': True, 'instructions': ['Stand facing a Smith machine bar or sturdy elevated platform at an appropriate height.', 'Place your hands next to one another on the bar.', 'Position your feet back from the bar with arms and body straight. This will be your starting position.', 'Keeping your body straight, lower your chest to the bar by bending the arms.', 'Return to the starting position by extending the elbows, pressing yourself back up.'], 'images': ['Incline_Push-Up_Close-Grip/0.jpg', 'Incline_Push-Up_Close-Grip/1.jpg'], 'hypertrophy_score': 1, 'rep_range': '8-12', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 9.0, 'no_of_sets': 2}, {'name': 'Standing Towel Triceps Extension', 'mechanic': 'isolation', 'equipment': 'body only', 'primary_muscle': 'triceps', 'secondary_muscles': [], 'beginner_friendly': True, 'instructions': ['To begin, stand up with both arms fully extended above the head holding one end of a towel with both hands. Your elbows should be in and the arms perpendicular to the floor with the palms facing each other while your feet should be shoulder width apart from each other. This is the starting position.', 'Now communicate with your partner so that he/she can grip the other side of the towel to apply resistance. Keeping your upper arms close to your head (elbows in) and perpendicular to the floor, lower the resistance in a semicircular motion behind your head until your forearms touch your biceps. Tip: The upper arms should remain stationary and only the forearms should move. Breathe in as you perform this step.', 'Go back to the starting position by using the triceps to raise the towel. Breathe out as you perform this step.', 'Repeat for the recommended amount of repetitions.'], 'images': ['Standing_Towel_Triceps_Extension/0.jpg', 'Standing_Towel_Triceps_Extension/1.jpg'], 'hypertrophy_score': 1, 'rep_range': '8-12', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 9.5, 'no_of_sets': 2}, {'name': 'Cocoons', 'mechanic': 'compound', 'equipment': 'body only', 'primary_muscle': 'abdominals', 'secondary_muscles': [], 'beginner_friendly': True, 'instructions': ['Begin by lying on your back on the ground. Your legs should be straight and your arms extended behind your head. This will be your starting position.', 'To perform the movement, tuck the knees toward your chest, rotating your pelvis to lift your glutes from the floor. As you do so, flex the spine, bringing your arms back over your head to perform a simultaneous crunch motion.', 'After a brief pause, return to the starting position.'], 'images': ['Cocoons/0.jpg', 'Cocoons/1.jpg'], 'hypertrophy_score': 2, 'rep_range': '8-12', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 13.0, 'no_of_sets': 2}, {'name': 'Leg Pull-In', 'mechanic': 'compound', 'equipment': 'body only', 'primary_muscle': 'abdominals', 'secondary_muscles': [], 'beginner_friendly': True, 'instructions': ['Lie on an exercise mat with your legs extended and your hands either palms facing down next to you or under your glutes. Tip: My preference is with the hands next to me. This will be your starting position.', 'Bend your knees and pull your upper thighs into your midsection as you breathe out. Continue the motion until your knees are around chest level. Contract your abs as you execute this movement and hold for a second at the top. Tip: As you perform the motion, the lower legs (calves) should always remain parallel to the floor.', 'Return to the starting position as you inhale.', 'Repeat for the recommended amount of repetitions.'], 'images': ['Leg_Pull-In/0.jpg', 'Leg_Pull-In/1.jpg'], 'hypertrophy_score': 2, 'rep_range': '10-15', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 13.0, 'no_of_sets': 2}, {'name': 'Reverse Crunch', 'mechanic': 'isolation', 'equipment': 'body only', 'primary_muscle': 'abdominals', 'secondary_muscles': [], 'beginner_friendly': True, 'instructions': ['Lie down on the floor with your legs fully extended and arms to the side of your torso with the palms on the floor. Your arms should be stationary for the entire exercise.', 'Move your legs up so that your thighs are perpendicular to the floor and feet are together and parallel to the floor. This is the starting position.', 'While inhaling, move your legs towards the torso as you roll your pelvis backwards and you raise your hips off the floor. At the end of this movement your knees will be touching your chest.', 'Hold the contraction for a second and move your legs back to the starting position while exhaling.', 'Repeat for the recommended amount of repetitions.'], 'images': ['Reverse_Crunch/0.jpg', 'Reverse_Crunch/1.jpg'], 'hypertrophy_score': 2, 'rep_range': '10-15', 'bench_required': False, 'pull_up_bar_required': False, 'order_score': 13.5, 'no_of_sets': 2}], 'tuesday': 'rest', 'wednesday': 'rest', 'thursday': 'rest', 'friday': 'rest', 'saturday': 'rest', 'sunday': 'rest'}
        assert expected == result

    