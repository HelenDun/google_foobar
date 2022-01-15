def solution0(n):
    number_operations = 0
    n = int(n)

    while (n > 1):
        # do all possible divisions by 2
        while (n % 2 == 0):
            number_operations += 1
            n = n // 2
        
        upper_bound = 2
        upper_power = 1
        while (upper_bound < n):
            upper_bound *= 2
            upper_power += 1
        lower_bound = upper_bound // 2
        lower_power = upper_power - 1
    
        upper_diff = upper_bound - n
        lower_diff = n - lower_bound

        if (upper_diff != 1 and lower_diff != 1):
            number_operations += 1
            n = (n - 1)
        else:
            boool = upper_diff < lower_diff
            number_operations += (upper_diff + upper_power) * boool
            number_operations += (lower_diff + lower_power) * (not boool)
            break
    
    return number_operations


def solution(n):
    n = int(n)
    operations = 0

    # first, do all possible divisions by 2
    while (n % 2 == 0):
        n = n // 2
        operations += 1

    while (n > 1):

        # find how many factors of 2 are in (n + 1) and (n - 1)
        upper = (n + 1) // 2
        lower = (n - 1) // 2
        #print(f"n: {n}\toperations: {operations}\tupper: {upper}\tlower: {lower}")

        upper_factor = 1
        lower_factor = 1

        while (upper % 2 == 0):
            upper = upper // 2
            upper_factor += 1

        while (lower % 2 == 0):
            lower = lower // 2
            lower_factor += 1

        # go with the operation that divides by 2 more
        boolean = (upper_factor > lower_factor) and (lower != 1)
        n = upper * boolean + lower * (not boolean)
        operations += upper_factor * boolean + lower_factor * (not boolean) + 1
    return operations





def test(k):
    for i in range(1,k+1):
        print(f"Test {i}: {solution(i)}")

test(100)
number = "123115922 1795514959 73383410176342643722 3345572556 8287960586 4838806293 6596196250 0430320625 03843925468550638441 0696515628 7951749387 6341125510 8928459554 1103692716 52877487631164170092 9986988023 1972422245 8109987258 0798960693 5217786073 96791006450968430359 0096132957 2590551421 6842343121 6909162902 3655876789 0728449777"
number = number.replace(' ', '')
print(f"Test {number}:\n{solution(number)}")
#print(solution(23))