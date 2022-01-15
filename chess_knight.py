def solution(src, dest):
    # turn src and dest into [x, y]
    x = (src % 8)
    y = (src - x) // 8
    src = [x,y]
    
    x = (dest % 8)
    y = (dest - x) // 8
    dest = [x,y]
    
    diff = [abs(dest[0] - src[0]), abs(dest[1] - src[1])]
    if (diff[0] == 0 and diff[1] == 0):
        return 0
    
    vectors = [[1,2],[2,1],[-1,2],[-2,1]]
    old_calculations = [diff]
    next_calculations = []
    num_steps = 0
    
    # breadth-first search the possible routes of vector combinations
    # the first route found will be of the minimum number of steps
    while (True):
        num_steps += 1
        for calc in old_calculations:
            for vect in vectors:
                pos = [calc[0] + vect[0], calc[1] + vect[1]]
                if (pos[0] == 0 and pos[1] == 0):
                    return num_steps
                    
                neg = [calc[0] - vect[0], calc[1] - vect[1]]
                if (neg[0] == 0 and neg[1] == 0):
                    return num_steps
                
                if  (pos not in next_calculations and (pos[0] <= diff[0] or pos[1] <= diff[1])):
                    next_calculations.append(pos)
                if  (neg not in next_calculations and (neg[0] >= 0 or neg[1] >= 0)):
                    next_calculations.append(neg)
            # end of vector for-loop
        # end of calculations for-loop
        old_calculations = next_calculations
        next_calculations = []
    
    return -1

def test(expected, output, number):
    print(f'\n----- Test {number} -----\n  Expected: {expected}\n  Output: {output}')

def coordinates(x, y):
    return x + 8 * y


print('TESTING')
test(3, solution(coordinates(1,1), coordinates(0,1)), 'A')
test(3, solution(coordinates(1,1), coordinates(1,0)), 'B')
test(2, solution(coordinates(2,6), coordinates(0,2)), 'C')
test(2, solution(coordinates(0,6), coordinates(0,2)), 'D')
test(6, solution(coordinates(0,0), coordinates(7,7)), 'E')
