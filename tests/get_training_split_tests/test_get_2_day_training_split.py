import pytest
import json
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.buildProgramme.get_training_split.get_2_day_training_split import get_2_day_training_split

class TestGet2DayTrainingSplit:
    time_per_set =  {
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

    def test_no_preferred_or_excluded_1(self):
        result = get_2_day_training_split([],[], 30, self.time_per_set)
        print(f"30-min 2-day split: {result}")
        expected = [
            ([
                ('chest', 2),
                ('middle back', 2),
                ('front delt', 2),
                ('quadriceps', 2)
            ], True),
            ([
                ('biceps', 2),
                ('triceps', 2),
                ('hamstrings', 2),
                ('lateral delt', 2),
                ('abdominals', 2),
                ('rear delt', 2),
                ('lats', 2),
                ('calves', 2),
                ('forearms', 2),
                ('chest', 2),
                ('middle back', 2),
                ('front delt', 2),
                ('quadriceps', 2)
            ], True)
        ]
        assert result == expected

    def test_no_preferred_or_excluded_2(self):
        result = get_2_day_training_split([],[], 60, self.time_per_set)
        print(f"60-min 2-day split: {result}")
        expected = [
            ([
                ('chest', 2),
                ('middle back', 2),
                ('front delt', 2),
                ('quadriceps', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('hamstrings', 2),
                ('lateral delt', 2),
                ('abdominals', 2),
                ('rear delt', 2)
            ], True),
            ([
                ('lats', 2),
                ('calves', 2),
                ('forearms', 2),
                ('chest', 2),
                ('middle back', 2),
                ('front delt', 2),
                ('quadriceps', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('hamstrings', 2),
                ('lateral delt', 2),
                ('abdominals', 2),
                ('rear delt', 2)
            ], True)
        ]
        assert result == expected
    

    def test_no_preferred_or_excluded_3(self):
        result = get_2_day_training_split([],[], 90, self.time_per_set)
        print(f"90-min 2-day split: {result}")
        expected = [
            ([
                ('chest', 2),
                ('middle back', 2),
                ('front delt', 2),
                ('quadriceps', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('hamstrings', 2),
                ('lateral delt', 2),
                ('abdominals', 2),
                ('rear delt', 2),
                ('lats', 2),
                ('calves', 2),
                ('forearms', 2)
            ], True),
            ([
                ('chest', 2),
                ('middle back', 2),
                ('front delt', 2),
                ('quadriceps', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('hamstrings', 2),
                ('lateral delt', 2),
                ('abdominals', 2),
                ('rear delt', 2),
                ('lats', 2),
                ('calves', 2),
                ('forearms', 2)
            ], True)
        ]
        assert result == expected
    
    def test_excluded_no_preferred(self):
        excluded = ["chest", "abdominals"]
        result = get_2_day_training_split(excluded, [], 60, self.time_per_set)
        print(f"60-min 2-day split: {result}")
        expected = [
            ([
                ('middle back', 2),
                ('front delt', 2),
                ('quadriceps', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('hamstrings', 2),
                ('lateral delt', 2),
                ('rear delt', 2),
                ('lats', 2),
                ('calves', 2),
            ], True),
            ([
                ('forearms', 2),
                ('middle back', 2),
                ('front delt', 2),
                ('quadriceps', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('hamstrings', 2),
                ('lateral delt', 2),
                ('rear delt', 2),
                ('lats', 2),
                ('calves', 2),
            ], True)
        ]
        assert result == expected

    def test_preferred_no_excluded(self):
        preferred = ["front delt", "lateral delt", "rear delt", "forearms"]
        result = get_2_day_training_split([], preferred, 60, self.time_per_set)
        print(f"60-min 2-day split: {result}")
        expected = [
            ([
                ('front delt', 2),
                ('lateral delt', 2),
                ('rear delt', 2),
                ('forearms', 2),
                ('chest', 2),
                ('middle back', 2),
                ('quadriceps', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('hamstrings', 2)
            ], True),
            ([
                ('abdominals', 2),
                ('lats', 2),
                ('calves', 2),
                ('front delt', 2),
                ('lateral delt', 2),
                ('rear delt', 2),
                ('forearms', 2),
                ('chest', 2),
                ('middle back', 2),
                ('quadriceps', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('hamstrings', 2)
            ], True)
        ]
        assert result == expected
    
    def test_preferred_and_excluded(self):
        preferred = ["front delt", "lateral delt", "rear delt", "forearms"]
        excluded = ["quadriceps", "hamstrings", "traps"]
        result = get_2_day_training_split(excluded, preferred, 60, self.time_per_set)
        print(f"60-min 2-day split: {result}")
        expected = [
            ([
                ('front delt', 2),
                ('lateral delt', 2),
                ('rear delt', 2),
                ('forearms', 2),
                ('chest', 2),
                ('middle back', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('abdominals', 2),
                ('lats', 2),
            ], True), 
            ([
                ('calves', 2),
                ('front delt', 2),
                ('lateral delt', 2),
                ('rear delt', 2),
                ('forearms', 2),
                ('chest', 2),
                ('middle back', 2),
                ('biceps', 2),
                ('triceps', 2),
                ('abdominals', 2),
                ('lats', 2),
            ], True)
        ]
        assert result == expected