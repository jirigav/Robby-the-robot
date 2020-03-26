from random import randint

number_of_genes = 243
max_mutations = 6
population_size = 10


# initialise the GA
#ga = pyeasyga.GeneticAlgorithm(data,
 #                           population_size=200,
  #                          generations=100,
   #                         crossover_probability=0.8,
    #                        mutation_probability=0.2,
     #                       elitism=True,
      #                      maximise_fitness=False)


def create_individual():
    individual = [randint(0, 6) for _ in range(number_of_genes)] # random action for every situation
    return individual



def crossover(parent_1, parent_2):
    crossover_index = randint(1, number_of_genes)
    child_1a = parent_1[:crossover_index]
    child_1b = [i for i in parent_2 if i not in child_1a]
    child_1 = child_1a + child_1b

    child_2a = parent_2[crossover_index:]
    child_2b = [i for i in parent_1 if i not in child_2a]
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
    if 10 > coordinates[0] >= 1 and 10 > coordinates[1] >= 0:
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
            plan[coordinates[0]][coordinates[1]] = 0
            return 10
        return -1 # no can

    	




def fitness (individual):
    score = 0

    for i in range(10):
        plan = generate_plan()
        position = [0, 0]
        for i in range(200):
            score += move(plan, position, individual)
    return score/200


def run():
	population = [create_individual() for _ in range(population_size)]
	score = [(fitness(population[i]), population[i]) for i in range(population_size)]
	sorted(score, key=lambda x: x[0])
	print(score[0])

run()


