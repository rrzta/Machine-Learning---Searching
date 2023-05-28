from math import cos, sin
import random

def fitnessFunc(x, y):
    '''
        Predefined functions in task
    '''
    # a -> Smallest value
    a = 0.01
    # Formula 
    h = ((cos(x) + sin(y))**2) / (x**2) + (y**2)
    fitness = 1 / (h + a)
    return fitness

class solutionGA:
    def __init__(self, profile):
        '''A
        Function to initialize the GA
        '''
        self.populationSize = profile["populationSize"]
        self.chromosomeLength = profile["chromosomeLength"]
        self.probCrossover = profile["probCrossover"]
        self.probMutation = profile["probMutation"]
        self.generation = profile["generation"]
        self.funcH = profile["funcH"]
        self.domain = profile["domain"]
        self.population = []
        for _ in range(self.populationSize):
            self.population.append(self.generateChromosome())

    def generateChromosome(self):
        # Function to make binary chromosomes
        result = []
        # Looping as much as the length of the Chromosomes
        for _ in range(self.chromosomeLength):
            # Generate random binary number(0 or 1)
            result.append(random.randint(0, 1))
        return result

    def chromosomeDecode(self, chrmsm):
        # Function to decode chromosomes
        xMin, xMax = self.domain[0]
        yMin, yMax = self.domain[1]
        tmp = 0
        x = 0
        y = 0
        nw = (self.chromosomeLength)//2
        for i in range(0, nw):
            tmp += 2**(-(i + 1))
        for i in range(0, nw):
            x += chrmsm[i] * 2**-(i + 1)
            y += chrmsm[nw + i] * 2**-(i + 1)
        x = (x * (xMax - xMin / tmp))
        y = (y * (yMax - yMin / tmp))
        x = x + xMin
        y = y + yMin
        return [x,y]

    def totalFitness(self):
        # Function to calculate fitness value
        result = []
        for i in self.population:
            result.append(self.funcH(*self.chromosomeDecode(i)))
        return result

    def rouletteWheel(self, fitness):
        # Function to select parents by using roulette wheel method
        total = 0
        totalFitness = sum(fitness)
        for i in range(self.populationSize):
            if (fitness[i]/totalFitness) > random.uniform(0, 1):
                total = i
                break
            i += 1
        return self.population[total]

    def crossover(self, x, y):
        # Function to crossovering
        if (random.uniform(0, 1) < self.probCrossover):
            # Randomly select the crossover point
            swap = random.randint(0, self.chromosomeLength - 1)
            for i in range(swap):
                x[i], y[i] = y[i], x[i] #Swapping the binary numbers
        return [x, y]

    def mutation(self, offspring):
        # Function to do mutations of a given offspring
        for i in range(self.chromosomeLength):
            if (random.uniform(0, 1) < self.probMutation):
                # Swaping the binary numbers
                offspring[0][i] = 1 - offspring[0][i]
                offspring[1][i] = 1 - offspring[1][i]
        return offspring

    def survivorSelection(self, fitness):
        # Function to do survivor selection
        el1 = 0
        el2 = 0
        for i in range(1, len(fitness)):
            if fitness[i] > fitness[el1]:
                el2 = el1
                el1 = i
        return el1, el2

    def changeGen(self):
        for _ in range(self.generation):
            # Listing fitness
            fitness = self.totalFitness()

            # Assign new population
            newPopp = []

            # Two best indices 
            elt1, elt2 = self.survivorSelection(fitness)

            # Add the population with the best index value to the next generation
            newPopp.append(self.population[elt1])
            newPopp.append(self.population[elt2])

            # Looping and finding the parent by calling the rouletteWheel() function
            for _ in range((self.populationSize-2)//2):
                parent1 = self.rouletteWheel(fitness)
                parent2 = self.rouletteWheel(fitness)

                # Looping and finding for parents if parent 1 and paretn 2 are the same
                while(parent1 == parent2):
                    parent2 = self.rouletteWheel(fitness)

                # Crossovering to both parents
                offspring = self.crossover(parent1[:], parent2[:])

                # Mutations in crossover results
                offspring = self.mutation(offspring)

                # Add offspring to the new population list
                newPopp.append(offspring[0])
                newPopp.append(offspring[1])

            # Assign new population to the main population
            self.population = newPopp

    def maximumValue(self):
        # Function that finds minimum value.
        fitness = self.totalFitness()
        ftns = fitness.index(max(fitness))
        bestFitness = fitness[ftns]

        # Function to get the best chromosome
        bestChromosome = self.population[ftns]

        # Function to decode the best chromosome
        decodeVal = self.chromosomeDecode(self.population[ftns])

        # Run Genetic Algorithm
        print("=================================================================")
        print("                         Genetic Algorithm")
        print("=================================================================")
        # Print best chromosome 
        print("Kromosom terbaik    : ", bestChromosome)
        # Print fitness value
        print("Nilai fitness\t    : ", bestFitness)
        # Print chromosome decoded
        print("Dekode kromosom(x,y): ", decodeVal)
        print("=================================================================")

'''
    Run Genetic Algorithm
'''
if __name__ == "__main__":
    # Format profile to use in GA
    # Change another value in profile to use in GA
    profile = {
        "populationSize": 200, # Population size
        "chromosomeLength": 8, # Chromosome length
        "generation": 50, # Number of generation (Max iteration)
        "probCrossover": 0.5, # Probability of crossover
        "probMutation": 0.25, # Probability of mutation
        "funcH": fitnessFunc, # Heuristic function
        "domain": [[-5, 5], [-5, 5]], # Domain of the function -> -5 <= x <= 5 and -5 <= y <= 5
    }

    # Class Initialization
    final = solutionGA(profile)

    # Output Results from Genetic Algorithm
    final.changeGen()
    final.maximumValue()