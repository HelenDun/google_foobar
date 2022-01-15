import time

'''

Final Solution
By Helen Dun
Inspired by Shrey Shah's Solution

'''

def get_empty_nebula(num_rows, num_cols):
    return [[False]*num_cols for _ in range(0, num_rows)]

def get_serial(boolean_values):
    binary = 0b10
    for boolean_value in boolean_values:
        binary += boolean_value
        binary = binary << 1
    return binary >> 1

def get_reflection(nebula):
    num_rows = len(nebula)
    num_cols = len(nebula[0])
    nebula_reflection = get_empty_nebula(num_cols, num_rows)
    for row in range(0, num_rows):
        for col in range(0, num_cols):
            nebula_reflection[col][row] = nebula[row][col]
    return nebula_reflection

POSSIBILITIES_START = {
    True: [
        [
            [True, False],
            [False, False]
        ],
        [
            [False, True],
            [False, False]
        ],
        [
            [False, False],
            [True, False]
        ],
        [
            [False, False],
            [False, True]
        ]
    ],
    False: [
        [
            # ..
            # ..
            [False, False],
            [False, False]
        ],
        [
            # x.
            # x.
            [True, False],
            [True, False]
        ],
        [
            # xx
            # ..
            [True, True],
            [False, False]
        ],
        [
            # x.
            # .x
            [True, False],
            [False, True]
        ],
        [
            # .x
            # x.
            [False, True],
            [True, False]
        ],
        [
            # xx
            # x.
            [True, True],
            [True, False]
        ],
        [
            # ..
            # xx
            [False, False],
            [True, True]
        ],
        [
            # x.
            # xx
            [True, False],
            [True, True]
        ],
        [
            # .x
            # .x
            [False, True],
            [False, True]
        ],
        [
            # xx
            # .x
            [True, True],
            [False, True]
        ],
        [
            # .x
            # xx
            [False, True],
            [True, True]
        ],
        [
            # xx
            # xx
            [True, True],
            [True, True]
        ]
    ]}
POSSIBILITIES_EDGE = {
    # next has gas, top left, top right
    get_serial([True, True, True]): [],
    get_serial([True, True, False]): [
        [False, False]
    ],
    get_serial([True, False, True]): [
        [False, False]
    ],
    get_serial([True, False, False]): [
        [True, False],
        [False, True]
    ],

    get_serial([False, True, True]): [
        [True, True],
        [True, False],
        [False, True],
        [False, False]
    ],
    get_serial([False, True, False]): [
        [True, True],
        [True, False],
        [False, True]
    ],
    get_serial([False, False, True]): [
        [True, True],
        [True, False],
        [False, True]
    ],
    get_serial([False, False, False]): [
        [True, True],
        [False, False]
    ]}

def get_serial_row_pair_possibilities(nebula_row):
    # start with the upper left corner
    has_gas = nebula_row[0]
    curr_possibilities = POSSIBILITIES_START[has_gas]

    # then find each possible and valid row
    for i in range(1, len(nebula_row)):
        next_possibilities = []
        has_gas = nebula_row[i]

        for curr_possibility in curr_possibilities:
            top_left_has_gas = curr_possibility[i][0]
            top_right_has_gas = curr_possibility[i][1]
            serial = get_serial([has_gas, top_left_has_gas, top_right_has_gas])

            # store the curr possibility concatenated with each of the next edge possibilities
            edge_possibilities = POSSIBILITIES_EDGE[serial]
            for edge_possibility in edge_possibilities:
                next_possibilities.append(curr_possibility + [edge_possibility])
        curr_possibilities = next_possibilities

    # serialize each row of boolean values into a binary number
    serial_possibilities = []
    for curr_possibility in curr_possibilities:
        row1 = []
        row2 = []
        for pair in curr_possibility:
            row1.append(pair[0])
            row2.append(pair[1])
        serial1 = get_serial(row1)
        serial2 = get_serial(row2)
        serial_possibilities.append([serial1, serial2])

    return serial_possibilities

def solution(nebula):
    num_rows = len(nebula)
    num_cols = len(nebula[0])

    # have the pass-by-reference lists in the 2D array be the shorter side
    if num_rows < num_cols:
        nebula = get_reflection(nebula)
        num_rows, num_cols = num_cols, num_rows
    
    # count how many of each second row unique serials there are
    pair_second = {}
    serialized_row_pairs = get_serial_row_pair_possibilities(nebula[0])
    for pair in serialized_row_pairs:
        if pair[1] not in pair_second:
            pair_second[pair[1]] = 0
        pair_second[pair[1]] += 1
    
    # continue to count each second row unique serial for further possibilities
    for i in range(1, num_rows):
        pair_first = pair_second
        pair_second = {}
        serialized_row_pairs = get_serial_row_pair_possibilities(nebula[i])
        for pair in serialized_row_pairs:
            if pair[0] not in pair_first:
                pair_first[pair[0]] = 0
            if pair[1] not in pair_second:
                pair_second[pair[1]] = 0
            pair_second[pair[1]] += pair_first[pair[0]]

    # count how many routes there were for the remaining possibilities
    sum = 0
    for key in pair_second:
        sum += pair_second[key]
    return sum



def is_valid(src_nebula, dst_nebula):
    temp_nebula = []
    for row in range(0, len(src_nebula)):
        temp_nebula.append([])
        for col in range(0, len(src_nebula)):
            has_gas = dst_nebula[row][col]
            has_gas += dst_nebula[row][col+1]
            has_gas += dst_nebula[row+1][col]
            has_gas += dst_nebula[row+1][col+1]
            temp_nebula[row].append(has_gas == 1)

    for row in range(0, len(src_nebula)):
        for col in range(0, len(src_nebula)):
            if src_nebula[row][col] != temp_nebula[row][col]:
                return False

    return True

def recursive_combinations(missing_num, bunnies_index, bunnies_num, combination):
    if (missing_num > bunnies_num - bunnies_index):
        print("!!Error: More True values to assign than available spots!!")
        print_stat(missing_num, bunnies_index, bunnies_num, combination)
        exit(1)
    elif (bunnies_num <= 0):
        print("!!Error: Number of bunnies is <= 0!!")
        print_stat(missing_num, bunnies_index, bunnies_num, combination)
        exit(1)
    elif (missing_num <= 0):
        list_of_combinations = [combination]
    elif (missing_num == bunnies_num - bunnies_index):
        combination.append(True)
        return recursive_combinations(missing_num - 1, bunnies_index + 1, bunnies_num, combination)
    else:
        duplicate = combination[:]
        combination.append(True)
        duplicate.append(False)
        list_of_combinations = recursive_combinations(missing_num - 1, bunnies_index + 1, bunnies_num, combination)
        list_of_combinations += recursive_combinations(missing_num, bunnies_index + 1, bunnies_num, duplicate)
    return list_of_combinations

def brute_force(src_nebula):
    num_rows = len(src_nebula)
    num_cols = len(src_nebula[0])
    if (num_rows > 3 or num_cols > 3):
        return -1
    max_index = (num_rows+1) * (num_cols+1)

    dst_nebula = get_empty_nebula(num_rows+1, num_cols+1)
    count = 0 + is_valid(src_nebula, dst_nebula)

    for i in range(1, max_index+1):
        combinations = recursive_combinations(i, 0, max_index, [])
        for combination in combinations:
            for j in range(0, len(combination)):
                value = combination[j]
                row = j // (num_cols+1)
                col = j % (num_cols+1)
                dst_nebula[row][col] = value
            for j in range(len(combination), max_index):
                row = j // (num_cols+1)
                col = j % (num_cols+1)
                dst_nebula[row][col] = False
            count += is_valid(src_nebula, dst_nebula)
    return count

def print_nebula(nebula):
    num_rows = len(nebula)
    num_cols = len(nebula[0])
    for row in range(0, num_rows):
        print(str(row) + ":\t",end="")

        for col in range(0, num_cols):
            if nebula[row][col]:
                print("x",end="")
            else:
                print(".",end="")

        print("")

def test_solution_silent(nebula):
    result_s = solution(nebula)
    result_bf = brute_force(nebula)
    if result_s != result_bf:
        print("WARNING!! Different Results!!")
        print("Nebula:")
        print_nebula(nebula)
        print("V4 Result: " + str(result_s))
        print("BF Result: " + str(result_bf))

def test_solutions_by_size(num_rows, num_cols):
    max_index = num_rows * num_cols
    src_nebula = get_empty_nebula(num_rows,num_cols)
    test_solution_silent(src_nebula)

    for i in range(1, max_index+1):
        combinations = recursive_combinations(i, 0, max_index, [])
        for k in range(0, len(combinations)):
            combination = combinations[k]
            for j in range(0, len(combination)):
                value = combination[j]
                row = j // (num_cols)
                col = j % (num_cols)
                src_nebula[row][col] = value
            for j in range(len(combination), max_index):
                row = j // (num_cols)
                col = j % (num_cols)
                src_nebula[row][col] = False
            test_solution_silent(src_nebula)
    return

def test_solution(num, nebula, expected):
    print("Solution Test " + str(num))
    print("Nebula:")
    print_nebula(nebula)
    print("Expected: " + str(expected))
    start = time.time()
    result = solution(nebula)
    stop = time.time()
    print("V4 Result: " + str(result))
    print("V4 Time: " + str(stop-start))
    start = time.time()
    result = brute_force(nebula)
    stop = time.time()
    print("BF Result: " + str(result))
    print("BF Time: " + str(stop-start))
    print("")
    print("")

def test_solutions():
    nebula = [
        [True, True, False, True, False, True, False, True, True, False],
        [True, True, False, False, False, False, True, True, True, False],
        [True, True, False, False, False, False, False, False, False, True],
        [False, True, False, False, False, False, True, True, False, False]
    ]
    test_solution(1,nebula,11567)

    nebula = [
        [True, False, True],
        [False, True, False],
        [True, False, True]
    ]
    test_solution(2,nebula,4)

    nebula = [
        [True, False, True, False, False, True, True, True], 
        [True, False, True, False, False, False, True, False], 
        [True, True, True, False, False, False, True, False], 
        [True, False, True, False, False, False, True, False], 
        [True, False, True, False, False, True, True, True]
    ]
    test_solution(3,nebula,254)

    nebula = get_empty_nebula(2,2)
    test_solution(4,nebula,208)

    nebula = get_empty_nebula(3,3)
    test_solution(5,nebula,10148)

    nebula = [
        [True, True],
        [True, True]
    ]
    test_solution(6,nebula,8)

    nebula = [
        [True, True, True],
        [True, True, True],
        [True, True, True]
    ]
    test_solution(7,nebula,12)

    nebula = [
        [True, True, True, True],
        [True, True, True, True],
        [True, True, True, True],
        [True, True, True, True]
    ]
    test_solution(8,nebula,20)

    nebula = [
        [True, True, True, True, True],
        [True, True, True, True, True],
        [True, True, True, True, True],
        [True, True, True, True, True],
        [True, True, True, True, True]
    ]
    test_solution(9,nebula,28)

    nebula = [
        [False, True, False],
        [False, False, False],
        [False, True, True],
    ]
    test_solution(10,nebula,-1)

    nebula = [
        [False, False, False],
        [False, False, True],
        [False, True, True],
    ]
    test_solution(11,nebula,-1)

    nebula = [
        [False, True, True],
        [False, False, True],
        [False, False, False],
    ]
    test_solution(12,nebula,-1)

    nebula = [
        [True, False, False],
        [False, False, False],
        [False, False, False],
    ]
    test_solution(13,nebula,2056)

    nebula = [
        [False, False, False],
        [False, False, False],
        [True, False, False],
    ]
    test_solution(14,nebula,2056)

    nebula = [
        [False, False, True],
        [False, False, False],
        [False, False, False],
    ]
    test_solution(15,nebula,2056)

    nebula = [
        [False, False, False],
        [False, False, False],
        [False, False, True],
    ]
    test_solution(16,nebula,2056)

    nebula = [
        [True, False],
        [False, False]
    ]
    test_solution(17,nebula,38)

    nebula = [
        [False, True],
        [False, False]
    ]
    test_solution(18,nebula,38)

    nebula = [
        [False, False],
        [True, False]
    ]
    test_solution(19,nebula,38)

    nebula = [
        [False, False],
        [False, True]
    ]
    test_solution(20,nebula,38)
    return

test_solutions()