import pytest
import json
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.buildProgramme_Local.validate_user_preferences import validate_excluded_muscle_groups
from backend.buildProgramme_Local.validate_user_preferences import validate_preferred_muscle_groups
from backend.buildProgramme_Local.validate_user_preferences import validate_equipment

class TestValidateUserPreferences:
    def test_validate_excluded_muscle_groups(self):
        valid = [
            "abdominals", "abductors", "adductors", "biceps", "front delt", "lateral delt", "rear delt",
            "calves", "chest", "forearms", "glutes", "hamstrings", "quadriceps", "lower back",
            "middle back", "lats", "traps", "triceps"
        ]
        excluded = ["abc", "abdominals", "back", "shoulders", "def", "triceps"]
        result = validate_excluded_muscle_groups(excluded, valid)
        expected = [
            "abdominals", "middle back", "lats", "front delt", "lateral delt", "rear delt", "triceps"
        ]
        assert result == expected
    
    def test_validate_preferred_muscle_groups(self):
        valid = [
            "abdominals", "abductors", "adductors", "biceps", "front delt", "lateral delt", "rear delt",
            "calves", "chest", "forearms", "glutes", "hamstrings", "quadriceps", "lower back",
            "middle back", "lats", "traps", "triceps"
        ]
        excluded = ["abdominals", "middle back", "lats", "front delt", "lateral delt", "rear delt", "triceps"]
        preferred = ["triceps", "biceps", "traps", "abc"]
        result = validate_preferred_muscle_groups(preferred, excluded, valid)
        expected = [
            "biceps", "traps"
        ]
        assert result == expected

    def test_validate_equipment(self):
        user_equipment = ["bands", "abc", "ab roller", "barbell", "dumbbell"]
        valid_equipment = ["body only", "bands", "kettlebells", "cable", "ab roller", "barbell", "machine", "exercise ball",
            "e-z curl bar", "medicine ball", "dip bar", "dumbbell", "bench", "pull up bar"]
        result = validate_equipment(user_equipment, valid_equipment)
        expected = [
            "body only", "bands", "ab roller", "barbell", "dumbbell"
        ]
        assert expected == result

    