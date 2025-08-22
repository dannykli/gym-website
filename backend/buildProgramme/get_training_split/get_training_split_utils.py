def orderMuscleGroups(possible_muscle_groups, excluded_muscle_groups, preferred_muscle_groups):
    ordered_muscle_groups = preferred_muscle_groups.copy()
    for muscle_group in possible_muscle_groups:
        if muscle_group not in ordered_muscle_groups and muscle_group not in excluded_muscle_groups:
            ordered_muscle_groups.append(muscle_group)
    return ordered_muscle_groups

def removeLastOccurrence(lst, value):
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == value:
            del lst[i]
            break
    return lst

def initialiseOrderedMuscleGroups(excluded_muscle_groups):
    muscle_groups = ["chest", "middle back", "front delt", "quadriceps", "biceps", "triceps", "hamstrings", "lateral delt", 
        "abdominals", "rear delt", "lats", "calves", "forearms"]
    ordered_muscle_groups = orderMuscleGroups(muscle_groups, excluded_muscle_groups, [])
    return ordered_muscle_groups

        