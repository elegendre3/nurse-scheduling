from typing import (Dict, List, Tuple)

import pandas as pd
from pulp import LpProblem

from nurse_scheduling.conf_smaller import (
    all,
    floor_map_inv,
    num_days,
    num_shifts,
    nurse_names_map,
    shift_names
)


def parse_var_name(var_name: str) -> Tuple[str, int, int, int]:
    """Parses "_"-combined-var into individual elements"""
    # print(f"raw var name: [{var_name}]")
    vars = var_name.split('_')
    if "ceil" in vars[0].lower() or "floor" in vars[0].lower() or "empty" in vars[0].lower():
        raise ValueError("Not a Schedule Variable")
    else:
        return vars[1], int(vars[2]), int(vars[3]), int(vars[4])


def _make_empty_schedule(all_data: dict):
    sched = {}

    for x in all_data.keys():
        sched[x] = {}
        sched[x]["sched"] = {d_i: [0] * num_shifts for d_i in range(num_days)}

    return sched


def lp_output_to_dict(prob: LpProblem) -> Dict:
    sched = _make_empty_schedule(all)

    for v in prob.variables():
        try:
            nurse, day, shift, floor = parse_var_name(v.name)
        except ValueError:
            continue
        # print(f'nurse [{nurse}], day [{day}], floor [{floor}], shift [{shift}]')
        value = v.varValue
        # print(f'value [{value}]')

        if value > 0:
            sched[nurse]['sched'][day][int(shift)] = floor_map_inv[floor]
    # print(sched)
    return sched


def output_dict_to_weekly(schedule: Dict) -> List[pd.DataFrame]:
    week_schedules = []

    for d_i in range(num_days):
        d_sched = {}
        for nurse in schedule.keys():
            d_sched[nurse] = schedule[nurse]['sched'][d_i]
        week_schedules.append(d_sched)

    return [pd.DataFrame(x).rename(index=shift_names, columns=nurse_names_map) for x in week_schedules]
