num_nurses = 7
num_floors = 4
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
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
        ],
    },
    "b": {
        "var": [],
        "cost": [
            [[2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10]],
            [[2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10], [2, 1, 1, 10]],
        ],  # expensive to be put on floor a
    },
    "c": {
        "var": [],
        "cost": [
            [[3, 3, 3, 30], [3, 3, 3, 30], [3, 3, 3, 30], [3, 3, 3, 30], [3, 3, 3, 30], [3, 3, 3, 30], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
            [[3, 3, 3, 30], [3, 3, 3, 30], [3, 3, 3, 30], [3, 3, 3, 30], [3, 3, 3, 30], [3, 3, 3, 30], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
        ],  # expensive to work shift 1 (~mornings)
    },
    "d": {
        "var": [],
        "cost": [
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [5, 5, 5, 50], [5, 5, 5, 50], [5, 5, 5, 50], [5, 5, 5, 50], [5, 5, 5, 50], [5, 5, 5, 50]],
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [5, 5, 5, 50], [5, 5, 5, 50], [5, 5, 5, 50], [5, 5, 5, 50], [5, 5, 5, 50], [5, 5, 5, 50]],
        ],  # expensive to work shift 2 (~afternoons)
    },
    "e": {
        "var": [],
        "cost": [
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
        ],
    },
    "f": {
        "var": [],
        "cost": [
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
        ],
    },
    "g": {
        "var": [],
        "cost": [
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
            [[1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10], [1, 1, 1, 10]],
        ],
    },
}
docs = {
    "doc_1": {
        "sched": [
            [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
            [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
        ],  # floor a
        "compat": [1, 1, 1, 1, 1, 1, 1],
    },
    "doc_2": {
        "sched": [
            [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ],  # floor a - not there day 2
        "compat": [1, 1, 1, 1, 1, 1, 1],
    },
    "doc_3": {
        "sched": [
            [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ],  # floor b only morning
        "compat": [1, 1, 1, 1, 1, 1, 1],
    },
    "doc_4": {
        "sched": [
            [[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0]],
            [[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0]],
        ],  # floor a only first and last shift
        "compat": [0, 0, 0, 0, 0, 1, 1],  # incompatibility with all but last one
    },
}


# Useful Maps (value/ref -> index)
floor_map = {"RDC": 0, "1ER": 1, "APPAREILS": 2, "ADMIN": 3}
floor_map_inv = {v: k for k, v in floor_map.items()}
shift_map = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "10": 9, "11": 10, "12": 11}
shift_map_inv = {v: k for k, v in shift_map.items()}

nurse_names_map = {
    "a": "DateMike",
    "b": "Jimothy",
    "c": "PAM!",
    "d": "Mose",
    "e": "StanlyTheManly",
    "f": "ItGuy",
    "g": "California",
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