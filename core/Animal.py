from .StackFSM import StackFSM

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
        self.velocity = new_velocity
        return self.velocity

    def is_collized_with(self, animal):
        return (self.position[0] + self.size[0] > animal.position[0]
            and self.position[0] < animal.position[0] + animal.size[0]
            and self.position[1] + self.size[1] > animal.position[1]
            and self.position[1] < animal.position[1] + animal.size[1])
        


    def update(self, world):
        self.update_position()
