import pygame, sys

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.can_shoot = True
        self.shoot_time = None

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            print('Pew pew')
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 250:
                self.can_shoot = True
        
    def update(self):
        self.input_position()
        self.laser_shoot()
        self.shoot_timer()


class Laser(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = position)

# Game init
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Star Fighter")

# Background import
bg_image = pygame.image.load('graphics/background.png').convert()

# Sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()

# Sprite creation
spaceship = Ship(spaceship_group)
laser = Laser((640,360), laser_group)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dt = clock.tick(120) / 1000

    # Background
    display_surface.blit(bg_image,(0,0))

    # Update
    spaceship_group.update()

    # Graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)

    pygame.display.update()