import pytest
import json
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.buildProgramme.get_training_split.get_4_day_training_split import get_4_day_training_split

class TestGet4DayTrainingSplit:
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
        result = get_4_day_training_split([], [], self.sets_per_muscle)
        print(f"4-day split: {result}")
        expected = [
            ([
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('traps', 2),
                ('middle back', 3),
                ('biceps', 3),
                ('lats', 3),
                ('triceps', 3)
            ], False), 
            ([
                ('quadriceps', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('adductors', 2),
                ('calves', 3),
                ('quadriceps', 3)
            ], False), 
            ([
                ('lats', 3),
                ('biceps', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('forearms', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('middle back', 3),
                ('biceps', 3)
            ], False), 
            ([
                ('hamstrings', 3),
                ('hamstrings', 3),
                ('abdominals', 3),
                ('lateral delt', 3),
                ('front delt', 3),
                ('abdominals', 3),
                ('abductors', 2),
                ('hamstrings', 3),
                ('calves', 3),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected
    
    def test_exclude_minor_muscles(self):
        excluded = ["traps", "forearms", "abdominals", "calves"]
        result = get_4_day_training_split(excluded, [], self.sets_per_muscle)
        expected = [
            ([
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('lats', 3),
                ('triceps', 3)
            ], False), 
            ([
                ('quadriceps', 3),
                ('quadriceps', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('adductors', 2),
                ('quadriceps', 3)
            ], False), 
            ([
                ('lats', 3),
                ('biceps', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('middle back', 3),
                ('biceps', 3)
            ], False),
            ([
                ('hamstrings', 3),
                ('hamstrings', 3),
                ('lateral delt', 3),
                ('front delt', 3),
                ('abductors', 2),
                ('hamstrings', 3),
                ('glutes', 3)
            ], False)
        ]
        print(f"4-day split: {result}")
        assert result == expected

    def test_exclude_chest_and_hams(self):
        excluded = ["chest", "hamstrings"]
        result = get_4_day_training_split(excluded, [], self.sets_per_muscle)
        expected = [
            ([
                ('middle back', 3),
                ('biceps', 3),
                ('triceps', 3),
                ('abdominals', 3),
                ('rear delt', 2)
            ], True),
            ([
                ('quadriceps', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('adductors', 2),
                ('calves', 3),
                ('quadriceps', 3)
            ], False),
            ([
                ('lats', 3),
                ('forearms', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('triceps', 3)
            ], True),
            ([
                ('front delt', 3),
                ('quadriceps', 3),
                ('lateral delt', 3),
                ('calves', 3),
                ('abdominals', 3)
            ], True)
        ]
        assert result == expected

    def test_exclude_back_abs_adductors(self):
        excluded = ["middle back", "lats", "abdominals", "adductors"]
        result = get_4_day_training_split(excluded, [], self.sets_per_muscle)
        print(f"4-day split: {result}")
        expected = [
            ([
                ('chest', 3),
                ('biceps', 3),
                ('triceps', 3),
                ('rear delt', 2),
                ('forearms', 3)
            ], True), 
            ([
                ('quadriceps', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('quadriceps', 3)
            ], False),
            ([
                ('chest', 3),
                ('biceps', 3),
                ('triceps', 3),
                ('rear delt', 2),
                ('forearms', 3)
            ], True), 
            ([
                ('hamstrings', 3),
                ('hamstrings', 3),
                ('lateral delt', 3),
                ('front delt', 3),
                ('abductors', 2),
                ('hamstrings', 3),
                ('calves', 3),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected
    
    def test_exclude_back_abs_adds_prefer_lower_back_and_bis(self):
        excluded = ["middle back", "lats", "abdominals", "adductors"]
        preferred = ["lower back", "biceps"]
        result = get_4_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"4-day split: {result}")
        expected = [
            ([
                ('lower back', 2),
                ('biceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('rear delt', 2),
            ], True),
            ([
                ('quadriceps', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('quadriceps', 3)
            ], False), 
            ([
                ('forearms', 3),
                ('chest', 3),
                ('biceps', 3),
                ('triceps', 3),
                ('rear delt', 2),
            ], True), 
            ([
                ('hamstrings', 3),
                ('hamstrings', 3),
                ('lateral delt', 3),
                ('front delt', 3),
                ('abductors', 2),
                ('hamstrings', 3),
                ('calves', 3),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected
    
    def test_exclude_triceps_prefer_back(self):
        excluded = ["triceps"]
        preferred= ["lats", "middle back"]
        result = get_4_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"4-day split: {result}")
        expected = [
            ([
                ('lats', 3),
                ('middle back', 3),
                ('chest', 3),
                ('biceps', 3),
                ('rear delt', 2)
            ], True), 
            ([
                ('quadriceps', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('adductors', 2),
                ('calves', 3),
                ('quadriceps', 3)
            ], False), 
            ([
                ('lats', 3),
                ('biceps', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('forearms', 3),
                ('chest', 3),
                ('chest', 3),
                ('middle back', 3),
                ('biceps', 3)
            ], False),
            ([
                ('hamstrings', 3),
                ('hamstrings', 3),
                ('abdominals', 3),
                ('lateral delt', 3),
                ('front delt', 3),
                ('abdominals', 3),
                ('abductors', 2),
                ('hamstrings', 3),
                ('calves', 3),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected

    def test_exclude_triceps_quads_prefer_back(self):
        excluded = ["quadriceps", "triceps"]
        preferred= ["middle back", "lats"]
        result = get_4_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"4-day split: {result}")
        expected = [
            ([
                ('middle back', 3),
                ('lats', 3),
                ('chest', 3),
                ('biceps', 3),
                ('rear delt', 2)
            ], True), 
            ([
                ('front delt', 3),
                ('hamstrings', 3),
                ('lateral delt', 3),
                ('abdominals', 3),
                ('calves', 3)
            ], True), 
            ([
                ('lats', 3),
                ('biceps', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('forearms', 3),
                ('chest', 3),
                ('chest', 3),
                ('middle back', 3),
                ('biceps', 3)
            ], False),
            ([
                ('hamstrings', 3),
                ('hamstrings', 3),
                ('abdominals', 3),
                ('lateral delt', 3),
                ('front delt', 3),
                ('abdominals', 3),
                ('abductors', 2),
                ('hamstrings', 3),
                ('calves', 3),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected

    def test_exclude_chest_quads_hams_forearms(self):
        excluded = ["chest", "quadriceps", "hamstrings", "forearms"]
        preferred= []
        result = get_4_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"4-day split: {result}")
        expected = [
            ([
                ('middle back', 3),
                ('front delt', 3),
                ('biceps', 3),
                ('triceps', 3),
                ('lateral delt', 3)
            ], True),
            ([
                ('abdominals', 3),
                ('rear delt', 2),
                ('lats', 3),
                ('calves', 3),
                ('middle back', 3)
            ], True),
            ([
                ('front delt', 3),
                ('biceps', 3),
                ('triceps', 3),
                ('lateral delt', 3),
                ('abdominals', 3)
            ], True),
            ([
                ('rear delt', 2),
                ('lats', 3),
                ('calves', 3),
                ('middle back', 3),
                ('abdominals', 3)
            ], True)
        ]
        assert result == expected
        
    def test_exclude_nothing_prefer_glutes_traps_back(self):
        excluded = []
        preferred= ["glutes", "traps", "middle back", "lats"]
        result = get_4_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"4-day split: {result}")
        expected = [
            ([
                ('traps', 2),
                ('middle back', 3),
                ('lats', 3), 
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('biceps', 3),
                ('triceps', 3)
            ], False),
            ([
                ('glutes', 3),
                ('quadriceps', 3),
                ('quadriceps', 3),
                ('calves', 3),
                ('front delt', 3),
                ('lateral delt', 3),
                ('quadriceps', 3),
                ('adductors', 2),
                ('calves', 3),
                ('quadriceps', 3)
            ], False), 
            ([
                ('traps', 2),
                ('lats', 3),
                ('biceps', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('forearms', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('middle back', 3),
                ('biceps', 3)
            ], False), 
            ([
                ('glutes', 3),
                ('glutes', 3),
                ('hamstrings', 3),
                ('hamstrings', 3),
                ('abdominals', 3),
                ('lateral delt', 3),
                ('front delt', 3),
                ('abdominals', 3),
                ('abductors', 2),
                ('hamstrings', 3),
                ('calves', 3),
                ('glutes', 3)
            ], False)
        ]
        assert result == expected