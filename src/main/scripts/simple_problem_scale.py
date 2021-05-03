from pulp import (LpMinimize, LpProblem, LpStatus, lpSum, LpVariable)


## Define problem
prob = LpProblem("simpleScheduleProblem", LpMinimize)

## Define variables
num_nurses = 3
num_floors = 2
num_shifts = 2

floor_needs_per_shift = [[2, 1], [2, 1]]

# Schema: [person]_[floor]_[shift]
all = {
    "a": {
        "var": [['a_a_1', 'a_b_1'], ['a_a_2', 'a_b_2']],
        "cost": [[1, 1], [1, 1]],
    },
    "b": {
        "var": [['b_a_1', 'b_b_1'], ['b_a_2', 'b_b_2']],
        "cost": [[2, 1], [2, 1]],
    },
    "c": {
        "var": [['c_a_1', 'c_b_1'], ['c_a_2', 'c_b_2']],
        "cost": [[1, 1], [2, 2]],
    }
}


# Checks
all_vars = []
for x in all.keys():
    cur_vars = all[x]['var']
    assert len(cur_vars) == num_shifts
    assert len(cur_vars[0]) == num_floors
    curr_vars_flat = [y for x in cur_vars for y in x]
    assert len(curr_vars_flat) == num_floors * num_shifts
    all_vars.extend(curr_vars_flat)

assert len(all_vars) == num_nurses * num_floors * num_floors

vars = LpVariable.dicts("var", all_vars, lowBound=0, upBound=1, cat='Integer')


## Define obj function
cost_func = lpSum(
    [
        vars[v] * w for k in all.keys() for v, w in zip(
            [y for x in all[k]["var"] for y in x],
            [y for x in all[k]["cost"] for y in x]
        )
    ]
)
prob += cost_func

## Define Constraints

# Enough staffing per floor
for i, s_needs in enumerate(floor_needs_per_shift):
    for j, f_needs in enumerate(s_needs):
        floor_x_y = lpSum([vars[all[k]["var"][i][j]] for k in all.keys()]) >= f_needs
        prob += floor_x_y

# Personal
for person in all.keys():
    # Max Day
    day_max = lpSum([vars[y] for x in all[person]['var'] for y in x]) <= 2.0
    prob += day_max

    # Can't be in more than 1 place
    for s_i in range(num_shifts):
        unicity = lpSum([vars[x] for x in all[person]['var'][s_i]]) <= 1.0
        prob += unicity


# Incompatibilities
#todo

# Solve
prob.solve()
print(f"Status: [{LpStatus[prob.status]}]")

# Show solution
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
