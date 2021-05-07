from typing import (Dict, List, Tuple)

import pandas as pd
from pulp import LpProblem


def parse_var_name(var_name: str) -> Tuple[str, str, str]:
    """Parses "_"-combined-var into individual elements"""
    vars = var_name.split('_')
    return vars[1], vars[2], vars[3]


def lp_output_to_dict(prob: LpProblem) -> Dict:
    all = {
        "a": {
            "sched": [0, 0],  # len(sched) == num_shifts
        },
        "b": {
            "sched": [0, 0],
        },
        "c": {
            "sched": [0, 0],
        },
        "d": {
            "sched": [0, 0],
        }
    }

    for v in prob.variables():
        nurse, floor, shift = parse_var_name(v.name)
        print(f'nurse [{nurse}], floor [{floor}], shift [{shift}]')
        value = v.varValue
        print(f'value [{value}]')

        if value > 0:
            all[nurse]['sched'][int(shift) - 1] = floor

    print(all)
    return all


def output_dict_to_weekly(all: Dict) -> List[pd.DataFrame]:
    week_schedules = [{}]  # len() = num worked days

    for nurse in all.keys():
        for day_idx in range(len(week_schedules)):
            week_schedules[day_idx][nurse] = all[nurse]['sched']

    return [pd.DataFrame(x) for x in week_schedules]
