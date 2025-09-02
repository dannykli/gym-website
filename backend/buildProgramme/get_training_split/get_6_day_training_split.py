from get_training_split.get_training_split_utils import orderMuscleGroups, removeLastOccurrence, initialiseOrderedMuscleGroups

# pre: excluded_muscle_groups, preferred_muscle_groups are both arrays with valid muscle group values 
#      and excluded_muscle_groups and preferred_muscle_groups share no common values
def get_6_day_training_split(excluded_muscle_groups, preferred_muscle_groups, sets_per_muscle):
    push = ["chest", "triceps", "front delt", "lateral delt", "chest", "triceps", "chest", "triceps", "front delt", "traps"]
    pull = ["middle back", "biceps", "lats", "rear delt", "biceps", "forearms", "middle back", "traps", "biceps", "lats"]
    legs_1 = ["quadriceps", "quadriceps", "calves", "abdominals", "quadriceps", "adductors", "hamstrings", "abdominals", "calves", "front delt", "hamstrings", "glutes"]
    chest_n_back = ["chest", "middle back", "chest", "lats", "chest", "middle back", "rear delt", "traps", "chest", "lats", "lateral delt"]
    sarms = ["triceps", "biceps", "lateral delt", "front delt", "triceps", "biceps", "forearms", "front delt", "triceps", "biceps", "forearms"]
    legs_2 = ["hamstrings", "hamstrings", "abdominals", "calves", "quadriceps", "abductors", "lower back", "quadriceps", "calves", "abdominals", "hamstrings", "glutes"]

    day_1_muscle_groups = push.copy()
    day_2_muscle_groups = pull.copy()
    day_3_muscle_groups = legs_1.copy()
    day_4_muscle_groups = chest_n_back.copy()
    day_5_muscle_groups = sarms.copy()
    day_6_muscle_groups = legs_2.copy()

    # indicates whether day_1/2/3 need to be replaced with a FULL BODY focus
    day_1_requires_mod = False
    day_2_requires_mod = False
    day_3_requires_mod = False
    day_4_requires_mod = False
    day_5_requires_mod = False
    day_6_requires_mod = False

    for muscle_group in excluded_muscle_groups:
        if muscle_group == "front delt":
            day_1_muscle_groups = [x for x in day_1_muscle_groups if x != muscle_group]
            day_5_muscle_groups = [x for x in day_5_muscle_groups if x != muscle_group]
        elif muscle_group == "lateral delt":
            day_1_muscle_groups.remove(muscle_group)
            day_4_muscle_groups.remove(muscle_group)
            day_5_muscle_groups.remove(muscle_group)
        elif muscle_group == "traps":
            day_1_muscle_groups.remove(muscle_group)
            day_2_muscle_groups.remove(muscle_group)
            day_4_muscle_groups.remove(muscle_group)
        elif muscle_group == "forearms":
            day_2_muscle_groups.remove(muscle_group)
            day_5_muscle_groups = [x for x in day_5_muscle_groups if x != muscle_group]
        elif muscle_group == "rear delt":
            day_2_muscle_groups.remove(muscle_group)
            day_4_muscle_groups.remove(muscle_group)
        elif (muscle_group == "abdominals" or muscle_group == "adductors" or muscle_group == "abductors" or 
            muscle_group == "calves" or muscle_group == "glutes"):
            day_3_muscle_groups = [x for x in day_3_muscle_groups if x != muscle_group]
            day_6_muscle_groups = [x for x in day_6_muscle_groups if x != muscle_group] 
        elif muscle_group == "chest":
            day_1_requires_mod = True
            day_4_requires_mod = True
        elif muscle_group == "triceps":
            day_1_requires_mod = True
            day_5_requires_mod = True
        elif muscle_group == "middle back" or muscle_group == "lats":
            day_2_requires_mod = True
            day_4_requires_mod = True
        elif muscle_group == "biceps":
            day_2_requires_mod = True
            day_5_requires_mod = True
        elif muscle_group == "quadriceps":
            day_3_requires_mod = True
            day_6_muscle_groups = [x for x in day_6_muscle_groups if x != muscle_group]
        elif muscle_group == "hamstrings":
            day_3_muscle_groups = [x for x in day_3_muscle_groups if x != muscle_group]
            day_6_requires_mod = True
        elif muscle_group == "lower back":
            day_6_muscle_groups.remove(muscle_group)
        else:
            print(f"Error: Did not recognise muscle group '{muscle_group}' in excludedMuscleGroups array")

    # Check day_k_muscle_groups array has not decreased too much, if it has, it requires modification
    if not day_1_requires_mod and len(day_1_muscle_groups) < 0.6 * len(push):
        day_1_requires_mod = True
    if not day_2_requires_mod and len(day_2_muscle_groups) < 0.6 * len(pull):
        day_2_requires_mod = True
    if not day_3_requires_mod and len(day_3_muscle_groups) < 0.6 * len(legs_1):
        day_3_requires_mod = True
    if not day_4_requires_mod and len(day_4_muscle_groups) < 0.6 * len(chest_n_back):
        day_4_requires_mod = True
    if not day_5_requires_mod and len(day_5_muscle_groups) < 0.6 * len(sarms):
        day_5_requires_mod = True
    if not day_6_requires_mod and len(day_6_muscle_groups) < 0.6 * len(legs_2):
        day_6_requires_mod = True
    
    
    further_modifications_required = day_1_requires_mod or day_2_requires_mod or day_3_requires_mod or day_4_requires_mod or day_5_requires_mod or day_6_requires_mod

    if further_modifications_required:

        used_preferred_muscle_groups = False

        if day_1_requires_mod:
            ordered_muscle_groups = initialiseOrderedMuscleGroups(excluded_muscle_groups)

            # prioritise muscle_groups not trained in day 4 if not subject to change
            if not day_4_requires_mod:
                low_priority_muscle_groups = set(day_4_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 3 if not subject to change
            if not day_3_requires_mod:
                low_priority_muscle_groups = set(day_3_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle_groups not trained in day 5 if not subject to change
            if not day_5_requires_mod:
                low_priority_muscle_groups = set(day_5_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle_groups not trained in day 2 if not subject to change
            if not day_2_requires_mod:
                low_priority_muscle_groups = set(day_2_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            
            # prioritise muscle_groups not trained in day 6 if not subject to change
            if not day_6_requires_mod:
                low_priority_muscle_groups = set(day_6_muscle_groups) # O(1) lookups
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

            # prioritise muscle_groups not trained in day 5 if not subject to change
            if not day_5_requires_mod:
                low_priority_muscle_groups = set(day_5_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle_groups not trained in day 4 if not subject to change
            if not day_4_requires_mod:
                low_priority_muscle_groups = set(day_4_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            
            # prioritise muscle_groups not trained in day 6 if not subject to change
            if not day_6_requires_mod:
                low_priority_muscle_groups = set(day_6_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            
            # prioritise muscle_groups not trained in day 1
            low_priority_muscle_groups = set(day_1_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle_groups not trained in day 3 if not subject to change
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

            # prioritise muscle_groups not trained in day 6 if not subject to change
            if not day_6_requires_mod:
                low_priority_muscle_groups = set(day_6_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            
            # prioritise muscle_groups not trained in day 1 
            low_priority_muscle_groups = set(day_1_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            
            # prioritise muscle_groups not trained in day 5 if not subject to change
            if not day_5_requires_mod:
                low_priority_muscle_groups = set(day_5_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle_groups not trained in day 2
            low_priority_muscle_groups = set(day_2_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            
            # prioritise muscle_groups not trained in day 4 if not subject to change
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

            # prioritise muscle_groups not trained in day 1
            low_priority_muscle_groups = set(day_1_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 2
            low_priority_muscle_groups = set(day_2_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            
            # prioritise muscle groups not trained in day 6 if not subject to change
            if not day_6_requires_mod:
                low_priority_muscle_groups = set(day_6_muscle_groups) # O(1) lookups
                prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
                ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)
            

            # prioritise muscle groups not trained in day 3
            low_priority_muscle_groups = set(day_3_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 5 if not subject to change
            if not day_5_requires_mod:
                low_priority_muscle_groups = set(day_5_muscle_groups) # O(1) lookups
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

        if day_5_requires_mod:
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

            # prioritise muscle groups not trained in day 4
            low_priority_muscle_groups = set(day_4_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 6
            if not day_6_requires_mod:
                low_priority_muscle_groups = set(day_6_muscle_groups) # O(1) lookups
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
            day_5_muscle_groups = ordered_muscle_groups[:no_of_muscle_groups_to_train]

        if day_6_requires_mod:
            ordered_muscle_groups = initialiseOrderedMuscleGroups(excluded_muscle_groups)

            # prioritise muscle groups not trained in day 3
            low_priority_muscle_groups = set(day_3_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 2
            low_priority_muscle_groups = set(day_2_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 4
            low_priority_muscle_groups = set(day_4_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 1
            low_priority_muscle_groups = set(day_1_muscle_groups) # O(1) lookups
            prioritised_muscle_groups = [x for x in ordered_muscle_groups if x not in low_priority_muscle_groups]
            ordered_muscle_groups = orderMuscleGroups(ordered_muscle_groups, [], prioritised_muscle_groups)

            # prioritise muscle groups not trained in day 5
            low_priority_muscle_groups = set(day_5_muscle_groups) # O(1) lookups
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
            day_6_muscle_groups = ordered_muscle_groups[:no_of_muscle_groups_to_train]
    else:
        # logic for prioritising preferred muscle groups for unmodified PUSH/PULL/LEGS x Arnold
        '''
        push = ["chest", "triceps", "front delt", "lateral delt", "chest", "triceps", "chest", "triceps", "front delt", "traps"]
        pull = ["middle back", "biceps", "lats", "rear delt", "biceps", "forearms", "middle back", "traps", "biceps", "lats"]
        legs_1 = ["quadriceps", "quadriceps", "calves", "abdominals", "quadriceps", "adductors", "hamstrings", "abdominals", "calves", "front delt", "hamstrings", "glutes"]
        chest_n_back = ["chest", "lats", "chest", "middle back", "chest", "lats", "rear delt", "traps", "chest", "middle back", "lateral delt"]
        sarms = ["triceps", "biceps", "lateral delt", "front delt", "triceps", "biceps", "forearms", "front delt", "triceps", "biceps", "forearms"]
        legs_2 = ["hamstrings", "hamstrings", "abdominals", "calves", "quadriceps", "abductors", "lower back", "quadriceps", "calves", "abdominals", "hamstrings", "glutes"]
        '''
        # reverse preferred muscle groups so most important is last in list and thus gets greatest priority
        preferred_muscle_groups.reverse()
        for muscle_group in preferred_muscle_groups:
            if muscle_group == "chest":
                day_1_muscle_groups.insert(0, muscle_group)
                day_4_muscle_groups.remove(muscle_group) # first occurence
                day_4_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "triceps":
                day_1_muscle_groups = removeLastOccurrence(day_1_muscle_groups, muscle_group)
                day_1_muscle_groups.insert(0, muscle_group)
                day_5_muscle_groups.remove(muscle_group) # first occurence
                day_5_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "front delt":
                day_1_muscle_groups = removeLastOccurrence(day_1_muscle_groups, muscle_group)
                day_1_muscle_groups.insert(0, muscle_group)
                day_5_muscle_groups = removeLastOccurrence(day_5_muscle_groups, muscle_group)
                day_5_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "lateral delt":
                day_1_muscle_groups = removeLastOccurrence(day_1_muscle_groups, muscle_group)
                day_1_muscle_groups.insert(0, muscle_group)
                day_4_muscle_groups = removeLastOccurrence(day_4_muscle_groups, muscle_group)
                day_4_muscle_groups.insert(0, muscle_group)
                day_5_muscle_groups = removeLastOccurrence(day_5_muscle_groups, muscle_group)
                day_5_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "middle back" or muscle_group == "lats":
                day_2_muscle_groups.remove(muscle_group) # first occurence
                day_2_muscle_groups.insert(0, muscle_group)
                day_4_muscle_groups = removeLastOccurrence(day_4_muscle_groups, muscle_group)
                day_4_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "biceps":
                day_2_muscle_groups = removeLastOccurrence(day_2_muscle_groups, muscle_group)
                day_2_muscle_groups.insert(0, muscle_group)
                day_5_muscle_groups = removeLastOccurrence(day_5_muscle_groups, muscle_group)
                day_5_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "rear delt":
                day_2_muscle_groups = removeLastOccurrence(day_2_muscle_groups, muscle_group)
                day_2_muscle_groups.insert(0, muscle_group)
                day_4_muscle_groups = removeLastOccurrence(day_4_muscle_groups, muscle_group)
                day_4_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "traps":
                day_2_muscle_groups.insert(0, muscle_group)
                day_4_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "forearms":
                day_2_muscle_groups = removeLastOccurrence(day_2_muscle_groups, muscle_group)
                day_2_muscle_groups.insert(0, muscle_group)
                day_5_muscle_groups = removeLastOccurrence(day_5_muscle_groups, muscle_group)
                day_5_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "lower back":
                day_2_muscle_groups.insert(0, muscle_group)
                day_6_muscle_groups = removeLastOccurrence(day_6_muscle_groups, muscle_group)
                day_6_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "quadriceps":
                day_3_muscle_groups = removeLastOccurrence(day_3_muscle_groups, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
                day_6_muscle_groups.remove(muscle_group) # first occurence
                day_6_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "calves" or muscle_group == "abdominals":
                day_3_muscle_groups = removeLastOccurrence(day_3_muscle_groups, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
                day_6_muscle_groups = removeLastOccurrence(day_6_muscle_groups, muscle_group)
                day_6_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "hamstrings":
                day_3_muscle_groups.remove(muscle_group) # first occurence
                day_3_muscle_groups.insert(0, muscle_group)
                day_6_muscle_groups = removeLastOccurrence(day_6_muscle_groups, muscle_group)
                day_6_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "adductors":
                day_3_muscle_groups = removeLastOccurrence(day_3_muscle_groups, muscle_group)
                day_3_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "abductors":
                day_6_muscle_groups = removeLastOccurrence(day_6_muscle_groups, muscle_group)
                day_6_muscle_groups.insert(0, muscle_group)
            elif muscle_group == "glutes":
                day_6_muscle_groups = [muscle_group, muscle_group] + day_6_muscle_groups
                day_3_muscle_groups = [muscle_group, muscle_group] + day_3_muscle_groups
            else:
                print(f"Error: did not recognise muscle group {muscle_group}")

    day_1_sets = map(lambda muscle: sets_per_muscle[muscle], day_1_muscle_groups)
    day_2_sets = map(lambda muscle: sets_per_muscle[muscle], day_2_muscle_groups)
    day_3_sets = map(lambda muscle: sets_per_muscle[muscle], day_3_muscle_groups)
    day_4_sets = map(lambda muscle: sets_per_muscle[muscle], day_4_muscle_groups)
    day_5_sets = map(lambda muscle: sets_per_muscle[muscle], day_5_muscle_groups)
    day_6_sets = map(lambda muscle: sets_per_muscle[muscle], day_6_muscle_groups)

    day_1 = list(zip(day_1_muscle_groups, day_1_sets))
    day_2 = list(zip(day_2_muscle_groups, day_2_sets))
    day_3 = list(zip(day_3_muscle_groups, day_3_sets))
    day_4 = list(zip(day_4_muscle_groups, day_4_sets))
    day_5 = list(zip(day_5_muscle_groups, day_5_sets))
    day_6 = list(zip(day_6_muscle_groups, day_6_sets))
    return [(day_1, day_1_requires_mod), (day_2, day_2_requires_mod), (day_3, day_3_requires_mod), 
            (day_4, day_4_requires_mod), (day_5, day_5_requires_mod), (day_6, day_6_requires_mod)]