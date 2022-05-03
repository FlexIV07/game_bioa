"""Fase 3."""
import pygame

pygame.init()

tamanho = 800, 600
x_pos_g = 0
y_pos_g = 400

canvas = pygame.display.set_mode(size=tamanho, display=1)

pygame.display.set_caption('Fase 3')

background = pygame.transform.scale(
                                    pygame.image.load('images/bg_game_3.png'),
                                    tamanho
                                   )

ground_img = pygame.transform.scale(pygame.image.load('images/ground.png'), (800, 200))

running = [
        pygame.transform.scale(pygame.image.load('images/monkey_1.png'), (80, 80)),
        pygame.transform.scale(pygame.image.load('images/monkey_2.png'), (80, 80))
          ]

worm = [
        pygame.transform.scale(pygame.image.load('images/enemy.png'), (80, 60)),
        pygame.transform.scale(pygame.image.load('images/enemy_1.png'), (80, 60))
          ]

def ground():
    global x_pos_g, y_pos_g
    image_width = ground_img.get_width()
    canvas.blit(ground_img, (x_pos_g, y_pos_g))
    canvas.blit(ground_img, (image_width + x_pos_g, y_pos_g))
    if x_pos_g <= -image_width:
        canvas.blit(ground_img, (image_width + x_pos_g, y_pos_g))
        x_pos_g = 0
    x_pos_g -= 5

def menu(death_count):
    global points
    execute = True
    while execute:
        canvas.fill((204, 175, 240))
        font = pygame.font.Font('freesansbold.ttf', 20)
        if death_count == 0:
            text = font.render("Nesta fase você será um macaco em uma ilha totalmente reconstruída,", True, (255, 255, 255))
            text_2 = font.render("corra para explorar esse novo ambiente", True, (255, 255, 255))
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
            canvas.blit(running[1], (350, 200))
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
            any_key_death = font.render("Aperte Espaço", True, (255, 255, 255))
            text_deathRect = text_death.get_rect()
            text_deathRect.center = (390, 300)
            any_key_deathRect = any_key_death.get_rect()
            any_key_deathRect.center = (700, 500)
            canvas.blit(text_death, text_deathRect)
            canvas.blit(any_key_death, any_key_deathRect)
            print('passei aqui')
            canvas.blit(running[1], (350, 200))
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



class Monkey():
    x_pos = 80
    y_pos = 390
    JUMP_VEL = 9

    def __init__(self):
        self.run_img = running

        self.monkey_run = True
        self.monkey_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.step_index += 1

    def jump(self):
        self.image = self.run_img[0]
        if self.monkey_jump:
            self.rect.y -= self.jump_vel * 5
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.monkey_jump = False
            self.monkey_run = True
            self.jump_vel = self.JUMP_VEL

    def update(self, user_input):
        if self.monkey_run:
            self.run()
        if self.monkey_jump:
            self.jump()

        if user_input[pygame.K_SPACE] and not self.monkey_jump:
            self.monkey_jump = True
            self.monkey_run = False

        if self.step_index >= 10:
            self.step_index = 0

    def draw(self, canvas):
        canvas.blit(self.image, (self.rect.x, self.rect.y))

class Worm():
    x_pos = 800
    y_pos = 405

    def __init__(self):

        self.image = worm
        self.rect = self.image[0].get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.index = 0

    def update(self, obstacles):
        self.rect.x -= 10
        if self.rect.x < -self.rect.width:
            obstacles.pop()
            self.rect.x = self.x_pos

    def draw(self, canvas):
        if self.index >= 9:
            self.index = 0
        canvas.blit(self.image[self.index//5], self.rect)
        self.index += 1


class Points:

    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def score(self, p):

        text = self.font.render('Points: ' + str(p), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (600, 40)
        canvas.blit(text, textRect)



def run():
    global points, death_count
    ran = True
    mamaco = Monkey()
    minhoca = Worm()
    clock = pygame.time.Clock()
    obstacles = []
    points = 0
    while ran:
        clock.tick(30)
        canvas.blit(background, (0, 0))
        ground()
        mamaco.draw(canvas)

        if len(obstacles) == 0:
            print('opa')
            obstacles.append(minhoca)

        for obstacle in obstacles:
            obstacle.draw(canvas)
            obstacle.update(obstacles)
            if mamaco.rect.colliderect(obstacle.rect):
                death_count = 1
                menu(death_count)
                print('perdeu')
                pygame.draw.rect(canvas, (255, 0, 0), mamaco.rect, 2)
                print(death_count)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ran = False

        user_input = pygame.key.get_pressed()

        Points().score(points)
        points += 1
        mamaco.update(user_input)
        pygame.display.update()
