from .get_training_split_utils import orderMuscleGroups

# pre: excluded_muscle_groups, preferred_muscle_groups are both arrays with valid muscle group values 
#      and excluded_muscle_groups and preferred_muscle_groups share no common values
def get_1_day_training_split(excluded_muscle_groups, preferred_muscle_groups):
    # FULL BODY x1
    muscle_groups = ["chest", "middle back", "front delt", "quadriceps", "biceps", "triceps", "hamstrings", "lateral delt", 
            "abdominals", "rear delt", "lats", "calves", "forearms"]

    # remove excluded muscle groups and prioritise user-preferred muscle groups
    ordered_muscle_groups = orderMuscleGroups(muscle_groups, excluded_muscle_groups, preferred_muscle_groups)

    sets = [2 for _ in range(len(ordered_muscle_groups))]

    ordered_muscle_groups_and_sets = list(zip(ordered_muscle_groups, sets))

    return [(ordered_muscle_groups_and_sets, False)]