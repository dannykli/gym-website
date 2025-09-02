from get_training_split.get_training_split_utils import orderMuscleGroups, removeLastOccurrence, initialiseOrderedMuscleGroups

# pre: excluded_muscle_groups, preferred_muscle_groups are both arrays with valid muscle group values 
#      and excluded_muscle_groups and preferred_muscle_groups share no common values
def get_3_day_training_split(excluded_muscle_groups, preferred_muscle_groups, sets_per_muscle):
    push = ["chest", "triceps", "front delt", "lateral delt", "chest", "triceps", "chest", "triceps", "front delt", "traps"]
    pull = ["middle back", "biceps", "lats", "rear delt", "biceps", "forearms", "middle back", "traps", "biceps", "lats"]
    legs = ["quadriceps", "hamstrings", "calves", "abdominals", "quadriceps", "hamstrings", "adductors", "abductors", "abdominals", "quadriceps", "calves", "abdominals", "glutes"]
    
    day_1_muscle_groups = push.copy()
    day_2_muscle_groups = pull.copy()
    day_3_muscle_groups = legs.copy()

    # indicates whether day_1/2/3 need to be replaced with a FULL BODY focus
    day_1_requires_mod = False
    day_2_requires_mod = False
    day_3_requires_mod = False

    for muscle_group in excluded_muscle_groups:
        if (muscle_group == "front delt" or muscle_group == "lateral delt"):
            day_1_muscle_groups = [x for x in day_1_muscle_groups if x != muscle_group]
        elif (muscle_group == "traps"):
            day_1_muscle_groups.remove(muscle_group)
            day_2_muscle_groups.remove(muscle_group)
        elif (muscle_group == "rear delt" or muscle_group == "forearms"):
            day_2_muscle_groups.remove(muscle_group)
        elif (muscle_group == "abdominals" or muscle_group == "adductors" or muscle_group == "abductors" or 
            muscle_group == "calves" or muscle_group == "glutes"):
            day_3_muscle_groups = [x for x in day_3_muscle_groups if x != muscle_group]
        elif (muscle_group == "chest" or muscle_group == "triceps"):
            day_1_requires_mod = True
        elif (muscle_group == "middle back" or muscle_group == "lats" or muscle_group == "biceps"):
            day_2_requires_mod = True
        elif (muscle_group == "quadriceps" or muscle_group == "hamstrings"):
            day_3_requires_mod = True
        elif (muscle_group == "lower back"):
            pass
        else:
            print(f"Error: Did not recognise muscle group '{muscle_group}' in excludedMuscleGroups array")

    # Check day_k_muscle_groups array has not decreased too much, if it has, it requires modification
    if not day_1_requires_mod and len(day_1_muscle_groups) < 0.6 * len(push):
        day_1_requires_mod = True
    if not day_2_requires_mod and len(day_2_muscle_groups) < 0.6 * len(pull):
        day_2_requires_mod = True
    if not day_3_requires_mod and len(day_3_muscle_groups) < 0.6 * len(legs):
        day_3_requires_mod = True

    further_modifications_required = day_1_requires_mod or day_2_requires_mod or day_3_requires_mod

    if further_modifications_required:
        used_preferred_muscle_groups = False
        if day_1_requires_mod:
            ordered_muscle_groups = initialiseOrderedMuscleGroups(excluded_muscle_groups)

            # prioritise muscle groups not trained in day 2 if not subject to change
            if not day_2_requires_mod:
                low_priority_muscle_groups = set(day_2_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 3 if not subject to change
            if not day_3_requires_mod:
                low_priority_muscle_groups = set(day_3_muscle_groups) # O(1) lookups
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
            # then prioritise muscle groups not selected for day 1 for future possible uses for day 2 and 3
            # ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], ordered_muscle_groups[no_of_muscle_groups_to_train:])
    
        if day_2_requires_mod:
            ordered_muscle_groups = initialiseOrderedMuscleGroups(excluded_muscle_groups)

            # prioritise muscle groups not trained in day 1
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

            # select correct number of muscle groups to train
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

            # if only day 3 requires change, modify day 3 to be SARMS focused
            if not day_1_requires_mod and not day_2_requires_mod:
                sarms_muscle_groups = ["biceps", "triceps", "front delt", "lateral delt", "forearms"]
                # remove any excluded muscle groups required by user
                sarms_muscle_groups = [x for x in sarms_muscle_groups if x not in excluded_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], sarms_muscle_groups)

            no_of_muscle_groups_to_train = 5
            if not used_preferred_muscle_groups:
                # priortise user-preferred muscle groups
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], preferred_muscle_groups)
                used_preferred_muscle_groups = True

                # check if shoulders are preferred and if so, increase number of muscle groups to train
                if "front delt" in preferred_muscle_groups:
                    no_of_muscle_groups_to_train = 6 

            # choose muscle groups to train
            day_3_muscle_groups = ordered_muscle_groups[:no_of_muscle_groups_to_train]
    else:
        # logic for prioritising preferred muscle groups for unmodified PUSH/PULL/LEGS
        '''
        push_muscle_groups = ["chest", "triceps", "front delt", "lateral delt", "chest", "triceps", "chest", "triceps, "front delt", "traps"]
        pull_muscle_groups = ["middle back", "biceps", "lats", "rear delt", "biceps", "forearms", "middle back", "traps", "biceps", "lats"]
        legs_muscle_groups = ["quadriceps", "hamstrings", "calves", "abdominals", "quadriceps", "hamstrings", "adductors", "abductors", "abdominals", "quadriceps", "calves", "abdominals", "glutes"]
        '''
        # reverse preferred muscle groups so most important is last in list and thus gets greatest priority
        preferred_muscle_groups.reverse()
        for muscle_group in preferred_muscle_groups:
            if muscle_group == "chest" or muscle_group == "triceps":
                day_1_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "front delt" or muscle_group == "lateral delt":
                day_1_muscle_groups.remove(muscle_group) # first occurence
                day_1_muscle_groups.insert(0, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "lats" or muscle_group == "traps" or muscle_group == "forearms" or muscle_group == "rear delt" or muscle_group == "lower back":
                day_2_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "biceps":
                day_2_muscle_groups = removeLastOccurrence(day_2_muscle_groups, muscle_group)
                day_2_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "quadriceps" or muscle_group == "calves":
                day_3_muscle_groups = removeLastOccurrence(day_3_muscle_groups, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
            elif (muscle_group == "hamstrings" or muscle_group == "abdominals" or muscle_group == "adductors"
                    or muscle_group == "abductors"):
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "glutes":
                day_3_muscle_groups = [muscle_group, muscle_group] + day_3_muscle_groups
            elif muscle_group == "middle back":
                day_2_muscle_groups.remove(muscle_group) # first occurence
                day_2_muscle_groups.insert(0, muscle_group)
            else:
                print(f"Error: did not recognise muscle group {muscle_group}")
    
    day_1_sets = map(lambda muscle: sets_per_muscle[muscle], day_1_muscle_groups)
    day_2_sets = map(lambda muscle: sets_per_muscle[muscle], day_2_muscle_groups)
    day_3_sets = map(lambda muscle: sets_per_muscle[muscle], day_3_muscle_groups)

    day_1 = list(zip(day_1_muscle_groups, day_1_sets))
    day_2 = list(zip(day_2_muscle_groups, day_2_sets))
    day_3 = list(zip(day_3_muscle_groups, day_3_sets))
    return [(day_1, day_1_requires_mod), (day_2, day_2_requires_mod), (day_3, day_3_requires_mod)]