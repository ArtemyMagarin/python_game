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
