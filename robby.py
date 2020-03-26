from random import randint, random, sample

number_of_genes = 243
max_mutations = 6
tournament_sample = 25
population_size = 200
rounds = 100
mutation_probability = 0.2



def create_strategy():
    individual = [randint(0, 6) for _ in range(number_of_genes)] # random action for every situation
    return individual

def new_individual(): # streatgy + fitness
	individual = create_strategy()
	score = fitness(individual)
	return individual, score

def crossover(parent_1, parent_2):
    crossover_index = randint(1, number_of_genes)
    child_1a = parent_1[:crossover_index]
    child_1b = parent_2[crossover_index:]
    child_1 = child_1a + child_1b

    child_2a = parent_2[crossover_index:]
    child_2b = parent_1[:crossover_index]
    child_2 = child_2a + child_2b

    return child_1, child_2



def mutate(individual):
    number_of_mutations = randint(1, max_mutations) # choose random number of mutations
    for i in range(number_of_mutations):
        individual[randint(0, max_mutations)] = randint(0, 6) 



# generates plan with random cans 
def generate_plan():
    return [[randint(0, 1) for _ in range(10)] for _ in range(10)] 

def site_state(coordinates, plan):
    if 10 > coordinates[0] >= 0 and 10 > coordinates[1] >= 0:
        return plan[coordinates[0]][coordinates[1]]

    return 2 # wall

def move(plan, position, strategy):
    up = site_state((position[0] - 1, position[1]), plan)
    down = site_state((position[0] - 1, position[1]), plan)
    right = site_state((position[0], position[1] - 1), plan)
    left = site_state((position[0], position[1] + 1), plan)
    current = site_state((position[0], position[1]), plan)
    gene_index = up * 81 + down * 27 +  right * 9 + left * 3 + current
    action = strategy[gene_index]

    if action == 6: # Robby moves randomly 
        action = randint(0, 3)


    if action == 0:  # Robby goes up
        if up == 2: # wall
            return -5

        position[0] -= 1
        return 0

    if action == 1: # Robby goes down
        if down == 2: # wall
            return -5

        position[0] += 1
        return 0

    if action == 2: # Robby goes right
        if right == 2: # wall
            return -5

        position[1] -= 1
        return 0

    if action == 3: # Robby goes left
        if left == 2: # wall
            return -5

        position[1] += 1
        return 0

    if action == 4: # Robby stays
        return 0

    if action == 5: # Robby picks can

        if current == 1:
            plan[position[0]][position[1]] = 0
            return 10
        return -1 # no can

    	




def fitness (strategy):
    score = 0

    for i in range(10):
        plan = generate_plan()
        position = [0, 0]
        for i in range(200):
            score += move(plan, position, strategy)
    return score/10


def tournament_selection(population):
	options = sample(population, tournament_sample)
	options.sort(key=lambda x: x[1], reverse=True)
	return options[0], options[1]

def new_population(population):
	population.sort(key=lambda x: x[1], reverse=True)
	print(population[0][1])
	new_population = []

	while (population_size > len(new_population)):
		parent1, parent2 = tournament_selection(population)
		child1, child2 = crossover(parent1[0], parent2[0])

		if random() < mutation_probability:
			mutate(child1)

		if random() < mutation_probability:
			mutate(child2)
		new_population.append((child1, fitness(child1)))
		new_population.append((child2, fitness(child2)))

	return new_population


def run():
    population = [new_individual() for _ in range(population_size)]
    population.sort(key=lambda x: x[1], reverse=True)
    print(generate_plan())
    print([population[i][1] for i in range(population_size)])
    for _ in range(rounds):
        population = new_population(population)
    population.sort(key=lambda x: x[1], reverse=True)
    print(population[0])
    print(generate_plan())

run()


