import numpy as np
from copy import deepcopy

# ------------- Fitness Function start ------------- #
def f(vector):
    """ This Function Takes N-dimension vector 
    and calculates fitness and return the fitness
    vector: Its a list or an array that consist of 
    some element, whether Integer or float
    This method returns a value which is sum of the
    element and we save it as our fitness vector. """

    sum = 0
    for i in range(len(vector)):
        sum += vector[i] ** 2
    return sum
# ------------- Fitness Function end ------------- #

# ------------- Random parent initialization start ------------- #
def random_parent(n):
    """ This Function Initialize a parent with
    the given dimension which in this question 
    is whether 10 or 100, and also each Dim is
    in range [-100, 100] according to the que-
    stion and finally it returns the vector of 
    parent. """

    # we created a list of random number, then we change the list to array
    # we returned an array of vector as our parent vector
    return np.array([float(np.random.randint(-100, 101)) for i in range(n)])   
# ------------- Random parent initialization end ------------- #

# ------------- Gaussian mutation of parent start ------------- #
def Gaussian_mutation(vector, mu=0, sigma=1):
    """ This function take three parameters as
    input: 
    vector: which is a array of dimension and
    also vector is the parent which we are 
    going to create child from it.
    mu: Mean (“centre”) of the distribution.
    sigma: Standard deviation (spread or “width”) 
    of the distribution. Must be non-negative. """

    # we have deepcopy of vector, beacuse vector is the parent and 
    # if we didn't have deepcopy of it, any changes on child, changes 
    # its parent too, that's why we have used deep copy here
    child = deepcopy(vector)
    for i in range(len(child)):
        randomSmallNumber = np.random.normal(mu, sigma)

        if child[i] + randomSmallNumber > 100:
            child[i] = 100
            continue
        if child[i] + randomSmallNumber < -100:
            child[i] = -100
            continue
        child[i] = child[i] + randomSmallNumber
    return child
# ------------- Gaussian mutation of parent end ------------- #

# ------------- Main algorithm flow start ------------- #
def evolutionary_strategy():
    """ 1. First we create a random parent with the N-dimension
    where N is what user defines.
    2. Then we calculate the parent fitness with the f function.
    3. Then we create a child by using the mutation function.
    4. Then we calculate the child fitness with the f function.
    5. At last we compare the two fitnesses we have calculated
    and as the question wants to reach to the minimum number 
    we select the one individual whose fitness is less than the
    other one, that's how we can reach to the minimum of the function.
    6. Then each time we check the iterator if equals to iteration 
    which user said then we change the sigma to the new value. """

    nDim = int(input("\nEnter the number of the dimension you want\n(In this question it's whether 10 or 100): "))
    loop = int(input("\nEnter the number of time you want algorithm run\n(enter 0 to enter infinite loop till the best fitness): "))
    iteration = int(input("\nEnter the iteration less than the number for loop you entered: "))
    c_parameter = float(input("\nEnter the value of parameter c, between[0.8, 1]: "))
    successfull_child = 0
    probability_s = float(0)
    sigma = 1
    iterator = 0

    # Step 1
    parent = random_parent(nDim)
    
    if loop == 0:
        i = 0
        while True:
            i += 1
            iterator += 1

            # Step 2
            parent_fitness = f(parent)
            
            # Step 3
            child = Gaussian_mutation(parent, sigma=sigma)
            
            # Step 4
            child_fitness = f(child)
            
            # Step 5
            if child_fitness < parent_fitness:
                parent = child
                print('\nWe are in round : ', i+1)
                print('This is the best child fitness till now: ', child_fitness)
                successfull_child += 1
            
            # Step 6
            if iterator == iteration:
                # now it's end of iteration user said, and we're updating sigma's value
                iterator = 0
                probability_s = successfull_child/iteration

                if probability_s > 1.5:
                    sigma = sigma / c_parameter
                    
                elif probability_s < 1.5:
                    sigma = sigma * c_parameter

                else:
                    sigma = sigma

    else: 
        for i in range(loop):
            iterator += 1

            # Step 2
            parent_fitness = f(parent)
            
            # Step 3
            child = Gaussian_mutation(parent, sigma=sigma)
            
            # Step 4
            child_fitness = f(child)
            
            # Step 5
            if child_fitness < parent_fitness:
                parent = child
                print('\nWe are in round : ', i+1)
                print('This is the best child fitness till now: ', child_fitness)
                successfull_child += 1
            
            # Step 6
            if iterator == iteration:
                # now it's end of iteration user said, and we're updating sigma's value
                iterator = 0
                probability_s = successfull_child/iteration

                if probability_s > 1.5:
                    sigma = sigma / c_parameter
                    
                elif probability_s < 1.5:
                    sigma = sigma * c_parameter

                else:
                    sigma = sigma
        print('Loop Finished Successfully after {}-Round. \n' .format(loop))

# ------------- Main algorithm flow end ------------- #

evolutionary_strategy()