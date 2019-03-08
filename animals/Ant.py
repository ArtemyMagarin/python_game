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
