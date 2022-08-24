import pygame, sys
from random import randint, uniform

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
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

            Laser(self.rect.midtop, laser_group)

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

        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0,-1)
        self.speed = 600

    def update(self):
        self.position += self.direction * self.speed * dt
        self.rect.topleft = (round(self.position.x),round(self.position.y))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        # Basic setup
        super().__init__(groups)

        meteor_surface = pygame.image.load('graphics/meteor.png').convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surface.get_size()) * uniform(0.5,1.5) 
        self.scaled_surface = pygame.transform.scale(meteor_surface,meteor_size)
        self.image = self.scaled_surface
        self.rect = self.image.get_rect(center = position)

        # Positioning
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,600)

        # Rotation logic
        self.rotation = 0
        self.rotation_speed = randint(10,40)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_meteor = pygame.transform.rotozoom(self.scaled_surface, self.rotation, 1)
        self.image = rotated_meteor
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self):
        self.position += self.direction * self.speed * dt
        self.rect.topleft = (round(self.position.x), round(self.position.y))
        self.rotate()

class Score():
    def __init__(self) -> None:
        self.font = pygame.font.Font('graphics/subatomic.ttf', 48)
    
    def display(self) -> None:
        score_text = f'Score : {pygame.time.get_ticks() // 1000}'
        score_surf = self.font.render(score_text, True, (200,200,200))
        score_rect = score_surf.get_rect(topright = (WINDOW_WIDTH-20,20))
        display_surface.blit(score_surf, score_rect)
        pygame.draw.rect(
            display_surface, 
            (200,200,200), 
            score_rect.inflate(20,20), 
            width = 1, 
            border_radius= 3
            )

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
meteor_group = pygame.sprite.Group()

# Sprite creation
spaceship = Ship(spaceship_group)

# Meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,500)

# Score
score = Score()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == meteor_timer:
            x_spawn = randint(-100,WINDOW_WIDTH+100)
            y_spawn = randint(-100,-50)
            Meteor((x_spawn,y_spawn), meteor_group)

    dt = clock.tick(120) / 1000

    # Background
    display_surface.blit(bg_image,(0,0))

    # Update
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()

    # Graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    score.display()

    pygame.display.update()