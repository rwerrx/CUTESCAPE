import pygame

from time import time

pygame.init()

d_width = 800
d_height = 600
display = pygame.display.set_mode((d_width, d_height))

character_width = 60
character_height = 100
character_x = d_width // 3
character_y = d_height - character_height - 100

clock = pygame.time.Clock()
do_jump = False
jumping_counter = 30

object_width = 20
object_height = 70
object_x = d_width - 50
object_y = d_height - object_height - 100

jump_time = 0


def jump():
    global character_y, do_jump, jumping_counter
    if jumping_counter >= -30:
        character_y -= jumping_counter / 2.5
        jumping_counter -= 1
    else:
        jumping_counter = 30
        do_jump = False


def on_button_jump():
    global jump_time
    if time() - jump_time >= 2:  # duration длительность одного прыжка
        jump()  # second jump
        jump_time = 0  # запрет третьего прыжка
    else:
        jump()  # first jump
        jump_time = time()


def draw_object():
    global object_x, object_y, object_width, object_height

    if object_x >= -object_width:
        pygame.draw.rect(display, (143, 34, 67), (object_x, object_y, object_width, object_height))
        object_x -= 4
    else:
        object_x = d_width - 50


def game_constructor():
    game = True

    while game:
        global do_jump, jumping_counter, character_y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:

            if do_jump !=2:
                if time()>0.020 and time()<2: #0020 здесь время автонажатия
                    do_jump=  1
                    'only click'
                else:
                    do_jump=2 #заглушка, чтобы двойной клик не сбрасывался на одинарный
                    'double click'
            oldtime=time()

        if do_jump:
            jump()

        display.fill((255, 255, 255))
        draw_object()
        pygame.draw.rect(display, (49, 52, 78), (character_x, character_y, character_width, character_height))
        pygame.display.update()

        clock.tick(60)


game_constructor()