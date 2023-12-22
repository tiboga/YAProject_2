import os
import sys

import pygame

FPS = 100
pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
speed_x = 4
change = (0,0)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x=WIDTH // 2, pos_y=HEIGHT // 2):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (250, 250)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, player):
        global change
        if change[0] != 0 or change[1] != 0:
            self.dx = -change[0] * 1.5
            self.dy = -change[1] * 1.5
        change = (0, 0)
        if self.dx != 0:
            print(self.dx, self.dy)



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


def move(player, movement):
    global change
    x, y = player.pos
    # if movement == 'jump':
    if movement == 'up':
        if y > 50:
            change = (0, -speed_x)
    elif movement == 'down':
        if y < level_y - 90:
            change = (0, speed_x)
    elif movement == 'left':
        if x > 50:
            change = (-speed_x, 0)
    elif movement == 'right':
        if x < level_x - 90:
            change = (speed_x, 0)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
    new_player = Player(250, 250)
    new_player.move(250, 250)
    # вернем игрока, а также размер поля в клетках
    return new_player, WIDTH, HEIGHT


def terminate():
    pygame.quit()
    sys.exit()


clock = pygame.time.Clock()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('texture_fon.png')
}
player_image = load_image('Woodcutter.png')

tile_width = tile_height = 50

player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

level_map = load_level('map.txt')

player, level_x, level_y = generate_level(load_level('map.txt'))


def start_screen():
    intro_text = []

    fon = pygame.transform.scale(load_image('title.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
    camera = Camera()
    Counter_ticks = False
    counter = 0
    running = True
    current_press = ''
    jump = False
    while running:
        if current_press == 'w':
            if counter == 2:
                move(player, 'up')
                counter = 0
        if current_press == 's':
            if counter == 2:
                move(player, 'down')
                counter = 0
        if current_press == 'a':
            if counter == 2:
                move(player, 'left')
                counter = 0
        if current_press == 'd':
            if counter == 2:
                move(player, 'right')
                counter = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    move(player, 'up')
                    current_press = 'w'
                    counter = 0
                    Counter_ticks = True
                elif event.key == pygame.K_s:
                    move(player, 'down')
                    current_press = 's'
                    counter = 0
                    Counter_ticks = True
                elif event.key == pygame.K_a:
                    move(player, 'left')
                    current_press = 'a'
                    counter = 0
                    Counter_ticks = True
                elif event.key == pygame.K_d:
                    move(player, 'right')
                    current_press = 'd'
                    counter = 0
                    Counter_ticks = True

                elif event.key == pygame.K_SPACE:
                    move(player, 'jump', speed=20)

            elif event.type == pygame.KEYUP:
                current_press = ''
                counter = 0
                Counter_ticks = False
        if Counter_ticks:
            counter += 1

        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in tiles_group:
            camera.apply(sprite)
        camera.dx = 0
        camera.dy = 0
        screen.fill('black')
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(100)
        if change[0] != 0:
            print(change)
