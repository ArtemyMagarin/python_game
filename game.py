import pygame
from time import sleep
import random
import sys

from utils import get_nearest_point, calculate_velocity

from core import StackFSM, Animal, World

# 
# todo: create new class Object
# todo: create new classes недвижимое существо, стена
# сделать генератор карт
# 

        

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






        



