import pygame
from time import sleep
import random
import sys

from utils import get_nearest_point, calculate_velocity

class StackFSM:
    def __init__(self):
        self.stack = []

    def update(self, *args, **kwargs):
        stateFn = self.getCurrentState()
        if stateFn is not None:
            stateFn(*args, **kwargs)

    def getCurrentState(self):
        return self.stack[-1] if len(self.stack) else None

    def popState(self):
        return self.stack.pop()

    def pushState(self, state):
        if state != self.getCurrentState():
            self.stack.append(state)


class Animal:
    def __init__(
            self, 
            position=(0, 0),
            velocity=(1, 1),
            speed=1,
            health=1):

        self.health = health
        self.position = position
        self.size = (5, 5)
        self.velocity = velocity
        self.speed = speed
        self.brain = StackFSM()
        self.hidden = False

    def hide(self):
        self.hidden = True


    def get_current_stats(self):
        return {
            'health': self.health
        }

    def update_position(self):
        new_position_x = self.position[0] + self.velocity[0] * self.speed
        new_position_y = self.position[1] + self.velocity[1] * self.speed
        self.position = (new_position_x, new_position_y)
        return self.position

    def set_velocity(self, new_velocity):
        # print("new_velocity", new_velocity)
        self.velocity = new_velocity
        return self.velocity

    def is_collized_with(self, animal):
        return (self.position[0] + self.size[0] > animal.position[0]
            and self.position[0] < animal.position[0] + animal.size[0]
            and self.position[1] + self.size[1] > animal.position[1]
            and self.position[1] < animal.position[1] + animal.size[1])
        


    def update(self, world):
        self.update_position()



class Ant(Animal):
    def __init__(self, 
            position=(0, 0), 
            velocity=(1, 1),
            speed=1,
            health=1):

        super(Ant, self).__init__(position, velocity, speed, health)
        self.storage = []
        self.size = (10, 10)
        self.color = (255, 0, 0)
        self.brain.pushState(self.find_plant)
        self.home = None

    def setHome(self, home):
        self.home = home

    def find_plant(self, world):
        plants = list(filter(lambda x: isinstance(x, Plant), world.entities))

        # if no more plants, go home
        if len(plants) == 0:
            self.brain.popState()
            self.brain.pushState(self.go_home)
            self.set_velocity((0, 0))
            return

        # if plant is near grab it 
        found_plant = False
        for plant in plants:
            if self.is_collized_with(plant):
                self.brain.popState()
                self.brain.pushState(self.add_plant_into_pocket)
                found_plant = True
        if found_plant:
            self.set_velocity((0, 0))
            return

        # if plants away, find nearest plant and go for it
        plant_coords = list(map(lambda x: x.position, plants))
        nearest_plant = get_nearest_point(self.position, plant_coords)
        velocity = calculate_velocity(self.position, nearest_plant, self.speed)
        self.set_velocity(velocity)


    def add_plant_into_pocket(self, world):
        added = False
        plants = list(filter(lambda x: isinstance(x, Plant) and not x.hidden, world.entities))
        for plant in plants:
            if self.is_collized_with(plant):
                self.storage.append(Payload())
                plant.hide()
                added = True

        if added:
            self.brain.popState()
            self.brain.pushState(self.go_home)
            self.set_velocity((0, 0))



    def go_home(self, world):
        if not self.is_collized_with(self.home):
            velocity = calculate_velocity(self.position, self.home.position, self.speed)
            self.set_velocity(velocity)
        else:
            self.brain.popState()
            self.brain.pushState(self.find_plant)
            self.set_velocity((0, 0))



    def update(self, world):
        action = self.brain.update(world)
        self.update_position()
        

class Plant(Animal):
    def __init__(self, *args, **kwargs):
        super(Plant, self).__init__(*args, **kwargs)
        self.size = (5, 5)
        self.color = (0, 255, 0)
        
    def update(self, world):
        pass


class Payload:
    pass

class Home(Animal):
    def update(self, world):
        pass

    def __init__(self, *args, **kwargs):
        super(Home, self).__init__(*args, **kwargs)
        self.size = (15, 15)
        self.color = (0, 0, 255)


class World:
    def __init__(self, height, width):
        self.entities = []
        self.height = height
        self.width = width

    def add_entity(self, entity):
        self.entities.append(entity)

    def update(self):
        ants = list(filter(lambda x: isinstance(x, Ant), self.entities))
        plants = list(filter(lambda x: isinstance(x, Plant), self.entities))

        hidden = []

        for entity in plants+ants:
            entity.update(self)
            if entity.hidden:
                hidden.append(entity)

        for h in hidden:
            self.entities.remove(h)


    def render(self, screen):
        screen.fill((0,0,0))

        ants = list(filter(lambda x: isinstance(x, Ant), self.entities))
        plants = list(filter(lambda x: isinstance(x, Plant), self.entities))
        homes = list(filter(lambda x: isinstance(x, Home), self.entities))

        for entity in ants:
            r = pygame.draw.rect(screen, entity.color, pygame.Rect(*entity.position, *entity.size))

        for entity in plants:
            r = pygame.draw.rect(screen, entity.color, pygame.Rect(*entity.position, *entity.size))

        for entity in homes:
            r = pygame.draw.rect(screen, entity.color, pygame.Rect(*entity.position, *entity.size))
        
        pygame.display.update()

def main():
    DEBUG = '--debug' in sys.argv

    size = height, width = 480, 480
    world = World(height, width)
    screen = pygame.display.set_mode(size)
    screen.fill((0,0,0))
    
    home = Home(position=(0, 0))
    home2 = Home(position=(465, 465))

    ant = Ant(position=home.position, speed=3)
    ant2 = Ant(position=home2.position, speed=3)
    ant.setHome(home)
    ant2.setHome(home2)
    
    
    world.add_entity(ant)
    world.add_entity(ant2)
    world.add_entity(home)
    world.add_entity(home2)

    for i in range(100):
        plant = Plant(position=(random.randint(10, 450), random.randint(10, 450)))
        world.add_entity(plant)

    running = True
    update = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False

            if DEBUG and event.type in (pygame.KEYDOWN, pygame.KEYUP):
                update = pygame.key.get_pressed()[pygame.K_SPACE]
                    
        if not DEBUG or update:
            world.update()
            world.render(screen)
            sleep(1/25)

if __name__ == '__main__':
    main()






        



