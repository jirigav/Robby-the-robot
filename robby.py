from pyeasyga import pyeasyga
from random import randint

number_of_genes = 243
max_mutations = 6
data = [0, 1, 2, 3, 4, 5, 6]

# initialise the GA
ga = pyeasyga.GeneticAlgorithm(data,
                            population_size=200,
                            generations=100,
                            crossover_probability=0.8,
                            mutation_probability=0.2,
                            elitism=True,
                            maximise_fitness=False)


def create_individual(data):
    individual = [randint(0, 6) for _ in range(number_of_genes)] # random action for every situation
    return individual

ga.create_individual = create_individual

def crossover(parent_1, parent_2):
    crossover_index = random.randrange(1, number_of_genes)
    child_1a = parent_1[:crossover_index]
    child_1b = [i for i in parent_2 if i not in child_1a]
    child_1 = child_1a + child_1b

    child_2a = parent_2[crossover_index:]
    child_2b = [i for i in parent_1 if i not in child_2a]
    child_2 = child_2a + child_2b

    return child_1, child_2

ga.crossover_function = crossover

def mutate(individual):
    number_of_mutations = randint(1, max_mutations) # choose random number of mutations
    for i in range(number_of_mutations):
    	individual[randint(0, max_mutations)] = randint(0, 6) 

ga.mutate_function = mutate


def generate_map():
	return [[randint(0, 1) for _ in range(10)] for _ in range(10)]

def fitness (individual, data):
    score = 0

print(generate_map())