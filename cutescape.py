import pygame
import os
import sys
from random import choice, randrange

pygame.init()
size = w, h = 1000, 420
pygame.display.set_caption('runner')
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()

runner_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
background_group = pygame.sprite.Group()

play_but = pygame.Surface([200, 50])
play_fon = pygame.Surface([800, 600])
stop = pygame.Surface([400, 300])
monsters = ['wmonsterrun4.png', 'rmonsterrun4.png']
robots = ['wrobotrun3.png', 'grobotrun4.png']
s = [700]

WHITE = pygame.Color('white')
BLACK = pygame.Color('black')

FPS = 30
clock = pygame.time.Clock()

columns = 6
rows = 1

x, y = 100, 350

scores = 0
cnt_runner = 0
cnt_monsters = 0
cnt2 = 0
cnt_sc = [0]
cnt_rd = 0
speed = -15

f = False
f2 = False
run = True


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global f2
    intro_text = ["CUTIESCAPE"]
    hl_text = ['PLAY HARD LEVEL']
    el_text = ['PLAY EASY LEVEL']
    fon = pygame.transform.scale(load_image('background2.png'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    pb_font = pygame.font.Font(None, 30)
    text_coord = 50

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 100
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    for line in hl_text:
        play_but.fill(pygame.Color('#2E8B57'))
        but_x2 = 100
        but_y2 = 300
        screen.blit(play_but, (but_x2, but_y2))
        string_rendered = pb_font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 135
        intro_rect.top = text_coord
        intro_rect.x = 110
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    for line in el_text:
        play_but.fill(pygame.Color('#2E8B57'))
        but_x = 100
        but_y = 200
        screen.blit(play_but, (but_x, but_y))
        string_rendered = pb_font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += -125
        intro_rect.top = text_coord
        intro_rect.x = 110
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RETURN]:
                return

            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if but_x < pos[0] < but_x + 200 and but_y < pos[1] < but_y + 50:
                    f2 = True
                    return

                elif but_x2 < pos[0] < but_x2 + 200 and but_y2 < pos[1] < but_y2 + 50:
                    f2 = False
                    return

        pygame.display.flip()
        clock.tick(FPS)


def text(message, x, y, font_type=None, font_size=30):
    global f2
    if f2:
        col = pygame.Color('black')
    else:
        col = pygame.Color('#2E8B57')
    font_type = pygame.font.Font(font_type, font_size)
    t = font_type.render(message, True, col)
    screen.blit(t, (x, y))


start_screen()


class Background(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__(all_sprites, background_group)
        if f2:

            self.image = pygame.transform.scale(load_image('background1.png'), (w, h))
            self.rect = self.image.get_rect()
            self.rect.bottom = h
        else:
            self.image = pygame.transform.scale(load_image('background2.png'), (w, h))
            self.rect = self.image.get_rect()
            self.rect.bottom = h


def stopped(lt):
    font = pygame.font.Font(None, 50)
    text_coord = 100
    n = 100
    for line in lt:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        n += 20
        intro_rect.x += n
        screen.blit(string_rendered, intro_rect)


def withdrawal_of_records():
    file = open('results.txt', 'w', encoding='utf8')
    file.write(f'record: {max(cnt_sc)}')
    file.close()


class White(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(obstacles_group, all_sprites)
        self.frames = []
        self.columns = 4
        self.rows = 1
        self.sheet = pygame.transform.scale(pygame.transform.flip(load_image(choice(monsters)), True, False),
                                            (400, 120))
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(1000, y)
        self.cnt = cnt_monsters
        self.cnt_rd = cnt_rd
        self.speed = speed

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, -50, sheet.get_width() // columns,
                                sheet.get_height())
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if self.cnt % 4 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
        if f2:
            self.speed = -15
        else:
            self.speed = -25
        self.rect = self.rect.move(speed, 0)
        if self.rect.x < -300:
            self.rect.x = randrange(1000, 1200)
            self.sheet = pygame.transform.scale(pygame.transform.flip(load_image(choice(monsters)), True, False),
                                                (120, 120))
        self.cnt += 1


class WhiteRobot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(obstacles_group, all_sprites)
        self.frames = []
        self.columns = 3
        self.rows = 1
        self.sheet = pygame.transform.scale(pygame.transform.flip(load_image('wrobotrun3.png'), True, False),
                                            (400, 120))
        self.columns = 3
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(1500, y)
        self.cnt = cnt_monsters
        self.speed = speed

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, -50, sheet.get_width() // columns,
                                sheet.get_height())
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if self.cnt % 4 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
        if f2:
            self.speed = -15
        else:
            self.speed = -25
        self.rect = self.rect.move(speed, 0)
        if self.rect.x < -300:
            self.rect.x = randrange(2000, 2800)
        self.cnt += 1


class GreenRobot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(obstacles_group, all_sprites)
        self.frames = []
        self.columns = 3
        self.rows = 1

        self.sheet = pygame.transform.scale(pygame.transform.flip(load_image('grobotrun4.png'), True, False),
                                            (400, 120))
        self.columns = 4

        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(1700, y)
        self.cnt = cnt_monsters
        self.speed = speed

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, -50, sheet.get_width() // columns,
                                sheet.get_height())
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if self.cnt % 4 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
        if f2:
            self.speed = -15
        else:
            self.speed = -25
        self.rect = self.rect.move(speed, 0)
        if self.rect.x < -300:
            self.rect.x = randrange(3000, 3200)
        self.cnt += 1


m_white = White()
robot = WhiteRobot()
robot2 = GreenRobot()


class Runner(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(runner_group, all_sprites)
        self.isJump = False
        self.jumpCount = 10
        sheet = pygame.transform.scale(load_image('omrun_6.png'), (500, 100))
        columns = 6
        self.frames = []
        self.cut_sheet(sheet, columns)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.rect.midbottom = (250, h)
        self.cnt = cnt_runner
        self.col = False
        self.mask = pygame.mask.from_surface(self.image)
        self.cnt_rd = cnt_rd

    def cut_sheet(self, sheet, columns):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height())
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args) -> None:
        global cnt2, f, run
        if self.cnt % 2 == 0 and self.isJump is False:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.isJump = True
        if self.isJump is True:
            if self.jumpCount >= -10:
                if self.jumpCount < 0:
                    self.rect.y += (self.jumpCount ** 2) // 2
                else:
                    self.rect.y -= (self.jumpCount ** 2) // 2
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10
        self.cnt += 1
        collided = pygame.sprite.spritecollideany(self, obstacles_group)
        if collided:
            if pygame.sprite.collide_mask(self, collided):
                if f2:

                    collided.rect.x += 15
                else:
                    collided.rect.x += 30
                f = True


def final_screen():
    global scores, run, f, f2, cnt2
    intro_text = ["GAME OVER"]
    hl_text = ['PLAY AGAIN']
    el_text = ['OUTPUT RECORD']
    pb_font = pygame.font.Font(None, 30)
    if f2:
        fon = pygame.transform.scale(load_image('background1.png'), (w, h))
    else:
        fon = pygame.transform.scale(load_image('background2.png'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50

    for line in intro_text:
        if f2:
            col = pygame.Color('#2E8B57')
        else:
            col = pygame.Color('black')
        string_rendered = font.render(line, 1, col)
        intro_rect = string_rendered.get_rect()
        text_coord += 0
        intro_rect.top = text_coord
        intro_rect.x = 130
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        font = pygame.font.Font(None, 50)
        text_coord = 50
        cnt_sc.append(int(scores))
        text(f'PRESS ENTER TO PLAY AGAIN, record: {str(max(cnt_sc))}, TO DISPLAY THE RESULTS IN A TXT FILE, PRESS 1',
             50, 100)

        for line in hl_text:
            play_but.fill(pygame.Color('#2E8B57'))
            but_x2 = 100
            but_y2 = 300
            screen.blit(play_but, (but_x2, but_y2))
            string_rendered = pb_font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 265
            intro_rect.top = text_coord
            intro_rect.x = 110
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        for line in el_text:
            play_but.fill(pygame.Color('#2E8B57'))
            but_x = 100
            but_y = 200
            screen.blit(play_but, (but_x, but_y))
            string_rendered = pb_font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += -125
            intro_rect.top = text_coord
            intro_rect.x = 110
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():

            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run = False
                f = False

            if keys[pygame.K_ESCAPE]:
                run = False
                f = False

            if keys[pygame.K_RETURN]:
                m_white.rect.x += randrange(1100, 1300)
                robot.rect.x += randrange(1500, 1700)
                f = False

            if keys[pygame.K_1]:
                withdrawal_of_records()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if but_x2 < pos[0] < but_x2 + 200 and but_y2 < pos[1] < but_y2 + 50:
                    m_white.rect.x += randrange(1100, 1300)
                    robot.rect.x += randrange(1500, 1700)
                    robot2.rect.x += randrange(1800, 1900)
                    f = False
                if but_x < pos[0] < but_x + 200 and but_y < pos[1] < but_y + 50:
                    withdrawal_of_records()

        cnt2, scores = 0, 0
        pygame.display.flip()


background = Background()
runner = Runner()

while run:

    screen.fill(BLACK)
    cnt2 += 1
    clock.tick(FPS)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            runner.update(event.key)

        if keys[pygame.K_2]:
            paused = True

            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        paused = False

                text('PRESS ENTER TO  CONTINUE THE GAME', 100, 100)
            pygame.display.flip()

    runner.update()
    m_white.update()
    robot.update()
    robot2.update()
    all_sprites.draw(screen)
    scores = cnt2 // 10
    text('scores: ' + str(scores), 800, 30)
    obstacles_group.draw(screen)

    while f:
        final_screen()

    pygame.display.flip()
pygame.quit()
quit()
