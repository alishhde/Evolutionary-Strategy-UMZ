from numpy.random import randint, rand, choice
from random import choices

def fx(individual):
    """ Fitness function """
    return (individual ** 2 + 2 * individual)

def selection(population, score):
    returnlist = []
    counter = len(population)
    # Computes the totallity of the population fitness
    population_fitness = sum(score)
    
    # Computes for each chromosome the probability 
    try:
        chromosome_probabilities = list([fitness/population_fitness for fitness in score])
    except ZeroDivisionError:
        population_fitness = 1
        chromosome_probabilities = list([fitness/population_fitness for fitness in score])

    for i in range(counter):
        value = choices(population, weights = chromosome_probabilities, k = 1)
        returnlist.append(value)

    return returnlist

def crossover(child1, child2, change_prob, crossover_kind = 1):
    
    onepointcrossover = False
    twopointcrossover = False
    uniformcrossover = False
    if crossover_kind == 1:
        onepointcrossover = True
        twopointcrossover = False
        uniformcrossover = False
    elif crossover_kind == 2:
        twopointcrossover = True
        onepointcrossover = False
        uniformcrossover = False
    elif crossover_kind == 3:
        uniformcrossover = True
        onepointcrossover = False
        twopointcrossover = False

    if rand() < change_prob:
        if onepointcrossover:
            crossover_point = randint(1, 5)
            child1 = child1[:crossover_point] + child2[crossover_point:]
            child2 = child2[:crossover_point] + child1[crossover_point:]
        
        elif twopointcrossover:
            crossover_point1 = randint(1, 3)

            while True:
                crossover_point2 = randint(1, 5)
                if crossover_point2 == crossover_point1 or crossover_point2 < crossover_point1:
                    continue
                else:
                    break

            child1 = child1[:crossover_point1] + child2[crossover_point1:crossover_point2] + child1[crossover_point2:]
            child2 = child2[:crossover_point1] + child1[crossover_point1:crossover_point2] + child2[crossover_point2:]

        elif uniformcrossover:
            for i in range(len(child1)):
                if rand() < change_prob:
                    child1[i], child2[i] = child2[i], child1[i]
                else:
                    pass
    else:
        pass

    return [child1, child2]

def mutation(child, change_prob):
    for i in range(len(child)):
        if rand() < change_prob:
            child[i] = 1 - child[i]
        else:
            pass

    return child
    
def genetic_algorithm(fx, number_of_binary, number_of_population, crossover_probab, crossover_kind, mutation_probab, loopnumber):
    
    binary_number = {(0, 0, 0, 0, 0) : 0, (0, 0, 0, 0, 1) : 1, (0, 0, 0, 1, 0) : 2, (0, 0, 0, 1, 1) : 3, (0, 0, 1, 0, 0) : 4, (0, 0, 1, 0, 1) : 5, (0, 0, 1, 1, 0) : 6, (0, 0, 1, 1, 1) : 7, (0, 1, 0, 0, 0) : 8, (0, 1, 0, 0, 1) : 9, 
    (0, 1, 0, 1, 0) : 10, (0, 1, 0, 1, 1) : 11, (0, 1, 1, 0, 0) : 12, (0, 1, 1, 0, 1) : 13, (0, 1, 1, 1, 0) : 14, (0, 1, 1, 1, 1) : 15, (1, 0, 0, 0, 0) : 16, (1, 0, 0, 0, 1) : 17, (1, 0, 0, 1, 0) : 18, (1, 0, 0, 1, 1) : 19, 
    (1, 0, 1, 0, 0) : 20, (1, 0, 1, 0, 1) : 21, (1, 0, 1, 1, 0) : 22, (1, 0, 1, 1, 1) : 23, (1, 1, 0, 0, 0) : 24, (1, 1, 0, 0, 1) : 25, (1, 1, 0, 1, 0) : 26, (1, 1, 0, 1, 1) : 27, (1, 1, 1, 0, 0) : 28, (1, 1, 1, 0, 1) : 29, (1, 1, 1, 1, 0) : 30, (1, 1, 1, 1, 1) : 31, }
    # selecting < number_of_population > as mating pool with the < number_of_binary > for < loopnumber >
    matingpool = [randint(0, 2, number_of_binary).tolist() for i in range(number_of_population)]

    # defining the first number as the best fitness number
    bestbin, bestint, best_score = tuple(matingpool[0]), binary_number[tuple(matingpool[0])], fx(binary_number[tuple(matingpool[0])]) 

    # ------------------------ MAIN -------------------------
    # this determines how many times best score reapeated 
    times = 0
    for i in range(loopnumber):

        # ------------------calculating scores ----------------------
        print('\n\n', 'Round:  ', i+1,)
        # list of all scores for every individual
        all_matingpool_scores = [fx(binary_number[tuple(matingpool[i])]) for i in range(len(matingpool))]

        # computing best score
        for i in range(len(matingpool)):
            if all_matingpool_scores[i] == best_score:
                    times += 1
            elif all_matingpool_scores[i] > best_score:
                bestbin, bestint, best_score = tuple(matingpool[i]), binary_number[tuple(matingpool[i])], all_matingpool_scores[i]
            else: pass

            if times == 3:
                return "Best Score is reapeating, End of algorithm. :D"

        print('New best nubmer till here: ', bestbin, bestint, best_score)
        # ------------------calculating scores ----------------------
       
        # -----------------selecting new parenting -----------------
        # we select the best parent from the mating pool and
        parents = selection(matingpool, all_matingpool_scores)
        
        new_parent = []
        for i in range(len(parents)):
            new_parent.append(parents[i][0])
        # ----------------selecting new parenting -----------------

        evolutioned_population = []

        if len(new_parent) % 2 == 1:
            for i in range(0, len(new_parent)-1, 2):
                par1 = new_parent[i]
                par2 = new_parent[i+1]

                for child in crossover(par1, par2, crossover_probab, crossover_kind):
                    evolutioned_population.append(mutation(child, mutation_probab))

            par1 = new_parent[-1]
            par2 = new_parent[randint(1, len(new_parent))]
            for child in crossover(par1, par2, crossover_probab, crossover_kind):
                evolutioned_population.append(mutation(child, mutation_probab))
                
        else:
            for i in range(0, len(new_parent), 2):
                par1 = new_parent[i]
                par2 = new_parent[i+1]

                for child in crossover(par1, par2, crossover_probab, crossover_kind):
                    evolutioned_population.append(mutation(child, mutation_probab))
        matingpool = evolutioned_population
         
    return("Loop Finished successfully. :D")
    # ------------------------ MAIN -------------------------

number_of_binary = 5
number_of_population = int(input("Enter number of population(even number)[2..32]: "))
crossover_probab = float(input("Enter crossover probability happen[0..1]: "))
crossover_kind = int(input("Which crossover you want ? \nEnter 1 for onepointcrossover or Enter 2 for twopointcrossover Enter 3 for uniformcrossover : "))
mutation_probab = float(input("Enter Mutation probability happen[0..1]: "))
loopnumber = int(input("Enter how many time you want algorithm work: "))

print(genetic_algorithm(fx, number_of_binary, number_of_population, crossover_probab, crossover_kind, mutation_probab, loopnumber))