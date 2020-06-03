from random import randint
from itertools import product

from robby import generate_plan, move, create_strategy, site_state, teleport

NUMBER_OF_GENES = 512
NUMBER_OF_STATES = 4
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
TELEPORT = 3

# CHARACTERS
CHARACTERS = {
    EMPTY: " ",
    CAN: "X",
    WALL: "|",
    TELEPORT: "T"
}

STATES = [EMPTY, CAN, WALL, TELEPORT]

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
    action = 0
    while 1:
        print("action", action)
        print_plan(plan, position)
        if "q" == input("q - exit"):
            break
        action += 1
        
        if site_state(position, plan) == 3:
            teleport(position, plan)

        sc, _ = move(plan, position, strategy)
        score += sc
        print("score:", score)

'''
Following naive strategy, Robby:
- picks up a can if he is currently on a position containing one
- moves to the position containing a can if his current position 
is empty and there is such neighbour position
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
    as Robby cannot stand on a wall or teleport.
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


    options = [EMPTY, WALL, TELEPORT]

    for situation in product(options, repeat=3):
        first, second, third = situation

        naive_individual[get_gene_index(EMPTY, EMPTY, first, second, third)] = RANDOM
        naive_individual[get_gene_index(EMPTY, first, second, EMPTY, third)] = RANDOM
        naive_individual[get_gene_index(EMPTY, first, second, third, EMPTY)] = RANDOM
        naive_individual[get_gene_index(EMPTY, first, EMPTY, second, third)] = RANDOM
    
    return naive_individual


'''
Following this naive strategy, Robby will keep the naive behaviour except:
- he will prefer teleport if there is no can in neighbourhood
'''
def create_naive_strategy_prefering_teleports():
    naive_individual = create_naive_strategy()

    # RULE THREE: If there is not a can nearby, prefer teleport is there is one
    options = [EMPTY, WALL, TELEPORT]

    for situation in product(options, repeat=3):
        first, second, third = situation

        naive_individual[get_gene_index(EMPTY, TELEPORT, first, second, third)] = NORTH
        naive_individual[get_gene_index(EMPTY, first, TELEPORT, second, third)] = SOUTH
        naive_individual[get_gene_index(EMPTY, first, second, TELEPORT, third)] = EAST
        naive_individual[get_gene_index(EMPTY, first, second, third, TELEPORT)] = WEST

    return naive_individual

'''
Following this strategy, Robby prefers teleports even if there is a can in neighbourhood.
'''
def create_naive_strategy_prefering_teleports_for_any_price():
    naive_individual = create_naive_strategy()

    # RULE FOUR: Prefer teleport
    for situation in product(STATES, repeat=3):
        first, second, third = situation

        naive_individual[get_gene_index(EMPTY, TELEPORT, first, second, third)] = NORTH
        naive_individual[get_gene_index(EMPTY, first, TELEPORT, second, third)] = SOUTH
        naive_individual[get_gene_index(EMPTY, first, second, TELEPORT, third)] = EAST
        naive_individual[get_gene_index(EMPTY, first, second, third, TELEPORT)] = WEST

    return naive_individual

if __name__ == '__main__':
    naive_individual = create_naive_strategy_prefering_teleports_for_any_price()
    show_strategy(generate_plan(), naive_individual)