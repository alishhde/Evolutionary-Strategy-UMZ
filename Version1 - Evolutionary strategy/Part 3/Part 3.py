import numpy as np
from copy import deepcopy
import random
# ------------- Fitness Function start ------------- #
def f(vectors):
    """ This Function Takes N-dimension vectors 
    and calculates fitnesses for each of the vectors
    and return the fitness.
    vector: It's a list or an array that consist of 
    some element, whether Integer or float.
    This method returns a value which is sum of the
    element and we save it as our fitness vector. """
    fitnesses = []
    sum = 0
    for veci in vectors:
        for dim in veci:
            sum += dim ** 2
        fitnesses.append(float(sum))
        sum = 0
    return np.array(fitnesses)
# ------------- Fitness Function end ------------- #

# ------------- Parent selection of parent start ------------- #
def selection(parent, parentfittness, children, childrenfitness, lambda_childnum, mu_parentnum, mode):
    """ This method will choose the best fitnesses """
    min = 10000000000000
    index = 0
    childrenfitness = list(childrenfitness)
    children = list(children)
    parentfittness = list(parentfittness)
    parent = list(parent)
    if mode == 0:   # ES(mu, lambda)
        bestparfornext = []
        bestparfittness = []
        for i in range(mu_parentnum):
            for j in range(len(childrenfitness)):
                if abs(childrenfitness[j]) < min:
                    min = childrenfitness[j]
                    index = j
            bestparfornext.append(children[index])
            bestparfittness.append(childrenfitness[index])
            min = 10000000000000
            del childrenfitness[index]
            del children[index]
        return np.array(bestparfornext), bestparfittness
    
    elif mode == 1: # ES(mu + lambda)
        bestparfornext = []
        bestparfittness = []
        main_pop = parent + children
        main_fit = parentfittness + childrenfitness
        for i in range(mu_parentnum):
            for j in range(len(main_fit)):
                if abs(main_fit[j]) < min:
                    min = main_fit[j]
                    index = j
            bestparfornext.append(main_pop[index])
            bestparfittness.append(main_fit[index])
            min = 10000000000000
            del main_fit[index]
            del main_pop[index]
        return np.array(bestparfornext), bestparfittness
# ------------- Parent selection of parent end ------------- #

# ------------- Random parent initialization start ------------- #
def random_parent(dim, mu):
    """ This Function Initialize a parent with
    the given dimension which in this question 
    is whether 10 or 100, and also each Dim is
    in range [-100, 100] according to the que-
    stion and finally it returns the vector of 
    parent. """
    parent_list = []
    for i in range(mu):
        parent_list.append([float(np.random.randint(-100, 101)) for i in range(dim)])
    # we created a list of random number, then we change the list to array
    # we returned an array of vector as our parent vector
    return np.array(parent_list)   
# ------------- Random parent initialization end ------------- #

# ------------- Recombination crossover of parent start ------------- #
def recombination(parent, sigma, lambda_children):
    child = []
    children = []
    for i in range(lambda_children):
        for i in range(len(parent[0])):
            child.append((parent[random.randint(0, 1)][i]))
        children.append(child)
        child = []
    children, sigma = Gaussian_mutation(children, sigma=sigma)
    return children, sigma
# ------------- Recombination crossover of parent end ------------- #

# ------------- Gaussian mutation of parent start ------------- #
def Gaussian_mutation(vectors, mu=0, sigma=1):
    """ This function take three parameters as
    input: 
    vector: which is a array of dimension and
    also vector is the parent which we are 
    going to create child from it.
    mu: Mean (“centre”) of the distribution.
    sigma: Standard deviation (spread or “width”) 
    of the distribution. Must be non-negative. """

    # we have deepcopy of vector, beacuse vector is the parent and 
    # if we didn't have deepcopy of it, any changes on newchildren, 
    # changes its parent too, that's why we have used deep copy here
    newchildren = deepcopy(vectors)
    taw = 1/(len(newchildren[0]) ** (1/2))
    newSigma = sigma * np.exp(taw * np.random.normal(0, 1))

    for i in range(len(newchildren)):
        for j in range(len(newchildren[i])):
            randomSmallNumber = np.random.normal(mu, 1)
            if newchildren[i][j] + newSigma * randomSmallNumber > 100:
                newchildren[i][j] = 100
                continue
            if newchildren[i][j] + newSigma * randomSmallNumber < -100:
                newchildren[i][j] = -100
                continue
            newchildren[i][j] = newchildren[i][j] + newSigma * randomSmallNumber
    return  np.array(newchildren), newSigma
# ------------- Gaussian mutation of parent end ------------- #

# ------------- Main algorithm flow start ------------- #
def evolutionary_strategy():
    """ 1. First we create a random parent with the N-dimension
    where N is what user defines, 
    2. Then we calculate the parent fitness with the f function
    3. Then we create a child by using the RECOMBINATION and 
    MUTATION function.
    4. Then we calculate the child fitness with the f function
    5. At last we compare the fitnesses we have calculated
    and as the question wants to reach to the minimum number 
    we SELECT the one individual whose fitness is less than the
    other one, that's how we can reach to the minimum of the function"""
    
    nDim = int(input("\nEnter the number of the dimension you want\n(In this question it's whether 10 or 100): "))
    loop = int(input("\nEnter the number of time you want algorithm run\n(enter 0 to enter infinite loop till the best fitness): "))
    lambda_children_num = int(input("\nEnter the number for lambda (ES(lambda, mu)In\nthis question It's 10): "))
    mu_parent_num = int(input("\nEnter the number of mu for parent \n(ES(lambda, mu)In\nthis question it's 2): "))
    mode = int(input("\n which kind of selection you want ?\n[0 for ES(mu, lambda), 1 for ES(mu + lambda)]: "))
    sigma = 1

    # Step 1
    parent_vectors = random_parent(nDim, mu_parent_num)

    if loop == 0:
        roundCounter = 0
        while True:
            roundCounter += 1

            # Step 2
            parent_fitness = f(parent_vectors)
            
            # Step 3
            children, sigma = recombination(parent_vectors, sigma, lambda_children_num)
            
            # Step 4
            child_fitness = f(children)

            # Step 5
            parent_vectors, parent_fitness = selection(parent_vectors, parent_fitness, children, child_fitness, lambda_children_num, mu_parent_num, mode)

            print('\nWe are in round : ', roundCounter+1)
            print('These are the best individuals fitnesses till now: ', parent_fitness)
            
    else: 
        for i in range(loop):

            # Step 2
            parent_fitness = f(parent_vectors)

            # Step 3
            children, sigma = recombination(parent_vectors, sigma, lambda_children_num)

            # Step 4
            child_fitness = f(children)

            # Step 5
            parent_vectors, parent_fitness = selection(parent_vectors, parent_fitness, children, child_fitness, lambda_children_num, mu_parent_num, mode)
            
            print('\nWe are in round : ', i+1)
            print('These are the best individuals fitnesses till now: ', parent_fitness, '\n')

        print('Loop Finished Successfully after {}-Round. \n' .format(loop))
            
# ------------- Main algorithm flow end ------------- #
evolutionary_strategy()