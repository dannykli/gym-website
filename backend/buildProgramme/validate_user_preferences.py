def validate_excluded_muscle_groups(excluded_muscle_groups, valid_muscle_groups):
    # "shoulders" -> "front delt", "lateral delt", "rear delt"
    # "back" -> "middle back", "lats"
    new_excluded = []
    muscle_groups = set(valid_muscle_groups)
    for muscle_group in excluded_muscle_groups:
        if muscle_group == "shoulders":
            new_excluded.append("front delt")
            new_excluded.append("lateral delt")
            new_excluded.append("rear delt")
        elif muscle_group == "back":
            new_excluded.append("middle back")
            new_excluded.append("lats")
        elif muscle_group in muscle_groups:
            new_excluded.append(muscle_group)
        else:
            print(f"Error: Did not recognise muscle group '{muscle_group}' in excludedMuscleGroups array")
    
    return new_excluded


def validate_preferred_muscle_groups(preferred_muscle_groups, excluded_muscle_groups, valid_muscle_groups):
    # Validate that preferred_muscle_groups is at most length 3
    if len(preferred_muscle_groups) > 3:
        print(f"Error: preferredMuscleGroups array is too long. Length is {len(preferred_muscle_groups)}")
        preferred_muscle_groups = preferred_muscle_groups[:3]
    
    # "shoulders" -> "front delt", "lateral delt", "rear delt"
    # "back" -> "middle back", "lats"
    new_preferred = []
    muscle_groups = set(valid_muscle_groups)
    for muscle_group in preferred_muscle_groups:
        if muscle_group == "shoulders":
            new_preferred.append("front delt")
            new_preferred.append("lateral delt")
            new_preferred.append("rear delt")
        elif muscle_group == "back":
            new_preferred.append("middle back")
            new_preferred.append("lats")
        elif muscle_group in muscle_groups:
            new_preferred.append(muscle_group)
        else:
            print(f"Error: Did not recognise muscle group '{muscle_group}' in preferredMuscleGroups array")
    
    # If a muscle group is preferred but also excluded, remove from preferred
    excluded_set = set(excluded_muscle_groups)
    for muscle_group in new_preferred:
        if muscle_group in excluded_set:
            new_preferred.remove(muscle_group)
    
    return new_preferred

def validate_equipment(equipment, valid_equipment):
    valid_equipment_set = set(valid_equipment)
    new_equipment = ["body only"]
    for item in equipment:
        if item in valid_equipment_set:
            new_equipment.append(item)
        else:
            print(f"Error: Did not recognise item '{item}' in equipment array")
    return new_equipment

'''
def validate_excluded_exercises(excluded_exercises, valid_exercises):
    exercise_set = set(valid_exercises)
    for exercise in excluded_exercises:
        if exercise not in exercise_set:
            print(f"Error: Did not recognise exercise '{exercise}' in excluded exercises array")
            excluded_exercises.remove(exercise)
'''
    
