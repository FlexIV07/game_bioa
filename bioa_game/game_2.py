import pygame
import random
from pygame.sprite import Sprite, GroupSingle
import game_3

pygame.init()

tamanho = 800, 600

canvas = pygame.display.set_mode(
                            size=tamanho,
                            display=1
                         )

pygame.display.set_caption(
                    'Fase 2'
                  )

background = pygame.transform.scale(
                                    pygame.image.load('images/level_2_bg.png'),
                                    tamanho
                                   )

passaro = pygame.transform.scale(
                                pygame.image.load('images/woody_down.png'),
                                (70, 70)
                                   )

def menu(death_count):
    global points
    execute = True
    while execute:
        canvas.fill((97, 220, 225))
        font = pygame.font.Font('freesansbold.ttf', 20)
        if death_count == 0:
            text = font.render("Nesta fase você será um pássaro explorando a ilha em fase de reconstrução", True, (255, 255, 255))
            text_2 = font.render("voe para dispersar sementes", True, (255, 255, 255))
            any_key = font.render("Aperte Espaço", True, (255, 255, 255))
            textRect = text.get_rect()
            text_2Rect = text_2.get_rect()
            textRect.center = (390, 300)
            text_2Rect.center = (390, 330)
            any_keyRect = any_key.get_rect()
            any_keyRect.center = (700, 500)
            canvas.blit(text, textRect)
            canvas.blit(text_2, text_2Rect)
            canvas.blit(any_key, any_keyRect)
            canvas.blit(passaro, (350, 200))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    execute = False
            enter = pygame.key.get_pressed()
            if enter[pygame.K_SPACE]:
                run()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        execute = False
        elif death_count != 0:
            text_death = font.render("Sua pontuação: " + str(points), True, (255, 255, 255))
            any_key_death = font.render("Aperte enter", True, (255, 255, 255))
            text_deathRect = text_death.get_rect()
            text_deathRect.center = (385, 300)
            any_key_deathRect = any_key_death.get_rect()
            any_key_deathRect.center = (700, 500)
            canvas.blit(text_death, text_deathRect)
            canvas.blit(any_key_death, any_key_deathRect)
            print('passei aqui')
            canvas.blit(passaro, (350, 200))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    execute = False
            enter = pygame.key.get_pressed()
            if enter[pygame.K_SPACE]:
                run()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        execute = False


class Bird(Sprite):
    """Classe de negócios do objeto bird."""

    x_pos = 80
    y_pos = 300
    JUMP_VEL = 5
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(
                                        pygame.image.load('images/woody_down.png'),
                                        (70, 70)
                                           )
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.jump_vel = self.JUMP_VEL
        self.bird_jump = False
        self.bird_fall = True

    def update(self, user_input):
        if self.bird_jump:
            self.jump()
        if self.bird_fall:
            self.fall()

        print(self.rect.x, self.rect.y)

        if user_input[pygame.K_SPACE] and not self.bird_jump:
            self.bird_jump = True
            self.bird_fall = False

    def jump(self):
        if self.bird_jump:
            self.rect.y -= 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.jump_vel = self.JUMP_VEL
            self.bird_jump = False
            self.bird_fall = True

    def fall(self):
        if self.fall:
            self.rect.y += 5

    def draw(self, canvas):
        canvas.blit(self.image, (self.rect.x, self.rect.y))


class Plant(Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/plant.png'), (300 ,300))
        self.rect = self.image.get_rect()
        self.rect.y = random.choice([0, 300])
        self.rect.x = 700
        if self.rect.y == 300:
            print('0')
            self.image = pygame.transform.rotate(self.image, 180)
        else:
            print('300')


    def update(self, obstacles):
        self.rect.x -= 10

        if self.rect.x < -self.rect.width:
            self.kill()
            self.image = pygame.transform.scale(pygame.image.load('images/plant.png'), (300 ,300))
            obstacles.pop()
            self.rect.y = random.choice([0, 300])
            self.rect.x = 700
            print(self.rect.y)
            if self.rect.y == 300:
                self.image = pygame.transform.rotate(self.image, 180)


    def draw(self, canvas):
        canvas.blit(self.image, (self.rect.x, self.rect.y))

class Points:

    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def score(self, p):

        text = self.font.render('Points: ' + str(p), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (600, 40)
        canvas.blit(text, textRect)


class Menu:
    ...




def run():
    global points, death_count
    woody = Bird()
    plant = Plant()
    run = True
    clock = pygame.time.Clock()
    obstacles = []
    points = 0
    death_count = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        canvas.blit(background, (0, 0))

        woody.draw(canvas)

        if len(obstacles) == 0:
            obstacles.append(plant)

        for obstacle in obstacles:
            obstacle.draw(canvas)
            obstacle.update(obstacles)

        if woody.rect.colliderect(plant.rect):
            run = False
            death_count = 1
            menu(death_count)

        if points == 1000:
            game_3.menu(death_count=0)

        user_input = pygame.key.get_pressed()
        points += 1
        Points().score(points)
        woody.update(user_input)
        pygame.display.update()
