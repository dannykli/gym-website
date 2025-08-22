from .get_training_split_utils import orderMuscleGroups

# pre: excluded_muscle_groups, preferred_muscle_groups are both arrays with valid muscle group values 
#      and excluded_muscle_groups and preferred_muscle_groups share no common values
def get_2_day_training_split(excluded_muscle_groups, preferred_muscle_groups, time_per_session, time_per_set):
    # FULL BODY x2
    # muscle groups ordered by priority
    muscle_groups = ["chest", "middle back", "front delt", "quadriceps", "biceps", "triceps", "hamstrings", "lateral delt", 
        "abdominals", "rear delt", "lats", "calves", "forearms"]
    
    # excluded "traps", "adductors", "lower back", "abductors", "glutes"

    ordered_muscle_groups = orderMuscleGroups(muscle_groups, excluded_muscle_groups, preferred_muscle_groups)

    # sets = map(lambda muscle: sets_per_muscle[muscle], ordered_muscle_groups)
    sets = [2 for _ in range(len(ordered_muscle_groups))]

    ordered_muscle_groups_and_sets = list(zip(ordered_muscle_groups, sets))

    # find number of muscle groups to be trained on day 1
    time = 0
    no_of_muscle_groups = 0
    for muscle_group, no_of_sets in ordered_muscle_groups_and_sets:
        # check if there is time to train another muscle group
        if time > time_per_session: 
            break
        time += time_per_set[muscle_group] * no_of_sets
        no_of_muscle_groups += 1

    day_1 = ordered_muscle_groups_and_sets[:no_of_muscle_groups]
    # day 2 is all of the muscle groups not trained on first day followed by highest property muscle groups already trained on day 1
    day_2 = ordered_muscle_groups_and_sets[no_of_muscle_groups:] + day_1

    return [day_1, day_2]
