from random import randint
from itertools import product

from robby import create_strategy, generate_plan, move

NUMBER_OF_GENES = 1250
NUMBER_OF_STATES = 5
NUMBER_OF_ACTIONS = 100
BOARD_SIZE = 10

# ACTIONS
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
STAY = 4
PICK_UP = 5
RANDOM = 6

ACTIONS = [NORTH, SOUTH, EAST, WEST, STAY, PICK_UP, RANDOM]

# STATES
EMPTY = 0
CAN = 1
WALL = 2
PIT = 3
TELEPORT = 4

# CHARACTERS
CHARACTERS = {
    EMPTY: " ",
    CAN: "X",
    WALL: "|",
    PIT: "O",
    TELEPORT: "T"
}

STATES = [EMPTY, CAN, WALL, PIT, TELEPORT]

def get_gene_index(current, north, south, east, west):
    return current * NUMBER_OF_STATES ** 4 + \
        north * NUMBER_OF_STATES ** 3 +  \
        south * NUMBER_OF_STATES ** 2 + \
        east * NUMBER_OF_STATES + \
        west
        
def print_plan(plan, position):
	print("".join(["-" for _ in range(BOARD_SIZE + 2)]))
	for row in range(BOARD_SIZE):
		print("|", end="")
		for col in range(BOARD_SIZE):
			if row == position[0] and col == position[1]: # robot
				print("R", end="")
			else:
			    print(CHARACTERS.get(plan[row][col], "U"), end="")
		print("|")
	print("".join(["-" for _ in range(BOARD_SIZE + 2)]))

def show_strategy(plan, strategy):
    score = 0
    position = [0, 0]
    print(len(strategy))
    for step in range(NUMBER_OF_ACTIONS):
        print("Action: ", step)
        print_plan(plan, position)
        actual_score, _ = move(plan, position, strategy)
        score += actual_score
        print("Score: ", score)

'''
Following naive strategy, Robby:
- picks up a can if he is currently on a position containing one
- moves to the position containing a can if his current position 
is empty and there is such neighbour position
- prefers going to an empty position before anything except a cell
with a can
- otherwise acts randomly
'''
def create_naive_strategy():
    naive_individual = create_strategy()

    # RULE ONE: If current position is a can

    # We generate every possible situation of neighbourhood cells
    # considering all of the states
    for situation in product(STATES, repeat=4):
        north, south, east, west = situation
        naive_individual[get_gene_index(CAN, north, south, east, west)] = PICK_UP

    '''
    For the rule two and three, current site is automatically empty,
    as Robby cannot stand on a wall or teleport and if he stands inside
    a pit, he cannot move for the rest of the session.
    '''

    # RULE TWO: If there is a can in neighbourhood

    # We determine a position with a can, current is EMPTY,
    # the rest can be in any state so we consider again all
    # of the states
    for situation in product(STATES, repeat=3):
        first, second, third = situation
        
        naive_individual[get_gene_index(EMPTY, CAN, first, second, third)] = NORTH
        naive_individual[get_gene_index(EMPTY, first, CAN, second, third)] = SOUTH
        naive_individual[get_gene_index(EMPTY, first, second, CAN, third)] = EAST
        naive_individual[get_gene_index(EMPTY, first, second, third, CAN)] = WEST


    # RULE THREE: Avoiding walls, pits and teleports if there
    # is an empty neighbour

    '''
    If there are several empty neighbour sites, we just define
    one of them.
    '''
    
    options = [EMPTY, WALL, TELEPORT, PIT]

    for situation in product(options, repeat=3):
        first, second, third = situation

        naive_individual[get_gene_index(EMPTY, EMPTY, first, second, third)] = NORTH
        naive_individual[get_gene_index(EMPTY, first, second, EMPTY, third)] = EAST
        naive_individual[get_gene_index(EMPTY, first, second, third, EMPTY)] = WEST
        naive_individual[get_gene_index(EMPTY, first, EMPTY, second, third)] = SOUTH
    
    return naive_individual


if __name__ == '__main__':
    show_strategy(generate_plan(), create_naive_strategy())