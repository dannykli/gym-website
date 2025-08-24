import pytest
import json
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.buildProgramme.get_training_split.get_1_day_training_split import get_1_day_training_split

class TestGet1DayTrainingSplit:
    def test_empty_arrays(self):
        result = get_1_day_training_split([],[])
        expected = [([
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
        ], True)]
        assert result == expected
    
    def test_excluded_but_no_preferred_1(self):
        excluded = ["quadriceps", "hamstrings"]
        result = get_1_day_training_split(excluded, [])
        expected = [([
            ('chest', 2),
            ('middle back', 2),
            ('front delt', 2),
            ('biceps', 2),
            ('triceps', 2),
            ('lateral delt', 2),
            ('abdominals', 2),
            ('rear delt', 2),
            ('lats', 2),
            ('calves', 2),
            ('forearms', 2)
        ], True)]
        assert result == expected

    def test_excluded_but_no_preferred_2(self):
        excluded = ["lats", "rear delt", "abdominals", "quadriceps", "hamstrings"]
        result = get_1_day_training_split(excluded, [])
        expected = [([
            ('chest', 2),
            ('middle back', 2),
            ('front delt', 2),
            ('biceps', 2),
            ('triceps', 2),
            ('lateral delt', 2),
            ('calves', 2),
            ('forearms', 2)
        ], True)]
        assert result == expected

    def test_excluded_but_no_preferred_3(self):
        excluded = ["chest", "front delt", "lats", "rear delt", "abdominals", "quadriceps", "hamstrings", "lower back"]
        result = get_1_day_training_split(excluded, [])
        expected = [([
            ('middle back', 2),
            ('biceps', 2),
            ('triceps', 2),
            ('lateral delt', 2),
            ('calves', 2),
            ('forearms', 2)
        ], True)]
        assert result == expected
    
    def test_preferred_but_no_excluded_1(self):
        preferred = ["front delt", "calves"]
        result = get_1_day_training_split([], preferred)
        expected = [([
            ('front delt', 2),
            ('calves', 2),
            ('chest', 2),
            ('middle back', 2),
            ('quadriceps', 2),
            ('biceps', 2),
            ('triceps', 2),
            ('hamstrings', 2),
            ('lateral delt', 2),
            ('abdominals', 2),
            ('rear delt', 2),
            ('lats', 2),
            ('forearms', 2)
        ], True)]
        assert expected == result

    def test_preferred_but_no_excluded_2(self):
        preferred = ["front delt", "calves", "lower back", "traps"]
        result = get_1_day_training_split([], preferred)
        expected = [([
            ('front delt', 2),
            ('calves', 2),
            ('lower back', 2),
            ('traps', 2),
            ('chest', 2),
            ('middle back', 2),
            ('quadriceps', 2),
            ('biceps', 2),
            ('triceps', 2),
            ('hamstrings', 2),
            ('lateral delt', 2),
            ('abdominals', 2),
            ('rear delt', 2),
            ('lats', 2),
            ('forearms', 2)
        ], True)]

    def test_preferred_and_excluded_1(self):
        preferred = ["front delt", "calves", "lower back", "traps"]
        excluded = ["abdominals", "forearms"]
        result = get_1_day_training_split(excluded, preferred)
        expected = [([
            ('front delt', 2),
            ('calves', 2),
            ('lower back', 2),
            ('traps', 2),
            ('chest', 2),
            ('middle back', 2),
            ('quadriceps', 2),
            ('biceps', 2),
            ('triceps', 2),
            ('hamstrings', 2),
            ('lateral delt', 2),
            ('rear delt', 2),
            ('lats', 2),
        ], True)]
        assert expected == result
    
    def test_preferred_and_excluded_2(self):
        preferred = ["forearms", "calves"]
        excluded = ["chest", "middle back"]
        result = get_1_day_training_split(excluded, preferred)
        expected = [([
            ('forearms', 2),
            ('calves', 2),
            ('front delt', 2),
            ('quadriceps', 2),
            ('biceps', 2),
            ('triceps', 2),
            ('hamstrings', 2),
            ('lateral delt', 2),
            ('abdominals', 2),
            ('rear delt', 2),
            ('lats', 2)
        ], True)]
        assert expected == result
    