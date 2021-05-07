
num_nurses = 6
num_floors = 2
num_days = 2
num_shifts = 2

floor_needs_per_shift = [[[2, 1], [2, 1]], [[2, 1], [2, 1]]]

# Schema: [person]_[floor]_[day]_[shift]
all = {
    "a": {
        "var": [[['a_a_1_1', 'a_b_1_1'], ['a_a_1_2', 'a_b_1_2']], [['a_a_2_1', 'a_b_2_1'], ['a_a_2_2', 'a_b_2_2']]],
        "cost": [[[1, 1], [1, 1]], [[1, 1], [1, 1]]],
    },
    "b": {
        "var": [[['b_a_1_1', 'b_b_1_1'], ['b_a_1_2', 'b_b_1_2']], [['b_a_2_1', 'b_b_2_1'], ['b_a_2_2', 'b_b_2_2']]],
        "cost": [[[2, 1], [2, 1]], [[2, 1], [2, 1]]],  # expensive to be put on floor a
    },
    "c": {
        "var": [[['c_a_1_1', 'c_b_1_1'], ['c_a_1_2', 'c_b_1_2']], [['c_a_2_1', 'c_b_2_1'], ['c_a_2_2', 'c_b_2_2']]],
        "cost": [[[3, 3], [1, 1]], [[3, 3], [1, 1]]],  # expensive to work shift 1 (~mornings)
    },
    "d": {
        "var": [[['d_a_1_1', 'd_b_1_1'], ['d_a_1_2', 'd_b_1_2']], [['d_a_2_1', 'd_b_2_1'], ['d_a_2_2', 'd_b_2_2']]],
        "cost": [[[1, 1], [5, 5]], [[1, 1], [5, 5]]],  # expensive to work shift 2 (~afternoons)
    },
    "e": {
        "var": [[['e_a_1_1', 'e_b_1_1'], ['e_a_1_2', 'e_b_1_2']], [['e_a_2_1', 'd_b_2_1'], ['e_a_2_2', 'e_b_2_2']]],
        "cost": [[[1, 1], [1, 1]], [[1, 1], [1, 1]]],
    },
    "f": {
        "var": [[['f_a_1_1', 'f_b_1_1'], ['f_a_1_2', 'f_b_1_2']], [['f_a_2_1', 'f_b_2_1'], ['f_a_2_2', 'f_b_2_2']]],
        "cost": [[[1, 1], [1, 1]], [[1, 1], [1, 1]]],
    }
}

docs = {
    "doc_1": {
        "sched": [[[1, 0], [1, 0]], [[1, 0], [1, 0]]],  # floor a
        "compat": [1, 1, 1, 0, 1, 1],  # incompatibility with nurse #4
    },
    "doc_2": {
        "sched": [[[1, 0], [1, 0]], [[0, 0], [0, 0]]],  # floor a - not there day 2
        "compat": [1, 1, 1, 1, 1, 1],
    },
    "doc_3": {
        "sched": [[[0, 1], [0, 0]], [[0, 1], [0, 0]]],  # floor b only shift 1
        "compat": [1, 1, 0, 1, 1, 1],  # incompatibility with nurse #3
    },
    "doc_4": {
        "sched": [[[0, 0], [0, 1]], [[0, 0], [0, 1]]],  # floor b only shift 2
        "compat": [1, 1, 0, 1, 1, 1],  # incompatibility with nurse #3
    },
    "doc_5": {
        "sched": [[[1, 0], [0, 0]], [[1, 0], [0, 0]]],  # floor a only shift 1
        "compat": [0, 1, 1, 0, 1, 1],  # incompatibility with nurse #1 and #4
    }
}

# Useful Maps (value/ref -> index)
day_map = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4}
floor_map = {"a": 0, "b": 1}
shift_map = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4}
