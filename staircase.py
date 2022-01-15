def solution(n):
    dynamic_dictionary = {}
    num_steps = 2
    num_designs = 0
    min_n = 3

    # go through all possible numbers of steps for the staircases
    while (n >= min_n):
        num_designs += recurse(1, num_steps, n, dynamic_dictionary)
        
        num_steps += 1
        min_n = (num_steps * (num_steps + 1)) / 2
    
    return num_designs

# Recurse finds all possible combinations of num_var variable
# where each consecutive pair of variables (a,b) are defined, a < b
# formula: x1 + x2 + x3 = t
# x1 = 1
    # formula: x2 + x3 = t - 1
    # x2 = 1, x3 = (t - 2)
    # x2 = 2, x3 = (t - 3)
    # ...
# x1 = 2
    # formula: x2 + x3 = t - 2
    # x2 = 1, x3 = (t - 3)
    # x2 = 2, x3 = (t - 4)
    # ...
# ...
def recurse(init_var, num_var, total_var, dyn_dict):
    # if two variables, use summation
    if (num_var == 2):
        return (total_var - 1) // 2 - (init_var - 1)
    
    # check if this has already been calculated
    key = f'{init_var}|{num_var}|{total_var}'
    if key in dyn_dict:
        return dyn_dict[key]

    num_designs = 0
    last_var = 0 
    min_total_var = 0
    while (total_var >= min_total_var):
        num_designs += recurse(init_var + 1, num_var - 1, total_var - init_var, dyn_dict)
    
        # let init_var = 2
        # init_var + 3 + ... + last_var = min_total_var
        init_var += 1
        last_var = init_var + num_var - 1
        min_total_var = ((last_var + init_var) * (last_var - init_var + 1)) / 2
    
    dyn_dict[key] = num_designs
    return num_designs


for i in range(3, 21):
    print(f'Test {i} | Output: {solution(i)}')

print(f'Test {200} | Output: {solution(200)}')

string = "ECS"
print(string*3)