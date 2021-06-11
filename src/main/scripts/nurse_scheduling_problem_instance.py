from pathlib import Path

import pulp
from pulp import (LpMinimize, LpProblem, LpStatus, lpSum, LpVariable)

from nurse_scheduling.display import csv_to_html
from nurse_scheduling.utils import deepflatten
from nurse_scheduling.visualization import (lp_output_to_dict, output_dict_to_weekly)
from nurse_scheduling.conf_smaller import (
    all,
    docs,
    floor_needs,
    long_day_costs,
    num_days,
    num_floors,
    num_nurses,
    num_shifts,
    nurses_names,
    var_name_tplt
)

# Define problem
prob = LpProblem("simpleScheduleProblem", LpMinimize)


# Define variables
# Checks
all_vars = []
for n_name in nurses_names:
    nurse_vars = []
    for d_idx in range(num_days):
        day = []
        for s_idx in range(num_shifts):
            shift = []
            for f_idx in range(num_floors):
                my_var = var_name_tplt % (n_name, d_idx, s_idx, f_idx)
                shift.append(my_var)
                all_vars.append(my_var)
            day.append(shift)
        nurse_vars.append(day)
    all[n_name]["var"] = nurse_vars

assert len(all_vars) == num_nurses * num_days * num_floors * num_shifts
nurses = list(all.keys())
assert len(nurses) == num_nurses
assert len(all[nurses[0]]["var"]) == num_days == len(all[nurses[0]]["cost"])
assert len(all[nurses[0]]["var"][0]) == num_shifts == len(all[nurses[0]]["cost"][0])
assert len(all[nurses[0]]["var"][0][0]) == num_floors == len(all[nurses[0]]["cost"][0][0])

vars = LpVariable.dicts("var", all_vars, lowBound=0, upBound=1, cat='Integer')
consts = []
continuity_vars = []

# Define Constraints

# Enough staffing per floor

for d_idx in range(num_days):
    for s_idx in range(num_shifts):
        for f_idx in range(num_floors - 1):
            floor_x_y = lpSum([vars[all[k]["var"][d_idx][s_idx][f_idx]] for k in all.keys()]) == floor_needs[f_idx][s_idx]
            consts.append(floor_x_y)
        # Last floor is Admin
        floor_x_y = lpSum([vars[all[k]["var"][d_idx][s_idx][num_floors - 1]] for k in all.keys()]) >= 0
        consts.append(floor_x_y)

# Personal
n_idx = 0
for nurse in all.keys():
    # Max Week  - half the total shifts # 36 hrs/week max w. 2 shifts of 6 hrs/day available
    week_max = lpSum([vars[x] for x in deepflatten(all[nurse]['var'])]) <= float(num_days * 10.0)  # float(num_days * num_shifts) * (1/2)
    consts.append(week_max)

    # Min Week
    week_max = lpSum([vars[x] for x in deepflatten(all[nurse]['var'])]) >= float(num_days * 6.5)  # float(num_days * num_shifts) * (1/2)
    consts.append(week_max)

    for d_idx in range(num_days):
        # Max Day - (could be used to strictly avoid 8am-8pm days)
        day_max = lpSum([vars[y] for x in all[nurse]['var'][d_idx] for y in x]) <= num_shifts * num_floors  # effectively useless
        consts.append(day_max)

        # Min Day
        day_min = lpSum([vars[y] for x in all[nurse]['var'][d_idx] for y in x]) >= float(6.0)
        consts.append(day_min)

        # Avoid long days
        for long_day_i in range(6):
            # 820Var (Bounded Int) >= (var_i_j_0_X + var_i_j_11_X) / 2.0 -> Weight 50
            # 819Var (Bounded Int) >= (var_i_j_0_X + var_i_j_10_X) / 2.0 -> Weight 40
            # 818Var (Bounded Int) >= (var_i_j_0_X + var_i_j_9_X) / 2.0 -> Weight 12
            # 817Var (Bounded Int) >= (var_i_j_0_X + var_i_j_8_X) / 2.0 -> Weight 10

            # 920Var  (Bounded Int) >= (var_i_j_0_X + var_i_j_11_X) / 2.0 -> Weight 20
            # 1020Var (Bounded Int) >= (var_i_j_1_X + var_i_j_11_X) / 2.0 -> Weight 15
            # 1120Var (Bounded Int) >= (var_i_j_2_X + var_i_j_11_X) / 2.0 -> Weight 12
            # 1220Var (Bounded Int) >= (var_i_j_3_X + var_i_j_11_X) / 2.0 -> Weight 10

            longmorning_var = LpVariable(f'dayLongMorning_{nurse}_{d_idx}_{long_day_i}', lowBound=0, upBound=1, cat='Integer')
            longmorning_const = longmorning_var >= (lpSum(
                [vars[x] for x in all[nurse]['var'][d_idx][0]] + [vars[x] for x in all[nurse]['var'][d_idx][num_shifts-1-long_day_i]]
            ) / 2) - 0.5
            consts.append(longmorning_const)
            continuity_vars.append(long_day_costs[long_day_i] * longmorning_const)

            longafternoon_var = LpVariable(f'dayLongAft_{nurse}_{d_idx}_{long_day_i}', lowBound=0, upBound=1, cat='Integer')
            longafternoon_const = longafternoon_var >= (lpSum(
                [vars[x] for x in all[nurse]['var'][d_idx][long_day_i]] + [vars[x] for x in all[nurse]['var'][d_idx][num_shifts - 1]]
            ) / 2) - 0.5
            consts.append(longafternoon_const)
            continuity_vars.append(long_day_costs[long_day_i] * longafternoon_const)

        # Per Shift
        for s_idx in range(num_shifts):
            # Can't be in more than 1 place
            unicity = lpSum([vars[x] for x in all[nurse]['var'][d_idx][s_idx]]) <= 1.0
            consts.append(unicity)

            # # Incompatibilities
            for doc in docs.keys():
                if docs[doc]['compat'][n_idx] == 0:  # if incompat
                    nurse_doc_constraint_expr = []
                    for f_idx in range(num_floors):  # iterate schedule (floor)
                        if docs[doc]['sched'][d_idx][s_idx][f_idx] == 1:  # check presence
                            nurse_doc_constraint_expr.append(vars[all[nurse]['var'][d_idx][s_idx][f_idx]])
                    if len(nurse_doc_constraint_expr) > 0:  # check for constraints
                        nurse_doc_constraint = lpSum(list(set(nurse_doc_constraint_expr))) <= 0
                        consts.append(nurse_doc_constraint)

    n_idx += 1  # Note: this works because all.keys() keeps the order that it was defined in...

# Define obj function
shedule_vars = [
        vars[v] * w for k in all.keys() for v, w in zip(
            [x for x in list(deepflatten(all[k]['var']))],
            [y for y in list(deepflatten(all[k]['cost']))],
        )
    ]
cost_func = lpSum(shedule_vars + continuity_vars)
prob += cost_func

# Add all constraints:
for c in consts:
    prob += c


# Solve
# prob.solve(pulp.PULP_CBC_CMD(maxSeconds=20, msg=True, fracGap=0))
prob.solve()
print(f"Status: [{LpStatus[prob.status]}]")
print()

if prob.status != -1:
    # Show solution
    # for v in prob.variables():
    #     if v.varValue > 0:
    #         print(v.name, "=", v.varValue)

    # Process into readable format
    output_dict = lp_output_to_dict(prob)
    out_df = output_dict_to_weekly(output_dict)
    for i in range(len(out_df)):
        print(out_df[i])
        print()
        out_df[i].to_csv(f'schedule_[{i}].csv', index=False)
        # break

s_path = Path('schedule_[0].csv')
t_path = Path('test.html')
csv_to_html(s_path, t_path)
