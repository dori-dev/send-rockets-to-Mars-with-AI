"""
Project classes
"""

# Standard library imports
from math import ceil
from random import randint, choice

# Third party imports
from EasyDraw.Vector import Vector, RandomVector

# Local imports
from constant import WIDTH, HEIGHT
from constant import IMAGE_DIR, MARS_COORDS
from constant import POPULATION_SIZE, ROCKET_LIFESPAN, MUTATION_RATE


class Population:
    """To control the generation of rockets
    """

    def __init__(self):
        self.rockets = []
        self.mating_pool = []
        for _ in range(POPULATION_SIZE):
            self.rockets.append(Rocket())

    def run(self, app):
        """update and show the rockets

        Args:
            app (EasyDraw.EasyDraw): application variable
        """
        for rocket in self.rockets:
            rocket.update(app)
            rocket.show(app.canvas)

    def evaluate(self):
        """Evaluating the fitness
        """
        max_fitness = 0
        # choice largest fitness
        for i in range(0, POPULATION_SIZE):
            self.rockets[i].calculate_fitness()
            if self.rockets[i].fitness > max_fitness:
                max_fitness = self.rockets[i].fitness

        for i in range(0, POPULATION_SIZE):
            # rockets's fitness between 0 to 1
            self.rockets[i].fitness /= max_fitness

        self.mating_pool = []  # clear mating_pool
        for i in range(0, POPULATION_SIZE):
            # The number of times this parent is in the mating pool
            # To change the chance of choosing parents over fitness
            number = ceil(self.rockets[i].fitness * 100)
            for _ in range(0, number):
                self.mating_pool.append(self.rockets[i])

    def selection(self):
        """Selection parents, and make new rockets
        """
        new_rockets = []
        for _ in self.rockets:
            # choosing parents
            parent_a = choice(self.mating_pool).dna
            parent_b = choice(self.mating_pool).dna
            # Mutations and distribution of genes‌
            child = parent_a.crossover(parent_b)
            child.mutation()
            # Create rocket with new genes
            new_rockets.append(Rocket(child))
        self.rockets = new_rockets


class DNA:
    """To control the DNA of rockets
    """

    def __init__(self, genes=None):
        if genes is None:
            # In the first generation, random genes are created
            self.genes = []
            for _ in range(0, ROCKET_LIFESPAN):
                self.genes.append(RandomVector())
        else:
            self.genes = genes

    def crossover(self, parent_b: list) -> object:
        """Getting genes from parents

        Args:
            parent_b (list): second parent

        Returns:
            [class]: DNA class with new genes
        """
        midpoint = randint(0, ROCKET_LIFESPAN)
        new_genes = parent_b.genes[:midpoint] + self.genes[midpoint:]
        return DNA(new_genes)

    def mutation(self):
        """Mutations of some genes according to MUTATION_RATE
        """
        for i in range(0, ROCKET_LIFESPAN):
            if randint(1, 100) < MUTATION_RATE * 100:
                self.genes[i] = RandomVector()


class Rocket:
    """To update, show and calculate fitness of rockets
    """

    def __init__(self, dna=None):
        self.pos = Vector(WIDTH // 2, HEIGHT - 40)  # position
        self.vel = Vector(0, 0)  # velocity
        self.acc = Vector(0, 0)  # acceleration

        self.reached = False
        self.crashed = False
        self.alive_time = 0
        self.fitness = 0

        if dna is None:
            # In the first generation, random genes are used
            self.dna = DNA()
        else:
            self.dna = dna

    def apply_force(self, force: Vector):
        """apply force to self.acc

        Args:
            force (Vector): Amount of force
        """
        self.acc += force

    def update(self, app):
        """Update the rocket,
        Apply force, velocity and survive time
        Check crashed and reached

        Args:
            app (EasyDraw.EasyDraw): application variable
        """
        # If crashed or reached, don't update rocket
        if self.crashed or self.reached:
            return

        # Applying force according to the genes it has
        self.apply_force(self.dna.genes[app.lifespan_count])
        # Apply velocity and alive_time, change position and reset acceleration
        self.alive_time += 1
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        # Reached Mars
        if self.pos.distance_from(MARS_COORDS) < 80:
            self.reached = True
            self.pos = MARS_COORDS
            # This means that the rocket has been alive for as long as possible
            self.alive_time = ROCKET_LIFESPAN

        for blackhole in app.blackholes:
            # It hit this blackhole
            if self.pos.distance_from(blackhole) < 60:
                self.crashed = True

        # It crashed
        if self.pos.x > WIDTH or self.pos.x < 0 or \
                self.pos.y > HEIGHT or self.pos.y < 0:
            self.crashed = True

    def calculate_fitness(self):
        """calculate the fitness,
        with distance, alive_time, reached and crashed
        These calculations can be modified to obtain different outputs
        """
        dist = self.pos.distance_from(MARS_COORDS)
        # If the distance is greater than WIDTH, it becomes WIDTH
        dist = min(dist, WIDTH)

        # The shorter the distance, the more fitness are calculated
        self.fitness = WIDTH + 1 - dist
        # Calculating fitness based on when rocket survive
        self.fitness *= self.alive_time ** 0.5 + 1
        # If the rocket reached or crashed, the fitness changes
        if self.reached:
            self.fitness *= self.alive_time ** 0.5 * 2
        if self.crashed:
            self.fitness /= dist ** 0.5 + 1

        # Return the ceiling of x as an Integral.
        self.fitness = ceil(self.fitness)

    def show(self, canvas):
        """show the rockets in screen

        Args:
            canvas (EasyDraw.EasyDraw.canvas): canvas of screen
        """
        # If crashed, don't show rocket
        if self.crashed:
            return

        canvas.push()
        canvas.translate(self.pos.x, self.pos.y)
        # Move the rocket
        canvas.rotate(self.vel.heading())
        # If the speed is low, the image of the rocket without fire is used
        if self.vel.length() < 1 or self.reached:
            img = 'rocket-idle.png'
        else:
            img = 'rocket-moving.png'
        canvas.create_image(0, 0, IMAGE_DIR + img)
        canvas.pop()
