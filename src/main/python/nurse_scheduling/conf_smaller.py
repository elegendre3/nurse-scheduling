num_nurses = 5
num_floors = 3
num_days = 2
num_shifts = 12

floor_needs = [[2] * num_shifts, [1] * num_shifts, [1] + [0] * (num_shifts - 2) + [1], [0] * num_shifts]  # assumed every day is same

nurses_names = [chr(97 + i) for i in range(num_nurses)]

# Schema: [person]_[day]_[shift]_[floor]
var_name_tplt = "%s_%i_%i_%i"

all = {
    "a": {
        "var": [],
        "cost": [
            [[1, 1, 10], [1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10]],
            [[1, 1, 10], [1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10]],
        ],
    },
    "b": {
        "var": [],
        "cost": [
            [[1, 1, 10], [1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10]],
            [[1, 1, 10], [1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10],[1, 1, 10]],
        ],
    },
    "c": {
        "var": [],
        "cost": [
            [[1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10]],
            [[1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10]],
        ],
    },
    "d": {
        "var": [],
        "cost": [
            [[1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10],[1, 1, 10], [1, 1, 10], [1, 1, 10]],
            [[1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10],[1, 1, 10], [1, 1, 10], [1, 1, 10]],
        ],
    },
    "e": {
        "var": [],
        "cost": [
            [[1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10],[1, 1, 10], [1, 1, 10], [1, 1, 10]],
            [[1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10], [1, 1, 10],[1, 1, 10], [1, 1, 10], [1, 1, 10]],
        ],
    },
}
docs = {
    "doc_1": {
        "sched": [
            [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
            [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
        ],  # floor a
        "compat": [1, 1, 1, 1, 1],
    },
    "doc_2": {
        "sched": [
            [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ],  # floor a - not there day 2
        "compat": [1, 1, 1, 1, 1],
    },
    "doc_3": {
        "sched": [
            [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ],  # floor b only morning
        "compat": [1, 1, 1, 1, 1],
    },
}


# Useful Maps (value/ref -> index)
floor_map = {"RDC": 0, "1ER": 1, "ADMIN": 2}
floor_map_inv = {v: k for k, v in floor_map.items()}
shift_map = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "10": 9, "11": 10, "12": 11}
shift_map_inv = {v: k for k, v in shift_map.items()}

nurse_names_map = {
    "a": "DateMike",
    "b": "Jimothy",
    "c": "PAM!",
    "d": "StanleyTheManly",
    "e": "MintDwight",
}

shift_names = {
    0: "8-9",
    1: "9-10",
    2: "10-11",
    3: "11-12",
    4: "12-13",
    5: "13-14",
    6: "14-15",
    7: "15-16",
    8: "16-17",
    9: "17-18",
    10: "18-19",
    11: "19-20",
}
