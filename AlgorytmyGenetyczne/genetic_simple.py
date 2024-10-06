#!/usr/bin/python3

# Way of solvong a problem using genethical algorithm:
# 1. Define a initial population, fenotypes, chromosons, and fit function.
# 2. Choose a best-fittedchromosons from population
# 3. If needed, create a childs form choosen population, randomly
# 4. Apply mutations, randomly
# 5. Create new population including best-fitted parents and childs, and apply that population to point 2. untill stop function will break the algorithm.

# Example of usage of genethic algorithm - looking for extremum of 1 unknown function.
# We have a function like f(x) = 2x + 1, and we want to find its maximum value using genethical algorithm. The inputs laus in range [0 - 32].

# 1.1 Define an initial population: Our initial population is pre defined N fenotypes from fenotypes [0-32] numbers.
#   Basing on fenotypes we can define chromosons. The chromoson is a binary representation of a fenotype. For example, if we have a fenotype 2, its chromoson is 0b00010. 
#   Each chromosn has 5 digits - it is enough to store maximum fenotype value, which is 32.
# 1.2 Choose an initial population - we assume we have initial population of range N = 7 (our assumption). Now, we choose 7 random fenotypes form all available fenotypes - let it be [6, 5, 13, 21, 26, 18, 8, 5].
#   For each fenotype we have a chromosom, like:
# 0b00110 -> 6
# 0b00101 -> 5
# 0b01101 -> 13
# 0b10101 -> 21
# 0b11010 -> 26
# 0b10010 -> 18
# 0b01000 -> 8
# 0b00101 -> 5
# 1.3 Define a fit function. In our case it will be initial function - f(x). Larger function output is better fit.
#
# 2. Define selection method. In our case we will use rulette round selection method. For each chromoson ch we apply the formula: v(ch) = f(ch) / (sum(f(ch1) .. f(chN))). 
#      The formula will give higher value is fit function will give a higher output for a given chromoson. It means - probability of choose chromosons given higher fit function value will be higher.
#      Now we define an 100 element array. In the array we have a value of chromosons. Each chromoson is in the arras as often, as selection method output is. Next, we use the arras as an input for random function to selct
#      The chromosons for next iterations.

import random

max_value = 128

def fit_function(x):
    return 2 * x + 1

# Define a stiop function - an algorith would stop if in apop we have a chromoson that would give ft_function result 65 or higher. 
def stop_function(pop):
    for ch in pop:
        if max_value - fit_function(ch) <= 1:
            return True
    return False

# Implementation of roulette check for selectong chromosons form population.
def roulette_check(pop):
    # Generate fit values for all chromosons from initial pop
    all_values = 0
    fit_values = dict()
    pop_size = len(pop)

    for ch in pop:
        all_values += fit_function(ch)

    for i in range(pop_size):
        fit_values[pop[i]] = int(round(100 * fit_function(pop[i]) / all_values, 0))

    # Generate roulette list
    roulette_list = list()
    for key, val in fit_values.items():
        roulette_list.extend([key] * val)

    # Choose a N items
    choosen_items = list()
    for i in range(pop_size):
        choosen_items.extend([random.choice(roulette_list)])

    return choosen_items

def cross_function(ch1, ch2):
    gen_to_change = random.choice(range(10)) #We choose from which gen in chromosons the gens would be exchanged. As we have 5 gens - we can choose up to 5.
    mask_1 = 0x1f << gen_to_change
    mask_2 = 0x1f >> (10 - gen_to_change)

    child_1 = ch1 & mask_1 | ch2 & mask_2
    child_2 = ch2 & mask_1 | ch1 & mask_2
    return [child_1, child_2]

def mutation_function(ch):
    gen_to_mutate = random.choice(range(100)) # We choose between 1...10 to redoce mutation probability
    ch_mut = 0
    if gen_to_mutate < 10:
        ch_mut = (ch ^ (1 << gen_to_mutate))
    return ch_mut

# Define a pair function - the funciton will take 2 elents randomly from population and mix together to create a new objects.
def pair_function(pop):
    _pop = pop.copy()
    pop_size = len(pop)
    nr_of_pairs = int(round(pop_size / 2, 0))
    children = list()

    for i in range(nr_of_pairs):
        ch1 = random.choice(_pop)
        _pop.remove(ch1)
        ch2 = random.choice(_pop)
        _pop.remove(ch2)
        cross_function(ch1, ch2)

        ch1 = mutation_function(ch1)
        ch2 = mutation_function(ch2)

        children.extend([ch1, ch2])

    return children


if __name__ == "__main__":
    initial_pop = [6, 5, 13, 21, 26, 18, 8, 5]
    population = initial_pop
    iteration = 0

    while(not stop_function(population)):
        choosen_chromosons = roulette_check(population)
        population = pair_function(choosen_chromosons)
        iteration += 1
        print("ITERATION: initial pop: " + str(choosen_chromosons) + " Childs: " + str(population))
    
    print("Solution found in " + str(iteration) + " iterations.")

    