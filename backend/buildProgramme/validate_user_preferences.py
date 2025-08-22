def validate_excluded_muscle_groups(excluded_muscle_groups, valid_muscle_groups):
    # "shoulders" -> "front delt", "lateral delt", "rear delt"
    # "back" -> "middle back", "lats"
    muscle_groups = set(valid_muscle_groups)
    for muscle_group in excluded_muscle_groups:
        if muscle_group == "shoulders":
            excluded_muscle_groups.append("front delt")
            excluded_muscle_groups.append("lateral delt")
            excluded_muscle_groups.append("rear delt")
            excluded_muscle_groups.remove(muscle_group)
        elif muscle_group == "back":
            excluded_muscle_groups.append("middle back")
            excluded_muscle_groups.append("lats")
            excluded_muscle_groups.remove(muscle_group)
        elif muscle_group not in muscle_groups:
            excluded_muscle_groups.remove(muscle_group)
            print(f"Error: Did not recognise muscle group '{muscle_group}' in excludedMuscleGroups array")


def validate_preferred_muscle_groups(preferred_muscle_groups, excluded_muscle_groups, valid_muscle_groups):
    # Validate that preferred_muscle_groups is at most length 3
    if len(preferred_muscle_groups) > 3:
        print(f"Error: preferredMuscleGroups array is too long. Length is {len(preferred_muscle_groups)}")
        preferred_muscle_groups = preferred_muscle_groups[:3]
    
    # "shoulders" -> "front delt", "lateral delt", "rear delt"
    # "back" -> "middle back", "lats"
    muscle_groups = set(valid_muscle_groups)
    for muscle_group in preferred_muscle_groups:
        if muscle_group == "shoulders":
            preferred_muscle_groups.append("front delt")
            preferred_muscle_groups.append("lateral delt")
            preferred_muscle_groups.append("rear delt")
            preferred_muscle_groups.remove(muscle_group)
        elif muscle_group == "back":
            preferred_muscle_groups.append("middle back")
            preferred_muscle_groups.append("lats")
            preferred_muscle_groups.remove(muscle_group)
        elif muscle_group not in muscle_groups:
            preferred_muscle_groups.remove(muscle_group)
            print(f"Error: Did not recognise muscle group '{muscle_group}' in preferredMuscleGroups array")
    
    # If a muscle group is preferred but also excluded, remove from preferred
    excluded_set = set(excluded_muscle_groups)
    for muscle_group in preferred_muscle_groups:
        if muscle_group in excluded_set:
            preferred_muscle_groups.remove(muscle_group)

def validate_equipment(equipment, valid_equipment):
    valid_equipment_set = set(valid_equipment)
    equipment.append("body only")
    for item in equipment:
        if item not in valid_equipment_set:
            print(f"Error: Did not recognise item '{item}' in equipment array")
            equipment.remove(item)

def validate_excluded_exercises(excluded_exercises, valid_exercises):
    exercise_set = set(valid_exercises)
    for exercise in excluded_exercises:
        if exercise not in exercise_set:
            print(f"Error: Did not recognise exercise '{exercise}' in excluded exercises array")
            excluded_exercises.remove(exercise)

    
