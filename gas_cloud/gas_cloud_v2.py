import time

def get_empty_nebula(num_rows, num_cols):
    return [[False]*num_cols for _ in range(0, num_rows)]

def get_serial(boolean_values):
    binary = 0b0
    for boolean_value in boolean_values:
        binary += boolean_value
        binary = binary << 1
    return binary

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
        False
    ],
    get_serial([True, False, True, False]): [
        False
    ],
    get_serial([True, True, False, False]): [
        False
    ],
    get_serial([True, False, False, False]): [
        True
    ],

    get_serial([False, True, True, True]): [
        True,
        False
    ],
    get_serial([False, True, True, False]): [
        True,
        False
    ],
    get_serial([False, True, False, True]): [
        True,
        False
    ],
    get_serial([False, False, True, True]): [
        True,
        False
    ],
    get_serial([False, False, False, True]): [
        True
    ],
    get_serial([False, False, True, False]): [
        True
    ],
    get_serial([False, True, False, False]): [
        True
    ],
    get_serial([False, False, False, False]): [
        False
    ]}

def fill_remaining_squares(src_nebula, dst_nebula):
    num_rows = len(src_nebula)
    num_cols = len(src_nebula[0])
    row = 1
    col = 1

    count = 0
    stack = [] # [index, clouds]

    src_has_gas = src_nebula[row][col]
    top_left_has_gas = dst_nebula[row][col]
    top_right_has_gas = dst_nebula[row][col+1]
    bottom_left_has_gas = dst_nebula[row+1][col]
    serial = get_serial([src_has_gas, top_left_has_gas, top_right_has_gas, bottom_left_has_gas])

    clouds = POSSIBILITIES_CORNER[serial]
    for cloud in clouds:
        stack.append([row, col, cloud])

    while len(stack) > 0:
        # get the next possibility
        element = stack.pop()
        row = element[0]
        col = element[1]
        cloud = element[2]
        
        # set the nebula to the possibility
        dst_nebula[row+1][col+1] = cloud

        # if this possibility fills the top row
        # then the next possibility is in fill_remaining
        if col == num_cols-1:
            if row == num_rows-1:
                count += 1
                continue
            else:
                row = row + 1
                col = 1
        else:
            col = col + 1

        # get what the next possibilities are
        src_has_gas = src_nebula[row][col]
        top_left_has_gas = dst_nebula[row][col]
        top_right_has_gas = dst_nebula[row][col+1]
        bottom_left_has_gas = dst_nebula[row+1][col]
        serial = get_serial([src_has_gas, top_left_has_gas, top_right_has_gas, bottom_left_has_gas])

        # add all of the next possibilities to the stack
        clouds = POSSIBILITIES_CORNER[serial]
        for cloud in clouds:
            stack.append([row, col, cloud])

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

    clouds = POSSIBILITIES_EDGE[serial]
    for cloud in clouds:
        stack.append([row, cloud])

    while len(stack) > 0:
        # get the next possibility
        element = stack.pop()
        row = element[0]
        cloud = element[1]
        
        # set the nebula to the possibility
        dst_nebula[row+1][col] = cloud[0]
        dst_nebula[row+1][col+1] = cloud[1]

        # if this possibility fills the top row
        # then the next possibility is in fill_remaining
        if row == num_rows-1:
            count += fill_remaining_squares(src_nebula, dst_nebula)
            continue

        # get what the next possibilities are
        row = row + 1
        src_has_gas = src_nebula[row][col]
        top_left_has_gas = dst_nebula[row][col]
        top_right_has_gas = dst_nebula[row][col+1]
        serial = get_serial([src_has_gas, top_left_has_gas, top_right_has_gas])

        # add all of the next possibilities to the stack
        clouds = POSSIBILITIES_EDGE[serial]
        for cloud in clouds:
            stack.append([row, cloud])

    # end of while loop
    for i in range(2, row):
        dst_nebula[i][col] = False
        dst_nebula[i][col+1] = False
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

    clouds = POSSIBILITIES_EDGE[serial]
    for cloud in clouds:
        stack.append([col, cloud])

    while len(stack) > 0:
        # get the next possibility
        element = stack.pop()
        col = element[0]
        cloud = element[1]
        
        # set the nebula to the possibility
        dst_nebula[row][col+1] = cloud[0]
        dst_nebula[row+1][col+1] = cloud[1]

        # if this possibility fills the top row
        # then the next possibility is in fill_remaining
        if col == num_cols-1:
            count += fill_left_col_squares(src_nebula, dst_nebula)
            continue

        # get what the next possibilities are
        col = col+1
        src_has_gas = src_nebula[row][col]
        top_left_has_gas = dst_nebula[row][col]
        bottom_left_has_gas = dst_nebula[row+1][col]
        serial = get_serial([src_has_gas, top_left_has_gas, bottom_left_has_gas])

        # add all of the next possibilities to the stack
        clouds = POSSIBILITIES_EDGE[serial]
        for cloud in clouds:
            stack.append([col, cloud])

    # end of while loop
    return count

def fill_start_square(src_nebula):
    num_rows = len(src_nebula)
    num_cols = len(src_nebula[0])
    dst_nebula = get_empty_nebula(num_rows+1, num_cols+1)

    count = 0
    src_has_gas = src_nebula[0][0]
    clouds = POSSIBILITIES_START[src_has_gas]
    for cloud in clouds:
        dst_nebula[0][0] = cloud[0][0]
        dst_nebula[0][1] = cloud[0][1]
        dst_nebula[1][0] = cloud[1][0]
        dst_nebula[1][1] = cloud[1][1]
        count += cloud[2] * fill_top_row_squares(src_nebula, dst_nebula)

    return count

def solution(nebula):
    return fill_start_square(nebula)




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
    print("Result: " + str(result))
    print("Time: " + str(stop-start))
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
    test_solution(4,nebula,0)

test_solutions()