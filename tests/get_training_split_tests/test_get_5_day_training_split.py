import pytest
import json
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.buildProgramme.get_training_split.get_5_day_training_split import get_5_day_training_split

class TestGet5DayTrainingSplit:
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

    def test_no_preferred_or_excluded(self):
        result = get_5_day_training_split([], [], self.sets_per_muscle)
        print(f"5-day split: {result}")
        expected = [
            ([
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('traps', 2)
            ], False), 
            ([
                ('middle back', 3),
                ('biceps', 3),
                ('lats', 3),
                ('rear delt', 2),
                ('biceps', 3),
                ('forearms', 3),
                ('middle back', 3),
                ('traps', 2),
                ('biceps', 3),
                ('lats', 3)
            ], False),
            ([
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('abdominals', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('adductors', 2),
                ('abductors', 2),
                ('abdominals', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('abdominals', 3),
                ('glutes', 3)
            ], False),
            ([
                ('chest', 3),
                ('middle back', 3),
                ('triceps', 3),
                ('biceps', 3),
                ('chest', 3),
                ('lats', 3),
                ('triceps', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('chest', 3),
                ('middle back', 3),
                ('triceps', 3),
                ('biceps', 3)
            ], False), 
            ([
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('abdominals', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('abdominals', 3),
                ('adductors', 2),
                ('abductors', 2),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected
    
    def test_exclude_minor_muscles(self):
        excluded = ["traps", "forearms", "abdominals", "calves"]
        result = get_5_day_training_split(excluded, [], self.sets_per_muscle)
        expected = [
            ([
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3)
            ], False),
            ([
                ('middle back', 3),
                ('biceps', 3),
                ('lats', 3),
                ('rear delt', 2),
                ('biceps', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('lats', 3)
            ], False),
            ([
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('adductors', 2),
                ('abductors', 2),
                ('quadriceps', 3),
                ('glutes', 3)
            ], False), 
            ([
                ('chest', 3),
                ('middle back', 3),
                ('triceps', 3),
                ('biceps', 3),
                ('chest', 3),
                ('lats', 3),
                ('triceps', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('chest', 3),
                ('middle back', 3),
                ('triceps', 3),
                ('biceps', 3)
            ], False), 
            ([
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('adductors', 2),
                ('abductors', 2),
                ('glutes', 3)
            ], False)
        ]
        print(f"5-day split: {result}")
        assert result == expected

    def test_exclude_chest_and_hams(self):
        excluded = ["chest", "hamstrings"]
        result = get_5_day_training_split(excluded, [], self.sets_per_muscle)
        expected = [
            ([
                ('front delt', 3),
                ('quadriceps', 3),
                ('triceps', 3),
                ('lateral delt', 3),
                ('abdominals', 3)
            ], True), 
            ([
                ('middle back', 3),
                ('biceps', 3),
                ('lats', 3),
                ('rear delt', 2),
                ('biceps', 3),
                ('forearms', 3),
                ('middle back', 3),
                ('traps', 2),
                ('biceps', 3),
                ('lats', 3)
            ], False),
            ([
                ('calves', 3),
                ('front delt', 3),
                ('quadriceps', 3),
                ('triceps', 3),
                ('lateral delt', 3)
            ], True),
            ([
                ('abdominals', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('lats', 3)
            ], True), 
            ([
                ('forearms', 3),
                ('calves', 3),
                ('front delt', 3),
                ('quadriceps', 3),
                ('triceps', 3)
            ], True)
        ]
        print(f"5-day split: {result}")
        assert result == expected

    def test_exclude_back_abs_adductors(self):
        excluded = ["middle back", "lats", "abdominals", "adductors"]
        result = get_5_day_training_split(excluded, [], self.sets_per_muscle)
        print(f"5-day split: {result}")
        expected = [
            ([
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('traps', 2)
            ], False), 
            ([
                ('biceps', 3),
                ('rear delt', 2),
                ('forearms', 3),
                ('chest', 3),
                ('triceps', 3)
            ], True), 
            ([
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('abductors', 2),
                ('quadriceps', 3),
                ('calves', 3),
                ('glutes', 3)
            ], False), 
            ([
                ('biceps', 3),
                ('rear delt', 2),
                ('forearms', 3),
                ('chest', 3),
                ('triceps', 3)
            ], True), 
            ([
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('abductors', 2),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected
    
    def test_exclude_back_abs_adds_prefer_lower_back_and_bis(self):
        excluded = ["middle back", "lats", "abdominals", "adductors"]
        preferred = ["lower back", "biceps"]
        result = get_5_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"5-day split: {result}")
        expected = [
            ([
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('traps', 2)
            ], False),
            ([
                ('lower back', 2),
                ('biceps', 3),
                ('rear delt', 2),
                ('forearms', 3),
                ('chest', 3)
            ], True), 
            ([
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('abductors', 2),
                ('quadriceps', 3),
                ('calves', 3),
                ('glutes', 3)
            ], False), 
            ([
                ('triceps', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('forearms', 3),
                ('chest', 3)
            ], True), 
            ([
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('abductors', 2),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected
    
    def test_exclude_triceps_prefer_back(self):
        excluded = ["triceps"]
        preferred= ["lats", "middle back"]
        result = get_5_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"5-day split: {result}")
        expected = [
            ([
                ('lats', 3),
                ('middle back', 3),
                ('chest', 3),
                ('biceps', 3),
                ('rear delt', 2)
            ], True), 
            ([
                ('middle back', 3),
                ('biceps', 3),
                ('lats', 3),
                ('rear delt', 2),
                ('biceps', 3),
                ('forearms', 3),
                ('middle back', 3),
                ('traps', 2),
                ('biceps', 3),
                ('lats', 3)
            ], False), 
            ([
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('abdominals', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('adductors', 2),
                ('abductors', 2),
                ('abdominals', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('abdominals', 3),
                ('glutes', 3)
            ], False),
            ([
                ('chest', 3),
                ('forearms', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('rear delt', 2)
            ], True), 
            ([ 
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('abdominals', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('abdominals', 3),
                ('adductors', 2),
                ('abductors', 2),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected

    def test_exclude_chest_quads_hams_forearms(self):
        excluded = ["chest", "quadriceps", "hamstrings", "forearms"]
        preferred= []
        result = get_5_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"5-day split: {result}")
        expected = [
            ([
                ('front delt', 3),
                ('triceps', 3),
                ('lateral delt', 3),
                ('abdominals', 3),
                ('calves', 3)
            ], True),
            ([
                ('middle back', 3),
                ('biceps', 3),
                ('lats', 3),
                ('rear delt', 2),
                ('biceps', 3),
                ('middle back', 3),
                ('traps', 2),
                ('biceps', 3),
                ('lats', 3)
            ],  False), 
            ([
                ('front delt', 3),
                ('triceps', 3),
                ('lateral delt', 3),
                ('abdominals', 3),
                ('calves', 3)
            ], True),
            ([
                ('middle back', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('lats', 3),
                ('front delt', 3)
            ], True),
            ([
                ('triceps', 3),
                ('lateral delt', 3),
                ('abdominals', 3),
                ('calves', 3),
                ('middle back', 3)
            ], True)
        ]
        assert result == expected
        
    def test_exclude_nothing_prefer_glutes_traps_back(self):
        excluded = []
        preferred= ["glutes", "traps", "middle back", "lats"]
        result = get_5_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"5-day split: {result}")
        expected = [
            ([
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('traps', 2)
            ], False), 
            ([
                ('traps', 2),
                ('middle back', 3),
                ('lats', 3),
                ('biceps', 3),
                ('lats', 3),
                ('rear delt', 2),
                ('biceps', 3),
                ('forearms', 3),
                ('middle back', 3),
                ('traps', 2),
                ('biceps', 3)
            ], False),
            ([
                ('glutes', 3),
                ('glutes', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('abdominals', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('adductors', 2),
                ('abductors', 2),
                ('abdominals', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('abdominals', 3),
                ('glutes', 3)
            ], False),
            ([
                ('traps', 2),
                ('middle back', 3),
                ('lats', 3),
                ('chest', 3),
                ('middle back', 3),
                ('triceps', 3),
                ('biceps', 3),
                ('chest', 3),
                ('lats', 3),
                ('triceps', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('chest', 3),
                ('triceps', 3),
                ('biceps', 3)
            ], False),
            ([
                ('glutes', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('abdominals', 3),
                ('quadriceps', 3),
                ('hamstrings', 3),
                ('calves', 3),
                ('abdominals', 3),
                ('adductors', 2),
                ('abductors', 2),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected