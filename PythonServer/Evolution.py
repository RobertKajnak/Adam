import numpy as np
import numpy.random as rand
from numpy.random import choice
from numpy.random import normal
import random


class Initialize:

    def __init__(self):

        self.pop_size = 20
        self.vector_length = 22


    def create_population(self, pop_size, vector_length):

        population = []

        for i in range(pop_size):

            individual = rand.random(vector_length).tolist()
            population.append(individual)

        np.save('weight_vectors', np.array(population))

        return


    def main(self):
        self.create_population(self.pop_size, self.vector_length)
        return



class RecombineAndMutate:

    def __init__(self):

        self.population = np.load('weight_vectors.npy')
        self.n_parents = 10
        self.a = 0.5
        self.mutation_rate = 0.02
        self.sd = 0.2

        return


    # parent selection
    def uniform_random(self, population, n_parents):
        parents_indices = choice(np.arange(len(population)), n_parents, replace=False).tolist()
        parents = [population[i] for i in parents_indices]
        return parents


    # take random individual
    def pop_random(self, lst):
        idx = random.randrange(0, len(lst))
        return lst.pop(idx)


    # play for cupid
    def make_pairs(self, lst):
        pairs = []

        while lst:
            rand1 = self.pop_random(lst)
            rand2 = self.pop_random(lst)
            pair = [rand1, rand2]
            pairs.append(pair)

        return pairs


    # recombine individuals
    def blend_crossover(self, pairs, a):

        offspring = []

        for pair in pairs:

            child = []

            for gene in range(len(pair[0])):

                gene_1 = pair[0][gene]
                gene_2 = pair[1][gene]

                d = abs(gene_1 - gene_2)

                min_bound = min(gene_1, gene_2) - a * d

                if min_bound < 0:
                    min_bound = 0

                max_bound = max(gene_1, gene_2) + a * d

                if max_bound > 1:
                    max_bound = 1

                gene = random.uniform(min_bound, max_bound)

                child.append(gene)

            offspring.append(child)

        return np.array(offspring)


    # mutate population
    def gaussian_perturbation(self, population, mutation_rate, sd):

        population = population.tolist()

        for individual in population:

            for gene in individual:

                if random.random() < mutation_rate:

                    mutation = normal(0, sd)

                    if gene + mutation >= 1:
                        population[population.index(individual)][individual.index(gene)] = 1

                    elif gene + mutation <= 0:
                        population[population.index(individual)][individual.index(gene)] = 0

                    else:
                        population[population.index(individual)][individual.index(gene)] += mutation

        return np.array(population)


    def main(self):
        parents = self.uniform_random(self.population, self.n_parents)
        pairs = self.make_pairs(parents)
        offspring = self.blend_crossover(pairs, self.a)
        population = np.vstack((self.population, offspring))
        population = self.gaussian_perturbation(population, self.mutation_rate, self.sd)
        np.save('weight_vectors.npy', population)
        return



class TrimPopulation:

    def __init__(self):

        # get review and alikeness score from database to devise fitness score
        self.population = np.load('weight_vectors.npy')
        self.fitness = np.arange(25)
        self.pop_size = 20

        return


    # survivor selection
    def mu_plus_lambda(self, population, population_size):

        survivors_indices = (-self.fitness).argsort()[:population_size]
        population = [population[i] for i in survivors_indices]

        return population


    def main(self):

        population = self.mu_plus_lambda(self.population, self.pop_size)
        np.save('weight_vectors.npy', population)

        return



