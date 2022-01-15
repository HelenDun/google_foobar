
def solution(num_bunnies, num_required):
    keyrings = [] # list of each bunny minion's keyring
    if num_required == 1:
        for i in range(0, num_bunnies):
            keyrings.append([0])
    else:
        # initialize each keyring
        for i in range(0, num_bunnies):
            keyrings.append([])
        
        if num_required == 0:
            return keyrings

        keyrings_missing_keys = recursive_combinations(num_required - 1, 0, num_bunnies, [])
        keyrings_missing_keys.reverse()

        for i in range(0, len(keyrings_missing_keys)):
            keyrings_missing_key = keyrings_missing_keys[i]

            if (len(keyrings_missing_key) > num_bunnies):
                print("!!Error: Number of keyrings > number of bunnies!!")
                print(keyrings_missing_key)
                exit(1)
            for keyring_index in range(0, num_bunnies):
                # if the key is not missing, add it to that bunny's keyring
                if (keyring_index >= len(keyrings_missing_key) or keyrings_missing_key[keyring_index] == False):
                    keyrings[keyring_index].append(i)

    return keyrings

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

def print_stat(missing_num, bunnies_index, bunnies_num, combination):
    print("missing_num:\t" + str(missing_num))
    print("bunnies_index:\t" + str(bunnies_index))
    print("bunnies_num:\t" + str(bunnies_num))
    print("combination:\t" + str(combination))

def test_correct(solution, num_required):
    if num_required == 0 or num_required == 1:
        return True

    num_bunnies = len(solution)
    max_num = 0
    for s in solution:
        for value in s:
            if (value > max_num):
                max_num = value

    # check that a group of (num_required - 1) doesn't create viable combinations
    for i in range(1, num_required):

        # get all possible i-length combinations of the bunny keyrings
        combinations = recursive_combinations(i, 0, num_bunnies, [])

        # check each i-length combination of bunny keyrings
        for combination in combinations:

            # add keys from relevant keyrings to the set
            solution_set = []
            for j in range(0, len(combination)):
                if (combination[j] == True):
                    solution_set = solution_set + solution[j]
            
            is_solution = True
            for j in range(0, max_num + 1):
                if (j not in solution_set):
                    is_solution = False
                    break
            if is_solution:
                print("!!Error: solution works for (num_required - 1)!!")
                return False


    # get and check all possible num_required-length combinations of the bunny keyrings
    combinations = recursive_combinations(num_required, 0, num_bunnies, [])
    for combination in combinations:

        # add keys from relevant keyrings to the set
        solution_set = []
        for j in range(0, len(combination)):
            if (combination[j] == True):
                solution_set = solution_set + solution[j]
        
        is_solution = True
        for j in range(0, max_num + 1):
            if (j not in solution_set):
                is_solution = False
                break
        if not is_solution:
            print("!!Error: solution does not work for combination!!")
            print(solution)
            print(combination)
            return False

    return True

def test_solution(num, num_bunnies, num_required, expected):
    print("-- Solution Test " + str(num) + " --")
    if (len(expected) != num_bunnies):
        print("!!Error: Expected result does not match number of bunnies!!")
        exit(1)
    elif (num_bunnies < num_required):
        print("!!Error: More consoles than bunnies!!")
        exit(1)
    print("Bunnies:\t" + str(num_bunnies))
    print("Required:\t" + str(num_required))
    print("Testing...")
    result = solution(num_bunnies, num_required)
    print("Expected:\t" + str(expected))
    print("Result:\t\t" + str(result))
    print("Correct:\t" + str(test_correct(result, num_required)))
    print("")
    return

def print_bunny(nb):
    print("\nTESTING BUNNIES: " + str(nb))

def tests_solution():
    empty = []
    nb = 1
    print_bunny(nb)
    test_solution(0, nb, 0, [empty])
    test_solution(1, nb, 1, [[0]])

    nb = 2
    print_bunny(nb)
    test_solution(2, nb, 0, [empty, empty] )
    test_solution(3, nb, 1, [[0], [0]] )
    test_solution(4, nb, 2, [[0], [1]] )

    nb = 3
    print_bunny(nb)
    test_solution(5, nb, 0, [empty, empty, empty] )
    test_solution(6, nb, 1, [[0], [0], [0]] )
    test_solution(7, nb, 2, [[0,1], [0,2], [1,2]] )
    test_solution(8, nb, 3, [[0], [1], [2]] )

    nb = 4
    print_bunny(nb)
    test_solution(9, nb, 0, [empty, empty, empty, empty] )
    test_solution(10, nb, 1, [[0], [0], [0], [0]] )
    test_solution(11, nb, 2, [[0,1,2], [0,1,3], [0,2,3], [1,2,3]] )
    test_solution(12, nb, 3, [[0,1,2], [0,3,4], [1,3,5], [2,4,5]] )
    test_solution(13, nb, 4, [[0], [1], [2], [3]] )

    nb = 5
    print_bunny(nb)
    test_solution(14, nb, 0, [empty, empty, empty, empty, empty] )
    test_solution(15, nb, 1, [[0], [0], [0], [0], [0]] )
    test_solution(16, nb, 2, [[0,1,2,3], [0,1,2,4], [0,1,3,4], [0,2,3,4], [1,2,3,4]] )
    test_solution(17, nb, 3, [[0,1,2,5,7,9], [0,1,3,6,8,9], [0,3,4,5,7,8], [1,2,4,5,6,8], [2,3,4,6,7,9]] )
    #test_solution(18, nb, 4, [[0,1], [1,2], [2,3], [3,4], [0,4]] )
    test_solution(19, nb, 5, [[0], [1], [2], [3], [4]] )

    nb = 6
    print_bunny(nb)
    test_solution(20, nb, 0, [empty, empty, empty, empty, empty, empty] )
    test_solution(21, nb, 1, [[0], [0], [0], [0], [0], [0]] )
    test_solution(22, nb, 2, [[0,1,2,3,4], [0,1,2,3,5], [0,1,2,4,5], [0,1,3,4,5], [0,2,3,4,5], [1,2,3,4,5]] )
    test_solution(23, nb, 3, [
        [0,1,2,3,5,6,7,9,10,11,13], 
        [0,1,2,4,5,6,8,9,10,12,14], 
        [0,1,3,4,5,7,8,9,11,12,15], 
        [0,2,3,4,6,7,8,9,13,14,15], 
        [1,2,3,4,9,10,11,12,13,14,15], 
        [5,6,7,8,9,10,11,12,13,14,15]
    ])
    #test_solution(24, nb, 4, [[0,1], [1,2], [2,3], [3,4], [0,4], []] )
    #test_solution(25, nb, 5, [[0,1], [1,2], [2,3], [3,4], [4,5], [0,5]] )
    test_solution(26, nb, 6, [[0], [1], [2], [3], [4], [5]] )
    return

def test_recursive_combinations(num, nb, r):
    combinations = recursive_combinations(r - 1, 0, nb, [])
    print("-- Recursive Combinations Test " + str(num) + " --")
    print("num_bunnies:\t" + str(nb))
    print("num_required:\t" + str(r))
    print("combinations:\t" + str(combinations))
    print("")
    return

def tests_recursive_combinations():
    nb = 2
    print_bunny(nb)
    test_recursive_combinations(1, nb, 2) #[[True,False], [False,True]]

    nb = 3
    print_bunny(nb)
    test_recursive_combinations(2, nb, 2)
    test_recursive_combinations(3, nb, 3)

    nb = 4
    print_bunny(nb)
    test_recursive_combinations(4, nb, 2)
    test_recursive_combinations(5, nb, 3)
    test_recursive_combinations(6, nb, 4)

    nb = 5
    print_bunny(nb)
    test_recursive_combinations(7, nb, 2)
    test_recursive_combinations(8, nb, 3)
    test_recursive_combinations(9, nb, 4)
    test_recursive_combinations(10, nb, 5)

    nb = 6
    print_bunny(nb)
    test_recursive_combinations(11, nb, 2)
    test_recursive_combinations(12, nb, 3)
    test_recursive_combinations(13, nb, 4)
    test_recursive_combinations(14, nb, 5)
    test_recursive_combinations(15, nb, 6)
    return

tests_recursive_combinations()

#tests_solution()
#print(test_correct([[0,1], [0,3], [1,2]], 2))