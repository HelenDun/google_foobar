
def solution(x, y):
    pair = [int(x), int(y)]
    if (pair[0] < pair[1]):
        pair = [pair[1], pair[0]]
    counter = 0

    while (pair[0] >= 1 and pair[1] >= 1):
        if (pair[0] == 1 and pair[1] == 1):
            return str(counter)
        elif (pair[0] == pair[1]):
            return "impossible"

        division = ((pair[0] - 1) // pair[1])
        counter += division

        temp = pair[0]
        pair[0] = pair[1]
        pair[1] = temp - pair[1] * division
        
    return "impossible"

def foo(n):
    pairs_old = set()
    pairs_old.add((1,1))
    pairs_new = set()
    result = 0
    while (result < n):
        result += 1
        for pair_old in pairs_old:
            pair_new1 = (pair_old[0] + pair_old[1], pair_old[1])
            pair_new2 = (pair_old[0], pair_old[1] + pair_old[0])
            pairs_new.add(pair_new1)
            pairs_new.add(pair_new2)
        pairs_old = pairs_new
        pairs_new = set()
    return pairs_old

def test(n):
    for i in range(0,n):
        pairs = foo(i)
        for pair in pairs:
            result = solution(str(pair[0]), str(pair[1]))
            if result != str(i):
                print(f"Pair: {pair}\tExpected: {i}\tResult: {result}")

test(4)
print(solution(2,2))
print(solution(3,3))
print(solution(4,4))
print(solution(2,4))