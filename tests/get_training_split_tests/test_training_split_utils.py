import pytest
import json
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.buildProgramme_Local.get_training_split.get_training_split_utils import orderMuscleGroups, removeLastOccurrence, initialiseOrderedMuscleGroups

class TestGet1DayTrainingSplit:
    def test_orderMuscleGroups(self):
        excluded = ["lower back", "hamstrings"]
        preferred= ["glutes", "traps", "middle back", "lats"]
        muscle_groups = ["chest", "middle back", "front delt", "quadriceps", "biceps", "triceps", "hamstrings", "lateral delt", 
        "abdominals", "rear delt", "lats", "calves", "forearms"]
        result = orderMuscleGroups(muscle_groups, excluded, preferred)
        expected = ["glutes", "traps", "middle back", "lats", "chest", "front delt", "quadriceps", "biceps", "triceps", "lateral delt", 
        "abdominals", "rear delt", "calves", "forearms"]
        assert result == expected

    def test_removeLastOccurence(self):
        lst = ["a", "a", "b", "c", "a", "b"]
        result = removeLastOccurrence(lst, "a")
        expected = ["a", "a", "b", "c", "b"]
        assert result == expected
      
    def test_initialiseOrderedMuscleGroups(self):
        excluded = ["hamstrings", "rear delt"]
        result = initialiseOrderedMuscleGroups(excluded)
        expected = ["chest", "middle back", "front delt", "quadriceps", "biceps", "triceps", "lateral delt", 
        "abdominals", "lats", "calves", "forearms"]
        assert result == expected
  