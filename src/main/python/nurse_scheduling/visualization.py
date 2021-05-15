from typing import (Dict, List, Tuple)

import pandas as pd
from pulp import LpProblem

from nurse_scheduling.conf import (
    all,
    shift_map,
    shift_map_inv,
    num_days,
    num_shifts,
    nurse_names_map,
    shift_names
)


def parse_var_name(var_name: str) -> Tuple[str, int, int, int]:
    """Parses "_"-combined-var into individual elements"""
    vars = var_name.split('_')
    return vars[1], int(vars[2]), int(vars[3]), int(vars[4])


def _make_empty_schedule(all_data: dict):
    sched = {}

    for x in all_data.keys():
        sched[x] = {"sched": [[0] * num_shifts] * num_days}

    return sched


def lp_output_to_dict(prob: LpProblem) -> Dict:
    sched = _make_empty_schedule(all)

    for v in prob.variables():
        nurse, day, shift, floor = parse_var_name(v.name)
        # print(f'nurse [{nurse}], day [{day}], floor [{floor}], shift [{shift}]')
        value = v.varValue
        # print(f'value [{value}]')

        if value > 0:
            sched[nurse]['sched'][day][int(shift)] = shift_map_inv[floor]

    # print(sched)
    return sched


def output_dict_to_weekly(schedule: Dict) -> List[pd.DataFrame]:
    week_schedules = [{}] * num_days  # len() = num worked days

    for nurse in schedule.keys():
        for d_i in range(num_days):
            week_schedules[d_i][nurse] = schedule[nurse]['sched'][d_i]

    return [pd.DataFrame(x).rename(index=shift_names, columns=nurse_names_map) for x in week_schedules]
