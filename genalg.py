import numpy as np
import random
from PIL import Image
import math


# I defined these variables automatically here but you could take user input
height = 16
width = 16
pop_size = 10
parent_number = 3
target_file_name = "banana.jpg"
population_size = 100
num_of_gens = 100
parents_per_gen = 5
mutations_per_gen = 1
# Must be bigger than 0 due to weird coding (line 70 & 74), might fix later
max_mutation_change = 3


# First class: a single image/person
class Person:
    # Only takes in height and width and automatically makes a random image of that size
    # Image is in the form of an array
    def __init__(self, height, width):
        # First list
        self.array = []
        # The height is the number of lists in the first list
        for k in range(height):
            # The width determines how many lists in every one of those lists
            self.array.append([np.random.randint(0, 256, 3).tolist() for i in range(width)])
        # Converting the lists in lists in a list into an array
        self.array = np.array(self.array)
        # Saving the height and width values for later use
        self.height = height
        self.width = width

    # A test of how close this image is to a different image
    # Takes in a target in array format
    def fitness_test(self, target):
        # Starts the score at 0
        score = 0
        # For each pixel
        for i in range(self.height):
            for k in range(self.width):
                # Add the difference between the target and the actual pixel to score
                score =+ math.sqrt(((target[i][k][0]-self.array[i][k][0])**2)+((target[i][k][1]-self.array[i][k][1])**2)+((target[i][k][2]-self.array[i][k][2])**2))
        # Small number is a good score
        return score

    # A function to randomly change the pixels of the image by a bit
    # Takes is the amount of mutations and the maximum magnitude of those mutations
    def mutate(self, amount, max_change):
        # For every mutation
        for i in range(amount):
            # Randomly determines whether to add or subtract
            a = random.getrandbits(1)
            # Randomly determines which row the pixel will be in
            x = np.random.randint(0, self.height)
            # Randomly determines which pixel in that row it will be
            y = np.random.randint(0, self.width)
            # defining a variable for the pixel it chose
            pixel = self.array[x][y]

            # For each RGB, or other, value
            for i in range(len(pixel)):
                # If it chose adding
                if a == True:
                    # Add a random amount between 0 and the max amount
                    pixel[i] += np.random.randint(0, max_change)
                # If it chose subtracting
                else:
                    # Subtract a random amount between 0 and the max amount
                    pixel[i] -= np.random.randint(0, max_change)
                # Making sure the value is between 0 and 256 (for RGB)
                max(min(256, pixel[i]), 0)
            # Changing the pixel
            self.array[x][y] = pixel

    # A function to display the image
    def display(self):
        # Necessary step to display the image correctly
        im = self.array.astype(np.uint8)
        # Converting from array to image
        im = Image.fromarray(im, mode = 'RGB')
        # Showing image
        im.show()


# Second class: a group of images/people
class Population:
    # Takes in the population size and automatically creates that amount of images/people
    def __init__(self, pop_size):
        # Making the list the objects will be added to
        self.pop = []
        # For the amount of people you want
        for i in range(pop_size):
            # Append a image/person object to the list
            self.pop.append(Person(height, width))

    # Tests every image/person in the population and picks a list of parents
    # Takes in target array and amount of parents needed
    def test(self, target, parent_amount):
        # Initializes list of scores
        scores = []
        # For each image/person in the population
        for i in self.pop:
            # Append its fitness score to the scores list
            scores.append(1/i.fitness_test(target))
        # Picks all the parents according to the weights
        # MUST FIX: LOW SCORES ARE GOOD, NOT HIGH
        parents = random.choices(self.pop, weights = scores, k = parent_amount)
        # Returns the list of parents
        return parents

    # Creates a new list of images/people from the list of parents
    # Takes in the list of parents, new population size, dimensions and mutation variables
    def mate(self, parents_list, pop_size, height, width, mutate_amount, max_change):
        # Initializes list for new population
        new_pop = []
        # For the amount of people/images you need
        for i in range(pop_size):    
            # Create a new person
            new = Person(height, width)
            # For each row
            for i in range(height):
                # For each pixel in that row
                for k in range(width):
                    # Choose a random parent
                    parent = random.choice(parents_list)
                    # That parent donates the pixel
                    new.array[i][k] = parent.array[i][k]
            # Some of the pixels mutate
            new.mutate(mutate_amount, max_change)
            # The new image/person is added to the new population list
            new_pop.append(new)
        # Sets the population list to this new list
        self.pop = new_pop


# Third class: the actual algorimth
class Algorimth:
    # Takes in the population size, target array, and dimesions
    def __init__(self, pop_size, target, height, width):
        # Defining each variable
        self.pop_size = pop_size
        self.height = height
        self.width = width
        # Creating a population of the right size
        self.population = Population(pop_size)
        self.target = target

    # A function that makes a new generation
    # Takes in amount of parents and mutation variables
    def generation(self, parent_amount, mutate_amount, max_change):
        # Finds the parents
        parents = self.population.test(self.target, parent_amount)
        # Creates a new population from those parents
        self.population.mate(parents, self.pop_size, self.height, self.width, mutate_amount, max_change)


# Name equals main thingy
#if __name__ == "__main_":
if True:
    # Opening the target image
    with Image.open(target_file_name) as img:
        # Resizing to the correct dimesions
        img = img.resize((height,width))
        img.show()
        # Converting to array
        target = np.asarray(img)

    # Initializing the algorimth
    algorimth = Algorimth(population_size, target, height, width)

    # Displaying the first image/person in the population
    algorimth.population.pop[0].display()
    # Displaying the first image/person's score on the fitness test
    print(algorimth.population.pop[0].fitness_test(target))

    # For the amount of generations you want to have
    for i in range(num_of_gens):
        # Make a new generation
        algorimth.generation(parents_per_gen, mutations_per_gen, max_mutation_change)

    # Displaying the first image/person in the population after these generations
    algorimth.population.pop[0].display()
    # Displaying the first image/person's score on the fitness test
    print(algorimth.population.pop[0].fitness_test(target))

