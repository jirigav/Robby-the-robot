from random import randint, random, sample, choices, choice

number_of_genes = 512

mutation_probability = 0.4

# number of mutated genes
number_of_mutations = 5

population_size = 200

number_of_generations = 1000

# number of actions performed on a plan 
number_of_actions = 200

number_of_plans = 100

# probability of can to be placed on a certain spot
can_probability = 0.5


#tournament selection sample size
tournament_sample = 50

def create_strategy():
    individual = [randint(0, 6) for _ in range(number_of_genes)] # random action for every situation
    return individual

def new_individual(): # streatgy + fitness
	individual = create_strategy()
	score = fitness(individual)
	return individual, score

def crossover(parent1, parent2):
    crossover_index = randint(0, number_of_genes - 1)
    child1a = parent1[:crossover_index]
    child1b = parent2[crossover_index:]
    child1 = child1a + child1b

    child2a = parent2[:crossover_index]
    child2b = parent1[crossover_index:]
    child2 = child2a + child2b

    return child1, child2



def mutate(individual):
    for i in range(number_of_mutations):
        individual[randint(0, number_of_genes - 1)] = randint(0, 6) 



def distribute_cans_to_clusters():
    plan = [[0 for _ in range(10)] for _ in range(10)]

    # create four clusters
    for i in range(2):
        shift_col = i * 5
        for j in range(2):
            shift_row = j * 5
            # "cluster center"
            c1, c2 = (randint(1 + shift_row, 3 + shift_row), randint(1 + shift_col, 3 + shift_col))

            # von Neumann's neighbourhood
            plan[c1][c2] = 1
            plan[c1 - 1][c2] = 1
            plan[c1 + 1][c2] = 1
            plan[c1][c2 - 1] = 1
            plan[c1][c2 + 1] = 1

    return plan
        

def distribute_cans_randomly():
    return [[1 if random() > (1 - can_probability) else 0 for _ in range(10)] for _ in range(10)] 

# create_plan_with_cans = distribute_cans_randomly()
create_plan_with_cans = distribute_cans_randomly


def generate_plan():
    plan = create_plan_with_cans() 
    i = 0
    while i < 5: #walls
        coordinates = (randint(0, 9), randint(0, 9))
        if coordinates in {(0, 0), (0, 9), (9, 0), (9, 9)}:
            continue
        plan[coordinates[0]][coordinates[1]] = 2
        i += 1
   
    plan[randint(0, 9)][randint(0, 9)] = 3
    plan[randint(0, 9)][randint(0, 9)] = 3

    return plan

# returns 2 if wall, 1 if can, 3 if teleport, 0 otherwise 
def site_state(coordinates, plan):
    if 10 > coordinates[0] >= 0 and 10 > coordinates[1] >= 0:
        return plan[coordinates[0]][coordinates[1]]

    return 2 # wall

def move(plan, position, strategy):
    north = site_state((position[0] - 1, position[1]), plan)
    south = site_state((position[0] + 1, position[1]), plan)
    east = site_state((position[0], position[1] + 1), plan)
    west = site_state((position[0], position[1] - 1), plan)
    current = site_state((position[0], position[1]), plan)
    gene_index = current * 256 + north * 64 +  south * 16 + east * 4 + west
    action = strategy[gene_index]
    random_action = False 
    if action == 6: # Robby moves randomly 
        action = randint(0, 3)
        random_action = True

    if action == 0:  # Robby goes north
        if north == 2: # wall
            return -5, (not random_action)

        position[0] -= 1
        return 0, False

    if action == 1: # Robby goes south
        if south == 2: # wall
            return -5, (not random_action)

        position[0] += 1
        return 0, False

    if action == 2: # Robby goes east
        if east == 2: # wall
            return -5, (not random_action)

        position[1] += 1
        return 0, False

    if action == 3: # Robby goes west
        if west == 2: # wall
            return -5, (not random_action)

        position[1] -= 1
        return 0, False

    if action == 5: # Robby picks can

        if current == 1:
            plan[position[0]][position[1]] = 0
            return 10, False
        return -1, True # no can


    return 0, True # action 4, Robby stays
    	


def teleport(position, plan):
	while site_state(position, plan) == 3 or site_state(position, plan) == 2:
		position[0] = randint(0, 9)
		position[1] = randint(0, 9)
	

def fitness (strategy):
    score = 0

    for i in range(number_of_plans):
        plan = generate_plan()
        position = choice([[0, 0], [0, 9], [9, 0], [9, 9]])
        for i in range(number_of_actions):
        	
            if site_state(position, plan) == 3: # teleport
                teleport(position, plan)


            round_score, stucked = move(plan, position, strategy)
            score += round_score


            if stucked:
            	score += (number_of_actions - i - 1)*round_score #skip repetitive actions
            	break


    return score/number_of_plans


def tournament_selection(population):
	options = sample(population, tournament_sample)
	options.sort(key=lambda x: x[1], reverse=True)
	return options[0], options[1]



def new_population(population):
	

    new_population = []

    while (population_size > len(new_population)):
        
        parent1, parent2 = tournament_selection(population) # choose parents

        child1, child2 = crossover(parent1[0], parent2[0]) 

        if random() < mutation_probability:
            mutate(child1)

        if random() < mutation_probability:
            mutate(child2)

        new_population.append((child1, fitness(child1)))
        new_population.append((child2, fitness(child2)))
		

    return new_population

def print_plan(plan, position):
	print("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛")
	for i in range(10):
		print("⬛", end="")
		for j in range(10):
			if i == position[0] and j == position[1]: # robot
				print("🤖", end="")
			else:
			    if plan[i][j] == 0: # empty
				    print("⬜", end="")
			    if plan[i][j] == 1: # can
				    print("🥫", end="")
			    if plan[i][j] == 2: # wall
			        print("⬛", end="")
			    if plan[i][j] == 3: # teleport
			        print("🌀", end="")
		print("⬛")
	print("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛")

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


def run():

    population = [new_individual() for _ in range(population_size)] # first population

    for i in range(number_of_generations):
        population.sort(key=lambda x: x[1], reverse=True)
        population = new_population(population)



    population.sort(key=lambda x: x[1], reverse=True)
    show_strategy(generate_plan(), population[0][0])
    return population
    


if __name__ == "__main__":
    run()
