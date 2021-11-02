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
            # To change the chance of parents choosing the rocket that scored more points than the others  # TODO
            number = ceil(self.rockets[i].fitness * 100)
            for _ in range(0, number):
                self.mating_pool.append(self.rockets[i])

    def selection(self):
        new_rockets = []

        for _ in self.rockets:
            parent_a = choice(self.mating_pool).dna
            parent_b = choice(self.mating_pool).dna
            child = parent_a.crossover(parent_b)
            child.mutation()
            new_rockets.append(Rocket(child))
        self.rockets = new_rockets


class DNA:
    def __init__(self, genes=None):
        if genes is None:
            self.genes = []
            for _ in range(0, ROCKET_LIFESPAN):
                self.genes.append(RandomVector())
        else:
            self.genes = genes

    def crossover(self, parent_b):
        new_genes = []
        mid_point = randint(0, ROCKET_LIFESPAN)
        for i in range(0, ROCKET_LIFESPAN):
            if i > mid_point:
                new_genes.append(self.genes[i])
            else:
                new_genes.append(parent_b.genes[i])

        return DNA(new_genes)

    def mutation(self):
        for i in range(0, ROCKET_LIFESPAN):
            if randint(1, 100) < MUTATION_RATE * 100:
                self.genes[i] = RandomVector()


class Rocket:
    def __init__(self, dna=None):
        # position
        self.pos = Vector(WIDTH // 2, HEIGHT - 40)
        # velocity
        self.vel = Vector(0, 0)
        # acceleration
        self.acc = Vector(0, 0)

        self.reached = False
        self.crashed = False
        self.alive_tick = 0

        if dna is None:
            self.dna = DNA()
        else:
            self.dna = dna
        self.fitness = 0

    def apply_force(self, force):
        self.acc += force

    def update(self, app):
        if self.crashed or self.reached:
            return
        dist = self.pos.distance_from(MARS_COORDS)
        self.alive_tick += 1
        if dist < 80:
            self.reached = True
            self.pos = MARS_COORDS
            # This means that the rocket has been alive for as long as possible
            self.alive_tick = ROCKET_LIFESPAN

        for blackhole in app.blackholes:
            if self.pos.distance_from(blackhole) < 60:
                self.crashed = True

        if self.pos.x > WIDTH or self.pos.x < 0 or self.pos.y > HEIGHT or self.pos.y < 0:
            self.crashed = True

        self.apply_force(self.dna.genes[app.lifespan_count])

        if not self.reached:
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0

    def calculate_fitness(self):
        dist = self.pos.distance_from(MARS_COORDS)
        dist = min(dist, WIDTH)

        self.fitness = WIDTH + 1 - dist
        self.fitness *= self.alive_tick ** 0.5 + 1
        if self.reached:
            self.fitness *= self.alive_tick ** 0.5 * 2
        if self.crashed:
            self.fitness /= dist ** 0.5 + 1

        self.fitness = ceil(self.fitness)

    def show(self, canvas):
        if self.crashed:
            return
        canvas.push()
        canvas.translate(self.pos.x, self.pos.y)
        canvas.rotate(self.vel.heading())
        if self.vel.length() < 1 or self.reached:
            img = 'rocket-idle.png'
        else:
            img = 'rocket-moving.png'
        canvas.create_image(0, 0, IMAGE_DIR + img)
        canvas.pop()
