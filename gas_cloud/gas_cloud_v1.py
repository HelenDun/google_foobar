import time

def get_empty_nebula(num_rows, num_cols):
    nebula = []
    for i in range(0,num_rows):
        nebula.append([])
        for j in range(0, num_cols):
            nebula[i].append(False)
    return nebula

def get_copy_nebula(nebula):
    nebula_copy = [row[:] for row in nebula]
    return nebula_copy

def get_gas_count(row, col, nebula):
    num_gas = nebula[row][col]
    num_gas += nebula[row][col+1]
    num_gas += nebula[row+1][col]
    num_gas += nebula[row+1][col+1]
    return num_gas

def fill_start_square(next_nebula):
    num_rows = len(next_nebula)
    num_cols = len(next_nebula[0])
    next_has_gas = next_nebula[0][0]

    nebulae = []
    nebula_empty = get_empty_nebula(num_rows+1, num_cols+1)

    if next_has_gas:

        # x.
        # ..
        nebula = get_copy_nebula(nebula_empty)
        nebula[0][0] = True
        nebulae.append([1,nebula])

        # .x
        # ..
        nebula = get_copy_nebula(nebula_empty)
        nebula[0][1] = True
        nebulae.append([1,nebula])

        # ..
        # x.
        nebula = get_copy_nebula(nebula_empty)
        nebula[1][0] = True
        nebulae.append([1,nebula])
        
        # ..
        # .x
        nebula_empty[1][1] = True
        nebulae.append([1,nebula_empty])
        
    else:

        # xx # .x
        # xx # xx
        nebula = get_copy_nebula(nebula_empty)
        nebula[0][1] = True
        nebula[1][0] = True
        nebula[1][1] = True
        nebulae.append([2,nebula])

        # xx # .x
        # .x # .x
        nebula = get_copy_nebula(nebula_empty)
        nebula[0][1] = True
        nebula[1][1] = True
        nebulae.append([2,nebula])

        # x. # ..
        # xx # xx
        nebula = get_copy_nebula(nebula_empty)
        nebula[1][0] = True
        nebula[1][1] = True
        nebulae.append([2,nebula])

        # xx # .x
        # x. # x.
        nebula = get_copy_nebula(nebula_empty)
        nebula[0][1] = True
        nebula[1][0] = True
        nebulae.append([2,nebula])
        
        # x.
        # .x
        nebula = get_copy_nebula(nebula_empty)
        nebula[0][0] = True
        nebula[1][1] = True
        nebulae.append([1,nebula])
        
        # xx
        # ..
        nebula = get_copy_nebula(nebula_empty)
        nebula[0][0] = True
        nebula[0][1] = True
        nebulae.append([1,nebula])
        
        # x.
        # x.
        nebula = get_copy_nebula(nebula_empty)
        nebula[0][0] = True
        nebula[1][0] = True
        nebulae.append([1,nebula])
        
        # ..
        # ..
        nebulae.append([1,nebula_empty])

    return nebulae

def fill_top_row_squares(next_nebula, old_nebulae):
    row = 0
    num_cols = len(next_nebula[0])
    for col in range(1, num_cols):
        new_nebulae = []
        next_has_gas = next_nebula[row][col]

        # for each possible nebula pattern, get the possible 2x2 squares
        for i in range(0, len(old_nebulae)):
            num_duplicates = old_nebulae[i][0]
            nebula = old_nebulae[i][1]
            num_gas = get_gas_count(row,col,nebula)

            # if there is gas in this square for the next nebula, 
            # the 2x2 square for this nebula must have exactly 1 gas square in it
            if next_has_gas:
                if num_gas > 1:
                    continue
                elif num_gas == 0:
                    # .x
                    # ..
                    temp_nebula = get_copy_nebula(nebula)
                    temp_nebula[row][col+1] = True
                    new_nebulae.append([num_duplicates, temp_nebula])
                    # ..
                    # .x
                    nebula[row+1][col+1] = True
                    new_nebulae.append([num_duplicates, nebula])
                else: # num_gas == 1:
                    new_nebulae.append([num_duplicates, nebula])

            # if there is no gas in this square for the next nebula,
            # the 2x2 square for this nebula must have anything but exactly 1 gas square
            else:

                if num_gas == 0:
                    # .x
                    # .x
                    temp_nebula = get_copy_nebula(nebula)
                    temp_nebula[row][col+1] = True
                    temp_nebula[row+1][col+1] = True
                    new_nebulae.append([num_duplicates, temp_nebula])

                    # ..
                    # ..
                    new_nebulae.append([num_duplicates, nebula])
                    continue

                # special top-right corner case
                elif col == num_cols - 1:
                    if num_gas == 2:
                        # x. # xx
                        # x. # x.
                        temp_nebula = get_copy_nebula(nebula)
                        new_nebulae.append([2*num_duplicates, temp_nebula])

                        # x. # xx
                        # xx # xx
                        nebula[row+1][col+1] = True
                        new_nebulae.append([2*num_duplicates, nebula])

                    else: # num_gas == 1
                        # yx
                        # y.
                        temp_nebula = get_copy_nebula(nebula)
                        new_nebulae.append([num_duplicates, temp_nebula])

                        # y. # yx
                        # yx # yx
                        nebula[row+1][col+1] = True
                        new_nebulae.append([2*num_duplicates, nebula])
                    continue

                elif num_gas == 2:
                    # x.
                    # x.
                    temp_nebula = get_copy_nebula(nebula)
                    new_nebulae.append([num_duplicates, temp_nebula])

                #if num_gas >= 1:
                # yx | xx
                # y. | x.
                temp_nebula = get_copy_nebula(nebula)
                temp_nebula[row][col+1] = True
                new_nebulae.append([num_duplicates, temp_nebula])

                # y. | x.
                # yx | xx
                temp_nebula = get_copy_nebula(nebula)
                temp_nebula[row+1][col+1] = True
                new_nebulae.append([num_duplicates, temp_nebula])

                # yx | xx
                # yx | xx
                nebula[row][col+1] = True
                nebula[row+1][col+1] = True
                new_nebulae.append([num_duplicates, nebula])
        old_nebulae = new_nebulae
    return new_nebulae

def fill_left_col_squares(next_nebula, old_nebulae):
    col = 0
    num_rows = len(next_nebula)
    for row in range(1, num_rows):
        new_nebulae = []
        next_has_gas = next_nebula[row][col]

        # for each possible nebula pattern, get the possible 2x2 squares
        for i in range(0, len(old_nebulae)):

            num_duplicates = old_nebulae[i][0]
            nebula = old_nebulae[i][1]
            num_gas = get_gas_count(row,col,nebula)

            # if there is gas in this square for the next nebula, 
            # the 2x2 square for this nebula must have exactly 1 gas square in it
            if next_has_gas:
                if num_gas > 1:
                    continue
                elif num_gas == 0:
                    # ..
                    # x.
                    temp_nebula = get_copy_nebula(nebula)
                    temp_nebula[row+1][col] = True
                    new_nebulae.append([num_duplicates, temp_nebula])
                    # ..
                    # .x
                    nebula[row+1][col+1] = True
                    new_nebulae.append([num_duplicates, nebula])
                else: # num_gas == 1:
                    new_nebulae.append([num_duplicates, nebula])

            # if there is no gas in this square for the next nebula,
            # the 2x2 square for this nebula must have anything but exactly 1 gas square
            else:
                if num_gas == 0:
                    # ..
                    # xx
                    temp_nebula = get_copy_nebula(nebula)
                    temp_nebula[row+1][col] = True
                    temp_nebula[row+1][col+1] = True
                    new_nebulae.append([num_duplicates, temp_nebula])

                    # ..
                    # ..
                    new_nebulae.append([num_duplicates, nebula])
                    continue

                # special bottom-left corner case
                elif row == num_rows - 1:
                    if num_gas == 2:
                        # xx # xx
                        # x. # ..
                        temp_nebula = get_copy_nebula(nebula)
                        new_nebulae.append([2*num_duplicates, temp_nebula])

                        # xx # xx
                        # .x # xx
                        nebula[row+1][col+1] = True
                        new_nebulae.append([2*num_duplicates, nebula])

                    else: # num_gas == 1
                        # yy
                        # x.
                        temp_nebula = get_copy_nebula(nebula)
                        temp_nebula[row+1][col] = True
                        new_nebulae.append([num_duplicates, temp_nebula])

                        # yy # yy
                        # .x # xx
                        nebula[row+1][col+1] = True
                        new_nebulae.append([2*num_duplicates, nebula])
                    continue

                elif num_gas == 2:
                    # xx
                    # ..
                    temp_nebula = get_copy_nebula(nebula)
                    new_nebulae.append([num_duplicates, temp_nebula])

                #if num_gas >= 1:
                # yy | xx
                # x. | x.
                temp_nebula = get_copy_nebula(nebula)
                temp_nebula[row+1][col] = True
                new_nebulae.append([num_duplicates, temp_nebula])

                # yy | xx
                # .x | .x 
                temp_nebula = get_copy_nebula(nebula)
                temp_nebula[row+1][col+1] = True
                new_nebulae.append([num_duplicates, temp_nebula])

                # yy | xx
                # xx | xx
                nebula[row+1][col] = True
                nebula[row+1][col+1] = True
                new_nebulae.append([num_duplicates, nebula])
        old_nebulae = new_nebulae
    return new_nebulae

def fill_remaining_squares(next_nebula, old_nebulae):
    num_rows = len(next_nebula)
    num_cols = len(next_nebula[0])

    for row in range(1, num_rows):
        for col in range(1, num_cols):
            new_nebulae = []
            next_has_gas = next_nebula[row][col]

            for i in range(0, len(old_nebulae)):
                num_duplicates = old_nebulae[i][0]
                nebula = old_nebulae[i][1]
                num_gas = get_gas_count(row,col,nebula)

                if next_has_gas:
                    if num_gas > 1:
                        continue
                    elif num_gas == 0:
                        nebula[row+1][col+1] = True
                        new_nebulae.append([num_duplicates, nebula])
                    else: # num_gas == 1:
                        new_nebulae.append([num_duplicates, nebula])

                else: # if not next_has_gas
                    if num_gas == 0:
                        # ..
                        # ..
                        new_nebulae.append([num_duplicates, nebula])
                        continue
                    elif num_gas >= 2:
                        # zz
                        # z.
                        temp_nebula = get_copy_nebula(nebula)
                        new_nebulae.append([num_duplicates, temp_nebula])
                    # num_gas >= 1
                    # yy | zz
                    # yx | zx
                    nebula[row+1][col+1] = True
                    new_nebulae.append([num_duplicates, nebula])
            old_nebulae = new_nebulae
    return new_nebulae

def get_nebulae(next_nebula):
    nebulae = fill_start_square(next_nebula)
    nebulae = fill_top_row_squares(next_nebula, nebulae)
    nebulae = fill_left_col_squares(next_nebula, nebulae)
    nebulae = fill_remaining_squares(next_nebula, nebulae)
    return nebulae

def get_nebulae_sum(nebulae):
    sum = 0
    for i in range(0, len(nebulae)):
        sum += nebulae[i][0]
    return sum

def solution(nebula):
    nebulae = get_nebulae(nebula)
    return get_nebulae_sum(nebulae)


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

def print_nebulae(nebulae):
    for i in range(0, len(nebulae)):
        num_duplicates = nebulae[i][0]
        nebula = nebulae[i][1]
        print("Nebula " + str(i) + "\t\t" + str(num_duplicates) + " Duplicate(s)")
        print_nebula(nebula)
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

    #nebula = get_empty_nebula(5,5)
    #test_solution(4,nebula,0)

def test_nebulae(num, next_nebula):
    print("===Nebulae Test " + str(num) + "===")
    print("Next Nebula:")
    print_nebula(next_nebula)
    print("")
    print("")

    print("**Fill Start Square**")
    start = fill_start_square(next_nebula)
    print_nebulae(start)
    print("")
    print("")

    print("**Fill Top Row Squares**")
    top_row = fill_top_row_squares(next_nebula, start)
    print_nebulae(top_row)
    print("")
    print("")

    print("**Fill Left Col Squares**")
    left_col = fill_left_col_squares(next_nebula, top_row)
    print_nebulae(left_col)
    print("")
    print("")
    
    print("**Fill Remaining Squares**")
    remaining = fill_remaining_squares(next_nebula, left_col)
    print_nebulae(remaining)
    print("")
    print("")

    print("Nebulae Sum: " + str(get_nebulae_sum(remaining)))
    return

def test_copy_nebula():
    nebula = [
        [True, False, True],
        [False, True, False],
        [True, False, True]
    ]
    nebula_copy = get_copy_nebula(0, nebula)
    nebula_copy[1][1] = False
    print_nebula(nebula)
    print("")
    print_nebula(nebula_copy)
    return

def test_gas_count(num, nebula, row, col, expected):
    print("Gas Count Test " + str(num))
    print("Row: " + str(row))
    print("Col: " + str(col))
    print("Expected: " + str(expected))
    print("Result: " + str(get_gas_count(row,col,nebula)))
    print_nebula(nebula)
    print("")
    print("")
    
def test_gas_counts():
    nebula = [
            [False, False, False],
            [False, True, True],
            [True, True, True]
        ]
    test_gas_count(1, nebula, 0, 0, 1)
    test_gas_count(2, nebula, 0, 1, 2)
    test_gas_count(3, nebula, 1, 0, 3)
    test_gas_count(4, nebula, 1, 1, 4)
    return

nebula = [
            [True, False, True],
            [False, True, False],
            [True, False, True]
        ]

#test_copy_nebula()
#test_gas_counts()
#test_nebulae(1, nebula)
test_solutions()
