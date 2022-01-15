import time

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

def get_empty_nebula(num_rows, num_cols):
    return [[False]*num_cols for _ in range(0, num_rows)]

def get_serial(boolean_values):
    binary = 0b10
    for boolean_value in boolean_values:
        binary += boolean_value
        binary = binary << 1
    return binary >> 1

POSSIBILITIES_START = {
    True: [
        [
            [True, False],
            [False, False],
            1
        ],
        [
            [False, True],
            [False, False],
            1
        ],
        [
            [False, False],
            [True, False],
            1
        ],
        [
            [False, False],
            [False, True],
            1
        ]
    ],
    False: [
        [
            # ..
            # ..
            [False, False],
            [False, False],
            1
        ],
        [
            # x.
            # x.
            [True, False],
            [True, False],
            1
        ],
        [
            # xx
            # ..
            [True, True],
            [False, False],
            1
        ],
        [
            # x.
            # .x
            [True, False],
            [False, True],
            1
        ],
        [
            # xx # .x
            # x. # x.
            [False, True],
            [True, False],
            2
        ],
        [
            # x. # ..
            # xx # xx
            [False, False],
            [True, True],
            2
        ],
        [
            # xx # .x
            # .x # .x
            [False, True],
            [False, True],
            2
        ],
        [
            # xx # .x
            # xx # xx
            [False, True],
            [True, True],
            2
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
POSSIBILITIES_CORNER = {
    get_serial([True, True, True, True]): [],
    get_serial([True, True, True, False]): [],
    get_serial([True, True, False, True]): [],
    get_serial([True, False, True, True]): [],
    get_serial([True, False, False, True]): [
        [False]
    ],
    get_serial([True, False, True, False]): [
        [False]
    ],
    get_serial([True, True, False, False]): [
        [False]
    ],
    get_serial([True, False, False, False]): [
        [True]
    ],

    get_serial([False, True, True, True]): [
        [True],
        [False]
    ],
    get_serial([False, True, True, False]): [
        [True],
        [False]
    ],
    get_serial([False, True, False, True]): [
        [True],
        [False]
    ],
    get_serial([False, False, True, True]): [
        [True],
        [False]
    ],
    get_serial([False, False, False, True]): [
        [True]
    ],
    get_serial([False, False, True, False]): [
        [True]
    ],
    get_serial([False, True, False, False]): [
        [True]
    ],
    get_serial([False, False, False, False]): [
        [False]
    ]}

def fill_remaining_row_squares(src_nebula, dst_nebula, row, col, num_squares):
    srcs_have_gas = []
    top_left_has_gas = dst_nebula[row][col]
    tops_have_gas = []
    bottom_left_has_gas = dst_nebula[row+1][col]
    for c in range(col, col + num_squares):
        srcs_have_gas.append(src_nebula[row][c])
        tops_have_gas.append(dst_nebula[row][c+1])
    serial = srcs_have_gas + tops_have_gas + [top_left_has_gas, bottom_left_has_gas]
    serial = get_serial(serial)

    if serial in POSSIBILITIES_CORNER:
        return POSSIBILITIES_CORNER[serial]

    possibilities = []
    half = num_squares // 2
    left = fill_remaining_row_squares(src_nebula, dst_nebula, row, col, half)
    for possibile_left in left:

        # add the possibility to the 2D array
        for i in range(0, len(possibile_left)):
            dst_nebula[row+1][col+i+1] = possibile_left[i]

        # get further possibilities
        right = fill_remaining_row_squares(src_nebula, dst_nebula, row, col + half, num_squares - half)
        for possible_right in right:
            possibilities.append(possibile_left + possible_right)
    
    # add the possibilities to the dynamic programming table
    POSSIBILITIES_CORNER[serial] = possibilities
    return possibilities

def fill_remaining_squares(src_nebula, dst_nebula):
    num_rows = len(src_nebula)
    num_cols = len(src_nebula[0])
    row = 1
    col = 1

    count = 0
    stack = [] # [row, clouds]

    possibilities = fill_remaining_row_squares(src_nebula, dst_nebula, row, col, num_cols - col)
    for possibility in possibilities:
        stack.append([row, possibility])

    while len(stack) > 0:
        # get the next possibility
        element = stack.pop()
        row = element[0]
        possibility = element[1]
        
        # set the nebula to the possibility
        for i in range(col, num_cols):
            dst_nebula[row+1][i+1] = possibility[i-col]

        # get the next row
        if row == num_rows - 1:
            if not is_valid(src_nebula, dst_nebula):
                print("INVALID")
                exit(1)
            count += 1
            continue

        # get what the next possibilities are
        row = row + 1
        possibilities = fill_remaining_row_squares(src_nebula, dst_nebula, row, col, num_cols - col)
        for possibility in possibilities:
            stack.append([row, possibility])

    # end of while loop
    return count

def fill_left_col_squares(src_nebula, dst_nebula):
    num_rows = len(src_nebula)
    row = 1
    col = 0

    count = 0
    stack = [] # [row, cloud]

    src_has_gas = src_nebula[row][col]
    top_left_has_gas = dst_nebula[row][col]
    top_right_has_gas = dst_nebula[row][col+1]
    serial = get_serial([src_has_gas, top_left_has_gas, top_right_has_gas])

    possibilities = POSSIBILITIES_EDGE[serial]
    for possibility in possibilities:
        stack.append([row, possibility])

    while len(stack) > 0:
        # get the next possibility
        element = stack.pop()
        row = element[0]
        possibility = element[1]
        
        # set the nebula to the possibility
        dst_nebula[row+1][col] = possibility[0]
        dst_nebula[row+1][col+1] = possibility[1]

        # if this possibility fills the left column
        # then the next possibility is in fill_remaining
        if row == num_rows - 1:
            count += fill_remaining_squares(src_nebula, dst_nebula)
            continue

        # get what the next possibilities are
        row = row + 1
        src_has_gas = src_nebula[row][col]
        top_left_has_gas = dst_nebula[row][col]
        top_right_has_gas = dst_nebula[row][col+1]
        serial = get_serial([src_has_gas, top_left_has_gas, top_right_has_gas])

        # add all of the next possibilities to the stack
        possibilities = POSSIBILITIES_EDGE[serial]
        for possibility in possibilities:
            stack.append([row, possibility])

    # end of while loop
    return count

def fill_top_row_squares(src_nebula, dst_nebula):
    num_cols = len(src_nebula[0])
    row = 0
    col = 1

    count = 0
    stack = [] # [col, clouds]

    src_has_gas = src_nebula[row][col]
    top_left_has_gas = dst_nebula[row][col]
    bottom_left_has_gas = dst_nebula[row+1][col]
    serial = get_serial([src_has_gas, top_left_has_gas, bottom_left_has_gas])

    possibilities = POSSIBILITIES_EDGE[serial]
    for possibility in possibilities:
        stack.append([col, possibility])

    while len(stack) > 0:
        # get the next possibility
        element = stack.pop()
        col = element[0]
        possibility = element[1]
        
        # set the nebula to the possibility
        dst_nebula[row][col+1] = possibility[0]
        dst_nebula[row+1][col+1] = possibility[1]

        # if this possibility fills the top row
        # then the next possibility is in fill_left_col
        if col == num_cols - 1:
            count += fill_left_col_squares(src_nebula, dst_nebula)
            continue

        # get what the next possibilities are
        col = col + 1
        src_has_gas = src_nebula[row][col]
        top_left_has_gas = dst_nebula[row][col]
        bottom_left_has_gas = dst_nebula[row+1][col]
        serial = get_serial([src_has_gas, top_left_has_gas, bottom_left_has_gas])

        # add all of the next possibilities to the stack
        possibilities = POSSIBILITIES_EDGE[serial]
        for possibility in possibilities:
            stack.append([col, possibility])

    # end of while loop
    return count

def fill_start_square(src_nebula):
    num_rows = len(src_nebula)
    num_cols = len(src_nebula[0])
    dst_nebula = get_empty_nebula(num_rows+1, num_cols+1)

    count = 0
    src_has_gas = src_nebula[0][0]
    possibilities = POSSIBILITIES_START[src_has_gas]
    for possibility in possibilities:
        dst_nebula[0][0] = possibility[0][0]
        dst_nebula[0][1] = possibility[0][1]
        dst_nebula[1][0] = possibility[1][0]
        dst_nebula[1][1] = possibility[1][1]
        count += possibility[2] * fill_top_row_squares(src_nebula, dst_nebula)

    return count

def solution(nebula):
    return fill_start_square(nebula)


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

def test_solution(num, nebula, expected):
    print("Solution Test " + str(num))
    print("Nebula:")
    print_nebula(nebula)
    print("Expected: " + str(expected))
    start = time.time()
    result = solution(nebula)
    stop = time.time()
    print("V3 Result: " + str(result))
    print("V3 Time: " + str(stop-start))
    start = time.time()
    result = brute_force(nebula)
    stop = time.time()
    print("BF Result: " + str(result))
    print("BF Time: " + str(stop-start))
    print("")
    print("")

def test_solution_silent(nebula):
    result_s = solution(nebula)
    result_bf = brute_force(nebula)
    if result_s != result_bf:
        print("WARNING!! Different Results!!")
        print("Nebula:")
        print_nebula(nebula)
        print("V3 Result: " + str(result_s))
        print("BF Result: " + str(result_bf))


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

def test_possibilities():
    for key in POSSIBILITIES_CORNER:
        print("Serial: " + bin(key))
        print("Possible: " + str(POSSIBILITIES_CORNER[key]))
        print("")
    print("")
    print("")
    print("")
    return

#test_solutions()
#test_solutions_by_size(2,2)
test_solutions_by_size(4,10)

nebula = [
    [False, True],
    [False, False]
]
#test_solution(18,nebula,38)