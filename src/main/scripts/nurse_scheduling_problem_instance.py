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
    week_max = lpSum([vars[x] for x in deepflatten(all[nurse]['var'])]) <= float(num_days * 12.0)  # float(num_days * num_shifts) * (1/2)
    consts.append(week_max)

    # Avoid full days as much as possible
    # todo

    for d_idx in range(num_days):
        # Max Day - (could be used to strictly avoid 8am-8pm days)
        day_max = lpSum([vars[y] for x in all[nurse]['var'][d_idx] for y in x]) <= num_shifts * num_floors  # effectively useless
        consts.append(day_max)

        # Min Day
        day_min = lpSum([vars[y] for x in all[nurse]['var'][d_idx] for y in x]) >= float(6.0)
        consts.append(day_min)

        # Prefer balanced week over few big days
        day = deepflatten(all[nurse]['var'][d_idx])
        day_sum = lpSum([vars[x] for x in day])
        day_ceil_var = LpVariable(
            f'nonEmptyDay_{nurse}_{d_idx}',
            lowBound=0,
            upBound=1,
            cat='Integer'
        )
        day_ceil_const = day_ceil_var <= 0.9 + (day_sum / 2)  # day_sum = 0 -> 0 | day_sum > 0 -> = 1
        consts.append(day_ceil_const)
        continuity_vars.append(10 * (1 - day_ceil_var))  # expensive to have empty days

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

    # Continuity | avoid 8-9 + 11-12 + 14-18
    # foreach nurse, day, floor:
    # foreach shift except 0 and -1:
    # var >= floor((ceil(sum(vars_before)/num_shifts) + ceil(sum(vars_after)/num_shifts))/2)
    # vars before shift s => same nurse, day, floor, but [0:s]
    # vars after  shift s => same nurse, day, floor, but [s+1:]
            if s_idx in [0, num_shifts - 1]:
                # Skipping first and last
                pass
            else:
                # Looking at previous shifts
                before_name = f'BeforeCeil_{nurse}_{d_idx}_{s_idx}'
                before = deepflatten([all[nurse]['var'][d_idx][s] for s in range(s_idx)])
                before_sum = lpSum([vars[x] for x in before])
                before_ceil_var = LpVariable(
                    before_name,
                    lowBound=0,
                    upBound=1,
                    cat='Integer'
                )
                before_ceil_const = before_ceil_var >= before_sum / (num_floors * num_shifts)
                consts.append(before_ceil_const)

                # Looking at next shifts
                after_name = f'AfterCeil_{nurse}_{d_idx}_{s_idx}'
                after = deepflatten([all[nurse]['var'][d_idx][s] for s in range(s_idx + 1, num_shifts)])
                after_sum = lpSum([vars[x] for x in after])
                after_ceil_var = LpVariable(
                    after_name,
                    lowBound=0,
                    upBound=1,
                    cat='Integer'
                )
                after_ceil_const = after_ceil_var >= after_sum / (num_floors * num_shifts)
                consts.append(after_ceil_const)

                # Enforcing continuity  - BY OBJECTIVE
                sum_mathfloor_var = LpVariable(
                    f'SumFloor_{nurse}_{d_idx}_{s_idx}',
                    lowBound=0,
                    upBound=1,
                    cat='Integer'
                )
                sum_mathfloor_const = sum_mathfloor_var >= (before_ceil_var + after_ceil_var) / 2.0
                consts.append(sum_mathfloor_const)
                continuity_vars.append(sum_mathfloor_var)  # will not make it 1 unless has to  | soft constraint

                cont_const = lpSum(vars[all[nurse]['var'][d_idx][s_idx][f_idx]] for f_idx in range(num_floors)) >= sum_mathfloor_var
                consts.append(cont_const)

                # Something makes PAM! do ADMIN at the end of the 2nd day.. it shouldnt

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
prob.solve(pulp.PULP_CBC_CMD(maxSeconds=20, msg=True, fracGap=0))
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
