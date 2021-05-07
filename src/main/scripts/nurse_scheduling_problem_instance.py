from pulp import (LpMinimize, LpProblem, LpStatus, lpSum, LpVariable)

from nurse_scheduling.visualization import (lp_output_to_dict, output_dict_to_weekly)
from nurse_scheduling.utils import deepflatten
from nurse_scheduling.conf import (
    all,
    docs,
    floor_needs_per_shift,
    num_days,
    num_floors,
    num_nurses,
    num_shifts
)

# Define problem
prob = LpProblem("simpleScheduleProblem", LpMinimize)


# Define variables
# Checks
all_vars = []
for x in all.keys():
    cur_vars = all[x]['var']
    assert len(cur_vars) == num_days
    assert len(cur_vars[0]) == num_shifts
    assert len(cur_vars[0][0]) == num_floors
    for d_idx in range(num_days):
        day_flat = [y for x in cur_vars[d_idx] for y in x]
        assert len(day_flat) == num_floors * num_shifts
        all_vars.extend(day_flat)

assert len(all_vars) == num_nurses * num_days * num_floors * num_floors

vars = LpVariable.dicts("var", all_vars, lowBound=0, upBound=1, cat='Integer')


## Define obj function
cost_func = lpSum(
    [
        vars[v] * w for k in all.keys() for v, w in zip(
            [x for x in list(deepflatten(all[k]['var']))],
            [y for y in list(deepflatten(all[k]['cost']))],
        )
    ]
)
prob += cost_func

## Define Constraints

# Enough staffing per floor

for h, d_needs in enumerate(floor_needs_per_shift):
    for i, s_needs in enumerate(d_needs):
        for j, f_needs in enumerate(s_needs):
            floor_x_y = lpSum([vars[all[k]["var"][h][i][j]] for k in all.keys()]) >= f_needs
            prob += floor_x_y

# Personal
n_idx = 0
for nurse in all.keys():
    # Max Week  - half the total shifts # 36 hrs/week max w. 2 shifts of 6 hrs/day available
    week_max = lpSum([vars[x] for x in deepflatten(all[nurse]['var'])]) <= float(num_days * num_shifts) * (1/2)
    prob += week_max

    # Avoid 2-shift days as much as possible
    # todo

    # Max Day - set to 2 now which is current max (could be used to strictly avoid 8am-8pm days)
    for d_i in range(num_days):
        day_max = lpSum([vars[y] for x in all[nurse]['var'][d_i] for y in x]) <= 2.0
        prob += day_max

        # Can't be in more than 1 place
        for s_i in range(num_shifts):
            unicity = lpSum([vars[x] for x in all[nurse]['var'][d_i][s_i]]) <= 1.0
            prob += unicity

            # Incompatibilities
            for doc in docs.keys():
                if docs[doc]['compat'][n_idx] == 0:  # if incompat
                    nurse_doc_constraint_expr = []
                    for f_idx in range(num_floors):  # iterate schedule (floor)
                        if docs[doc]['sched'][d_i][s_i][f_idx] == 1:  # check presence
                            nurse_doc_constraint_expr.append(vars[all[nurse]['var'][d_i][s_i][f_idx]])
                    if len(nurse_doc_constraint_expr) > 0:  # check for constraints
                        nurse_doc_constraint = lpSum(list(set(nurse_doc_constraint_expr))) <= 0
                        prob += nurse_doc_constraint

    n_idx += 1  # Note: this works because all.keys() keeps the order that it was defined in...


# Solve
prob.solve()
print(f"Status: [{LpStatus[prob.status]}]")
print()

if prob.status != -1:
    # Show solution
    for v in prob.variables():
        if v.varValue > 0:
            print(v.name, "=", v.varValue)

    # Process into readable format
    out_df = output_dict_to_weekly(lp_output_to_dict(prob))
    for i in range(len(out_df)):
        print(out_df[i])
        print()
        out_df[i].to_csv(f'schedule_[{i}].csv', index=False)
