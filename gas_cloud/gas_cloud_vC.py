import time

'''

WARNING: This is not my code (except for the testing code). 
This is from Shrey Shah's article on her Google Foobar solutions, which I turned to in defeat.
https://pages.cs.wisc.edu/~shrey/2020/08/10/google-foobar.html

'''

def solution(g):
    transposed = tuple(zip(*g))
    preimgs = precol(transposed[0])
    precount = dict()
    for pair in preimgs:
        precount[pair[0]] = 1
    for col in transposed:
        preimgs = precol(col)
        count = dict()
        for pair in preimgs:
            if pair[0] not in precount: precount[pair[0]] = 0
            if pair[1] not in count: count[pair[1]] = 0
            count[pair[1]] += precount[pair[0]]
        precount = count
    return sum(precount.values())


def precol(col):
    possib = ((0, 0), (0, 1), (1, 0), (1, 1))
    curr = devol[col[0]]
    for i in range(1, len(col)):
        new = []
        for tes in curr:
            for comb in possib:
                if evol[(tes[i], comb)] == col[i]:
                    new.append(tes+(comb,))
        curr = tuple(new)
    bin_ret = [tuple(zip(*i)) for i in curr]
    return [tuple([bitlist(nu) for nu in possibl]) for possibl in bin_ret]

def bitlist(bitsl):
    out = 0
    for bit in bitsl:
        out = (out << 1) | bit
    return out

evol = {
            ((0, 0), (0, 0)): 0, 
            ((0, 0), (0, 1)): 1, 
            ((0, 0), (1, 0)): 1,
            ((0, 0), (1, 1)): 0, 
            ((0, 1), (0, 0)): 1, 
            ((0, 1), (0, 1)): 0,
            ((0, 1), (1, 0)): 0, 
            ((0, 1), (1, 1)): 0, 
            ((1, 0), (0, 0)): 1,
            ((1, 0), (0, 1)): 0, 
            ((1, 0), (1, 0)): 0, 
            ((1, 0), (1, 1)): 0,
            ((1, 1), (0, 0)): 0, 
            ((1, 1), (0, 1)): 0, 
            ((1, 1), (1, 0)): 0,
            ((1, 1), (1, 1)): 0
        }

devol = {
            0:(
                ((0, 0), (0, 0)), 
                ((0, 0), (1, 1)), 
                ((0, 1), (0, 1)),
                ((0, 1), (1, 0)), 
                ((0, 1), (1, 1)), 
                ((1, 0), (0, 1)),
                ((1, 0), (1, 0)), 
                ((1, 0), (1, 1)), 
                ((1, 1), (0, 0)),
                ((1, 1), (0, 1)), 
                ((1, 1), (1, 0)), 
                ((1, 1), (1, 1))
            ),
            1:(
                ((1, 0), (0, 0)), 
                ((0, 1), (0, 0)), 
                ((0, 0), (1, 0)),
                ((0, 0), (0, 1))
        )}





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
    print("VC Result: " + str(result))
    print("VC Time: " + str(stop-start))
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
        print("VC Result: " + str(result_s))
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


nebula = [
    [True, True, False, True, False, True, False, True, True, False],
    [True, True, False, False, False, False, True, True, True, False],
    [True, True, False, False, False, False, False, False, False, True],
    [False, True, False, False, False, False, True, True, False, False]
]
test_solution(1,nebula,11567)
#test_solutions()