from .get_training_split_utils import orderMuscleGroups, removeLastOccurrence, initialiseOrderedMuscleGroups

# pre: excluded_muscle_groups, preferred_muscle_groups are both arrays with valid muscle group values 
#      and excluded_muscle_groups and preferred_muscle_groups share no common values
def get_4_day_training_split(excluded_muscle_groups, preferred_muscle_groups, sets_per_muscle):
    # UPPER/LOWER x2 subject to modifications if excluded exercises dictate
    upper_1 = ["chest", "triceps", "chest", "triceps", "chest", "traps", "middle back", "biceps", "lats", "triceps" ]
    lower_1 = ["quadriceps", "quadriceps", "calves", "front delt", "lateral delt", "quadriceps", "adductors", "calves", "quadriceps"]
    upper_2 = ["lats", "biceps", "middle back", "biceps", "rear delt", "forearms", "chest", "triceps", "chest", "middle back", "biceps"]
    lower_2 = ["hamstrings", "hamstrings", "abdominals", "lateral delt", "front delt", "abdominals", "abductors", "hamstrings", "calves", "glutes"]

    day_1_muscle_groups = upper_1
    day_2_muscle_groups = lower_1
    day_3_muscle_groups = upper_2
    day_4_muscle_groups = lower_2

    # indicates whether day_1/2/3/4 need to be replaced with a different muscle focus
    day_1_requires_mod = False
    day_2_requires_mod = False
    day_3_requires_mod = False
    day_4_requires_mod = False

    for muscle_group in excluded_muscle_groups:
        if muscle_group == "front delt" or muscle_group == "lateral delt":
            day_2_muscle_groups.remove(muscle_group)
            day_4_muscle_groups.remove(muscle_group)
        elif muscle_group == "rear delt" or muscle_group == "forearms":
            day_3_muscle_groups.remove(muscle_group)
        elif muscle_group == "traps":
            day_1_muscle_groups.remove(muscle_group)
        elif muscle_group == "adductors":
            day_2_muscle_groups.remove(muscle_group)
        elif muscle_group == "abductors":
            day_4_muscle_groups.remove(muscle_group)
        elif muscle_group == "abdominals":
            day_4_muscle_groups = [x for x in day_4_muscle_groups if x != muscle_group]
        elif muscle_group == "calves":
            day_2_muscle_groups = [x for x in day_2_muscle_groups if x != muscle_group]
            day_4_muscle_groups.remove(muscle_group)
        elif muscle_group == "triceps":
            day_1_requires_mod = True
            day_3_muscle_groups.remove(muscle_group)
        elif muscle_group == "biceps":
            day_3_requires_mod = True
            day_1_muscle_groups.remove(muscle_group)
        elif muscle_group == "chest" or muscle_group == "middle back" or muscle_group == "lats":
            day_1_requires_mod = True
            day_3_requires_mod = True
        elif muscle_group == "quadriceps":
            day_2_requires_mod = True
        elif muscle_group == "hamstrings":
            day_4_requires_mod = True
        elif muscle_group == "lower back":
            pass
        else:
            print(f"Error: did not recognise muscle group {muscle_group}")
    
    further_modifications_required = day_1_requires_mod or day_2_requires_mod or day_3_requires_mod or day_4_requires_mod

    if further_modifications_required:

        used_preferred_muscle_groups = False
        if day_1_requires_mod:
            ordered_muscle_groups = initialiseOrderedMuscleGroups(excluded_muscle_groups)
            # prioritise muscle groups not trained in day 3 if not subject to change
            if not day_3_requires_mod:
                low_priority_muscle_groups = set(day_3_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 2 if not subject to change
            if not day_2_requires_mod:
                low_priority_muscle_groups = set(day_2_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 4 if not subject to change
            if not day_4_requires_mod:
                low_priority_muscle_groups = set(day_4_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            
            # lastly prioritise preferred muscle groups
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], preferred_muscle_groups)

            no_of_muscle_groups_to_train = 5
            # check if shoulders are preferred and if so, increase number of muscle groups to train
            if "front delt" in preferred_muscle_groups:
                no_of_muscle_groups_to_train = 6 

            used_preferred_muscle_groups = True

            # select correct number of muscle groups to train
            day_1_muscle_groups = ordered_muscle_groups[:no_of_muscle_groups_to_train]

        if day_2_requires_mod:
            ordered_muscle_groups = initialiseOrderedMuscleGroups(excluded_muscle_groups)

            # prioritise muscle groups not trained in day 4 if not subject to change
            if not day_4_requires_mod:
                low_priority_muscle_groups = set(day_4_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # priortise muscle groups not trained in day 1
            low_priority_muscle_groups = set(day_1_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 3 if not subject to change
            if not day_3_requires_mod:
                low_priority_muscle_groups = set(day_3_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            no_of_muscle_groups_to_train = 5

            if not used_preferred_muscle_groups:
                # priortise user-preferred muscle groups
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], preferred_muscle_groups)
                used_preferred_muscle_groups = True

                # check if shoulders are preferred and if so, increase number of muscle groups to train
                if "front delt" in preferred_muscle_groups:
                    no_of_muscle_groups_to_train = 6 

            # select muscle groups to train
            day_2_muscle_groups = ordered_muscle_groups[:no_of_muscle_groups_to_train]
        
        if day_3_requires_mod:
            ordered_muscle_groups = initialiseOrderedMuscleGroups(excluded_muscle_groups)

            # prioritise muscle groups not trained in day 1
            low_priority_muscle_groups = set(day_1_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 2
            low_priority_muscle_groups = set(day_2_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            
            # prioritise muscle groups not trained in day 4 if not subject to change
            if not day_4_requires_mod:
                low_priority_muscle_groups = set(day_4_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            no_of_muscle_groups_to_train = 5

            if not used_preferred_muscle_groups:
                # priortise user-preferred muscle groups
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], preferred_muscle_groups)
                used_preferred_muscle_groups = True

                # check if shoulders are preferred and if so, increase number of muscle groups to train
                if "front delt" in preferred_muscle_groups:
                    no_of_muscle_groups_to_train = 6 

            # select muscle groups to train
            day_3_muscle_groups = ordered_muscle_groups[:no_of_muscle_groups_to_train]

        if day_4_requires_mod:
            ordered_muscle_groups = initialiseOrderedMuscleGroups(excluded_muscle_groups)

            # prioritise muscle groups not trained in day 2
            low_priority_muscle_groups = set(day_2_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 1
            low_priority_muscle_groups = set(day_1_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
                
            # prioritise muscle groups not trained in day 3
            low_priority_muscle_groups = set(day_3_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            no_of_muscle_groups_to_train = 5
            if not used_preferred_muscle_groups:
                # priortise user-preferred muscle groups
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], preferred_muscle_groups)
                used_preferred_muscle_groups = True

                # check if shoulders are preferred and if so, increase number of muscle groups to train
                if "front delt" in preferred_muscle_groups:
                    no_of_muscle_groups_to_train = 6

            # select muscle groups to train
            day_4_muscle_groups = ordered_muscle_groups[:no_of_muscle_groups_to_train]
    else:
        # logic for prioritising preferred muscle groups for unmodified UPPER/LOWER x2
        '''
        upper_1 = ["chest", "triceps", "chest", "triceps", "chest", "traps", "middle back", "biceps", "lats", "triceps" ]
        lower_1 = ["quadriceps", "quadriceps", "calves", "front delt", "lateral delt", "quadriceps", "adductors", "calves", "quadriceps"]
        upper_2 = ["lats", "biceps", "middle back", "biceps", "rear delt", "forearms", "chest", "triceps", "chest", "middle back", "biceps"]
        lower_2 = ["hamstrings", "hamstrings", "abdominals", "lateral delt", "front delt", "abdominals", "abductors", "hamstrings", "calves", "glutes"]
        '''
        for muscle_group in preferred_muscle_groups:
            if muscle_group == "chest":
                day_1_muscle_groups.remove(muscle_group) # first occurence
                day_1_muscle_groups.insert(0, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "triceps":
                day_1_muscle_groups = removeLastOccurrence(day_1_muscle_groups, muscle_group)
                day_1_muscle_groups.insert(0, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "middle back": 
                day_1_muscle_groups = removeLastOccurrence(day_1_muscle_groups, muscle_group)
                day_1_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "lats":
                day_1_muscle_groups = removeLastOccurrence(day_1_muscle_groups, muscle_group)
                day_1_muscle_groups.insert(0, muscle_group)
                day_3_muscle_groups.remove(muscle_group) # first occurence
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "traps":
                day_1_muscle_groups = removeLastOccurrence(day_1_muscle_groups, muscle_group)
                day_1_muscle_groups.insert(0, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "front delt" or muscle_group == "lateral delt":
                day_2_muscle_groups = removeLastOccurrence(day_2_muscle_groups, muscle_group)
                day_2_muscle_groups.insert(0, muscle_group)
                day_4_muscle_groups = removeLastOccurrence(day_4_muscle_groups, muscle_group)
                day_4_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "adductors":
                day_2_muscle_groups = removeLastOccurrence(day_2_muscle_groups, muscle_group)
                day_2_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "abductors":
                day_4_muscle_groups = removeLastOccurrence(day_4_muscle_groups, muscle_group)
                day_4_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "biceps":
                day_1_muscle_groups.insert(0, muscle_group)
                day_3_muscle_groups = removeLastOccurrence(day_3_muscle_groups, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "rear delt":
                day_3_muscle_groups = removeLastOccurrence(day_3_muscle_groups, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "forearms":
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "glutes":
                day_2_muscle_groups.insert(0, muscle_group)
                day_4_muscle_groups = [muscle_group, muscle_group] + day_4_muscle_groups
            elif muscle_group == "abdominals" or muscle_group == "lower back":
                day_4_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "quadriceps":
                day_2_muscle_groups = day_2_muscle_groups.remove(muscle_group) # first occurence
                day_2_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "hamstrings":
                day_4_muscle_groups = day_4_muscle_groups.remove(muscle_group) # first occurence
                day_4_muscle_groups.insert(0, muscle_group)
            else:
                print(f"Error: did not recognise muscle group {muscle_group}")

    day_1_sets = map(lambda muscle: sets_per_muscle[muscle], day_1_muscle_groups)
    day_2_sets = map(lambda muscle: sets_per_muscle[muscle], day_2_muscle_groups)
    day_3_sets = map(lambda muscle: sets_per_muscle[muscle], day_3_muscle_groups)
    day_4_sets = map(lambda muscle: sets_per_muscle[muscle], day_4_muscle_groups)

    day_1 = list(zip(day_1_muscle_groups, day_1_sets))
    day_2 = list(zip(day_2_muscle_groups, day_2_sets))
    day_3 = list(zip(day_3_muscle_groups, day_3_sets))
    day_4 = list(zip(day_4_muscle_groups, day_4_sets))
    return [day_1, day_2, day_3, day_4]