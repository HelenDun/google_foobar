import math
AXES = 2
X = 0
Y = 1
HORIZONTAL = 1
VERTICAL = 0
BOTH = -1
IS_PRINT = False

def solution(dimensions, your_position, trainer_position, max_distance):
    # get every possible reflection of the room within the maximum distance
    # check each reflected room to see if the trainer can be hit
    vectors = 0
    max_rooms_x = (max_distance + dimensions[X] - 1) // dimensions[X]
    max_rooms_y = (max_distance + dimensions[Y] - 1) // dimensions[Y]
    for i in range(-1 * max_rooms_x, max_rooms_x + 1):
        for j in range(-1 * max_rooms_y, max_rooms_y + 1):
            vectors += (None != get_vector([i,j], dimensions, your_position, trainer_position, max_distance))
    return vectors

# returns a vector of the bullet path from you to a trainer that bounces on the specified walls
# if the vector does not exist, returns None
def get_vector(room, dimensions, your_position, trainer_position, max_distance):

    # check whether the room is in any negative directions
    is_axis_negative = []
    for axis in range(0, AXES):
        is_axis_negative.append(room[axis] < 0)

    # get the position of the target
    target = trainer_position
    for axis in range(0, AXES):
        for i in range(0, abs(room[axis])):
            line = (i + 1) * dimensions[axis] * (not is_axis_negative[axis]) - i * dimensions[axis] * is_axis_negative[axis]
            target = get_reflection(target, line, axis)

    # check that the distance the beam travels is lethal
    vector = get_difference(your_position, target)
    if IS_PRINT:
        print("")
        print("is negative:\t\t" + str(is_axis_negative))
        print("target:\t\t\t" + str(target))
        print("vector:\t\t\t" + str(vector))
        print("your position:\t" + str(your_position))
        print("trainer position:\t" + str(trainer_position))
    if not is_shorter_or_equal_distance(vector, max_distance):
        return None
    elif is_equal_vector(target, trainer_position):
        return vector

    # default declarations
    your_reflection = your_position
    trainer_reflection = trainer_position
    walls = []
    for axis in range(0, AXES):
        walls.append(dimensions[axis] * (vector[axis] >= 0))

    # check that the beam doesn't hit unwanted targets
    is_not_hitting = not is_hitting(your_position, vector, trainer_reflection)
    while is_not_hitting and not is_equal_vector(target, trainer_reflection):
        collision = get_next_collision(your_position, vector, walls[Y], walls[X])

        # flip horizontally over the vertical wall
        if collision == HORIZONTAL or collision == BOTH:
            your_reflection = get_reflection(your_reflection, walls[X], X)
            trainer_reflection = get_reflection(trainer_reflection, walls[X], X)
            walls[X] += dimensions[X] * (vector[X] >= 0) - dimensions[X] * (vector[X] < 0)

        # flip vertically over the horizontal wall
        if collision == VERTICAL or collision == BOTH:
            your_reflection = get_reflection(your_reflection, walls[Y], Y)
            trainer_reflection = get_reflection(trainer_reflection, walls[Y], Y)
            walls[Y] += dimensions[Y] * (vector[Y] >= 0) - dimensions[Y] * (vector[Y] < 0)

        # check if the reflections in the room are hit
        is_not_hitting = is_equal_vector(target, trainer_reflection)
        is_not_hitting = is_not_hitting or not is_hitting(your_position, vector, trainer_reflection)
        is_not_hitting = is_not_hitting and not is_hitting(your_position, vector, your_reflection)

        if IS_PRINT:
            print("collision:\t\t\t" + str(collision))
            print("your reflection:\t" + str(your_reflection))
            print("trainer reflection:\t" + str(trainer_reflection))
            print("is not hitting:\t\t" + str(is_not_hitting))
    
    # if nothing went wrong then continue
    if is_not_hitting:
        return vector
    return None

# return the coordinate after being reflected horizontally or vertically over the vertical or horizontal line
# Note. HORIZONTAL means X-coordinate is changed/reflected over a vertical line
def get_reflection(position, line, line_axis):
    reflection = position[:]
    reflection[line_axis] = (2 * line - position[line_axis])
    return reflection

# return the vector to get from position1 to position2
def get_difference(position1, position2):
    return [position2[X] - position1[X], position2[Y] - position1[Y]]

# return whether the vectors are equal
def is_equal_vector(vector1, vector2):
    for axis in range(0, AXES):
        if vector1[axis] != vector2[axis]:
            return False
    return True

# return the distance the vector goes
def is_shorter_or_equal_distance(vector, max_distance):
    return vector[X] * vector[X] + vector[Y] * vector[Y] <= max_distance * max_distance

# return whether the reflection will be hit by the vector
def is_hitting(position, vector, reflection):
    difference = get_difference(position, reflection)
    return is_overlapping(difference, vector)

# return whether vector2 overlaps vector1 (aka. v2 is a multiple of v1)
def is_overlapping(vector1, vector2):
    return vector1[X] * vector2[Y] == vector1[Y] * vector2[X]

# return which wall the vector will collide with next
def get_next_collision(position, vector, horizontal_line, vertical_line):
    # get the y coordinate of the collision
    collision = vertical_line * vector[Y] + position[Y] * vector[X] - vector[Y] * position[X]
    line = horizontal_line * vector[X]

    # if vector[X] is negative and reversed the < sign, then reverse it back
    negative = (vector[X] < 0)
    collision = collision * (not negative) - collision * negative
    line = line * (not negative) - line * negative

    # check if the y coordinate of the collision is within the bounds of the line
    is_both = (collision == line)
    is_horizontal = (vector[Y] >= 0 and collision < line) or (vector[Y] < 0 and collision > line)
    is_vertical = not is_horizontal and not is_both
    return HORIZONTAL * is_horizontal + VERTICAL * is_vertical + BOTH * is_both

def test_get_vector(room_reflection, expected):
    print("")
    print("-- Room Reflection: " + str(room_reflection) + " --")
    beam = get_vector(room_reflection, [3,2], [1,1], [2,1], 4)
    print("")
    print("Result: " + str(beam))
    print("Expected: " + str(expected))
    print("")

def test_get_vectors():
    tests = [
        [(1,0), None],
        [(-1,0), None],
        [(0,0), [1,0]],
        [(0,1), [1,2]],
        [(0,-1), [1,-2]],
        [(1,1), [3,2]],
        [(-1,1), [-3,2]],
        [(1,-1), [3,-2]],
        [(-1,-1), [-3,-2]],
        [(0,2), None],
        [(0,-2), None],
        [(1,2), None],
        [(1,-2), None],
    ]
    print("-- Testing get_beam() --")
    for test in tests:
        test_get_vector(test[0], test[1])
    print("")

def test_solution(dimensions, your_position, trainer_position, max_distance, expected):
    print("-- Testing solution() --")
    print("Dimensions:\t\t\t" + str(dimensions))
    print("Your Position:\t\t" + str(your_position))
    print("Trainer Position:\t" + str(trainer_position))
    print("Max Distance:\t\t" + str(max_distance))
    result = solution(dimensions, your_position, trainer_position, max_distance)
    print("- \tExpected:\t" + str(expected))
    print("- \tResult: \t" + str(result))
    print("")

def test_solutions():
    tests = [
        [[3,2], [1,1], [2,1], 4, 7],
        [[300,275], [150,150], [185, 100], 500, 9]
    ]

    for test in tests:
        test_solution(test[0], test[1], test[2], test[3], test[4])

def test_get_next_collision():
    tests = [
        [[1,1], [3,-4], 0, 3, VERTICAL],
        [[1,1], [3,-4], -2, 3, HORIZONTAL],
        [[1,1], [3,-4], -2, 6, VERTICAL],
        [[150,150], [-335, -50], 0, 0, HORIZONTAL]
    ]

    print("-- Testing is_next_horizontal() --")
    for test in tests:
        result = get_next_collision(test[0], test[1], test[2], test[3])
        print("Wall X: " + str(test[2]) + "\tWall Y: " + str(test[3]) + "\tExpected: " + str(test[4]) + "\tResult: " + str(result))
    print("")



test_get_next_collision()
test_get_vectors()
test_solutions()

#test_get_beam((1,1), [3,2])
#test_solution([300,275], [150,150], [185, 100], 500, 9)