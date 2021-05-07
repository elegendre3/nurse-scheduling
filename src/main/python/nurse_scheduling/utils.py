from typing import List


def deepflatten(input_list: List):
    """Recursively flattens any nested list"""
    if input_list == []:
        return input_list
    if isinstance(input_list[0], list):
        return deepflatten(input_list[0]) + deepflatten(input_list[1:])
    return input_list[:1] + deepflatten(input_list[1:])


if __name__ == "__main__":
    list_1 = [
        [1, 2, 3], [4, 5, 6]
    ]
    list_2 = [
        [
            [1, 2, 3], [4, 5, 6]
        ],
        [
            [7, 8, 9], [10, 11, 12]
        ]
    ]
    list_2b = [
        [
            ['aa', 'b', 'c'], [4, 5, 6]
        ],
        [
            [7, 8, 9], [10, 11, 12]
        ]
    ]
    list_3 = [
        [
            [
                [1, 2, 3], [4, 5, 6]
            ],
            [
                [7, 8, 9], [10, 11, 12]
            ]
        ],
        [
            [
                [13, 14, 15], [16, 17, 18]
            ],
            [
                [19, 20, 21], [22, 23, 24]
            ]
        ]
    ]

    print(deepflatten(list_1))
    print(deepflatten(list_2))
    print(deepflatten(list_2b))
    print(deepflatten(list_3))
