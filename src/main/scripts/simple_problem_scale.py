from pulp import (LpMinimize, LpProblem, LpStatus, lpSum, LpVariable)


## Define problem
prob = LpProblem("simpleScheduleProblem", LpMinimize)

## Define variables
num_nurses = 3
num_floors = 2
num_shifts = 2

floor_shift_needs = [2, 2, 1, 1]

# Schema: [person]_[floor]_[shift]
all = {
    "a": {
        "var": ['a_a_1', 'a_a_2', 'a_b_1', 'a_b_2'],
        "cost": [1, 1, 1, 1],
    },
    "b": {
        "var": ['b_a_1', 'b_a_2', 'b_b_1', 'b_b_2'],
        "cost": [2, 2, 1, 1],
    },
    "c": {
        "var": ['c_a_1', 'c_a_2', 'c_b_1', 'c_b_2'],
        "cost": [1, 2, 1, 2],
    }
}


# Checks
all_vars = []
for x in all.keys():
    cur_vars = all[x]['var']
    assert len(cur_vars) == num_floors * num_shifts
    all_vars.extend(cur_vars)

assert len(all_vars) == num_nurses * num_floors * num_floors

vars = LpVariable.dicts("var", all_vars, lowBound=0, upBound=1, cat='Integer')


## Define obj function
cost_func = lpSum([vars[v] * w for k in all.keys() for v, w in zip(all[k]["var"], all[k]["cost"])])
prob += cost_func

## Define Constraints

# TODO Use vars[xx]

# Enough staffing per floor
for floor_shift_comb in range(num_floors * num_shifts):
    floor_x_y = lpSum([vars[all[k]["var"][floor_shift_comb]] for k in all.keys()]) >= floor_shift_needs[floor_shift_comb]
    prob += floor_x_y

# Personal
for person in all.keys():
    # Max Day
    day_max_k = lpSum([vars[x] for x in all[person]['var']]) <= 2.0
    prob += day_max_k

    # Can't be in more than 1 place
    unicity_1 = lpSum([vars[all[person]['var'][0]], vars[all[person]['var'][2]]]) <= 2.0
    unicity_2 = lpSum([vars[all[person]['var'][1]], vars[all[person]['var'][3]]]) <= 2.0
    prob += unicity_1
    prob += unicity_2


# Incompatibilities
#todo

# Solve
prob.solve()
print(f"Status: [{LpStatus[prob.status]}]")

# Show solution
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
