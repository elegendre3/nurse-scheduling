num_nurses = 6
num_floors = 2
num_days = 5
num_shifts = 10

floor_needs = {"a": 2, "b": 1}

nurses_names = ["a", "b", "c", "d", "e", "f"]

# Schema: [person]_[floor]_[day]_[shift]
var_name_tplt = "%s_%i_%i_%i"

# Define variables
# Checks
all = {}
all_vars = []
for n_name in nurses_names:
    nurse_vars = []
    day = []
    for d_idx in range(num_days):
        shift = []
        for s_idx in range(num_shifts):
            floor = []
            for f_idx in range(num_floors):
                my_var = var_name_tplt % (n_name, f_idx, d_idx, s_idx)
                floor.append(my_var)
                all_vars.append(my_var)
            shift.append(floor)
        day.append(shift)
    nurse_vars.append(day)
    all[f"{n_name}"] = nurse_vars

assert len(all_vars) == num_nurses * num_days * num_floors * num_shifts
