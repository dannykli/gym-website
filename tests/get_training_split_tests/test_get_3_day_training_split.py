import pytest
import json
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.buildProgramme.get_training_split.get_3_day_training_split import get_3_day_training_split

class TestGet3DayTrainingSplit:
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
        result = get_3_day_training_split([], [], self.sets_per_muscle)
        print(f"3-day split: {result}")
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
          ], False)
        ]
        assert result == expected
    
    def test_exclude_minor_muscles(self):
        excluded = ["traps", "forearms", "abdominals"]
        result = get_3_day_training_split(excluded, [], self.sets_per_muscle)
        print(f"3-day split: {result}")
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
              ('calves', 3),
              ('quadriceps', 3),
              ('hamstrings', 3),
              ('adductors', 2),
              ('abductors', 2),
              ('quadriceps', 3),
              ('calves', 3),
              ('glutes', 3)
          ], False)
        ]
        assert result == expected

    def test_exclude_chest(self):
        excluded = ["chest"]
        result = get_3_day_training_split(excluded, [], self.sets_per_muscle)
        print(f"3-day split: {result}")
        expected = [
            ([
                ('front delt', 3),
                ('triceps', 3),
                ('lateral delt', 3),
                ('middle back', 3),
                ('biceps', 3)
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
            ], False)
        ]
        assert result == expected

    def test_exclude_chest_triceps(self):
        excluded = ["chest", "triceps"]
        result = get_3_day_training_split(excluded, [], self.sets_per_muscle)
        print(f"3-day split: {result}")
        expected = [
            ([
                ('front delt', 3),
                ('lateral delt', 3),
                ('middle back', 3),
                ('biceps', 3),
                ('rear delt', 2),
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
            ], False)
        ]
        assert result == expected
    
    def test_exclude_back(self):
        excluded = ["middle back", "lats"]
        result = get_3_day_training_split(excluded, [], self.sets_per_muscle)
        print(f"3-day split: {result}")
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
                ('front delt', 3)
            ], True),
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
            ], False)
        ]
        assert result == expected
    
    def test_exclude_back_prefer_chest(self):
        excluded = ["middle back", "lats"]
        preferred= ["chest"]
        result = get_3_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"3-day split: {result}")
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
                ('chest', 3),
                ('biceps', 3),
                ('rear delt', 2),
                ('forearms', 3),
                ('front delt', 3)
            ], True),
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
            ], False)
        ]
        assert result == expected

    def test_exclude_quads_prefer_shoulders(self):
        excluded = ["quadriceps"]
        preferred= ["front delt", "lateral delt", "rear delt", "lower back"]
        result = get_3_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"3-day split: {result}")
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
                ('front delt', 3),
                ('lateral delt', 3),
                ('rear delt', 2),
                ('lower back', 2),
                ('biceps', 3),
                ('triceps', 3)
            ], True)
        ]
        assert result == expected

    def test_exclude_nothing_prefer_shoulders(self):
        excluded = []
        preferred= ["front delt", "lateral delt", "rear delt"]
        result = get_3_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"3-day split: {result}")
        expected = [
            ([
                ('lateral delt', 3),
                ('front delt', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('chest', 3),
                ('triceps', 3),
                ('front delt', 3),
                ('traps', 2)
            ], False),
            ([
                ('rear delt', 2),
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
                ('lateral delt', 3),
                ('front delt', 3),
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
            ], False)
        ]
        
    def test_exclude_nothing_prefer_glutes_traps_back(self):
        excluded = []
        preferred= ["glutes", "traps", "middle back", "lats"]
        result = get_3_day_training_split(excluded, preferred, self.sets_per_muscle)
        print(f"3-day split: {result}")
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
                ('biceps', 3),
                ('lats', 3)
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
            ], False)
        ]
        assert result == expected