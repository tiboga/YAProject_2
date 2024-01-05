import os
import sys

import pygame

FPS = 100
pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
speed_x = 4
speed_y = 4
change = (0, 0)
direction_of_movement = ''

direction_of_movement_enemy = ''
direction_of_movement_boss = ''
enemy_attack_ready = False
health = 0  # счётчик ударов. 3удара = -1hp

moving = ''


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Plat(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(plat_group, tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, animation=None):
        super().__init__(enemy_group, tiles_group, all_sprites)
        self.animations = {'idle': animation[0], 'walk': animation[1], 'attack': animation[2]}
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.move(pos_x * tile_width, pos_y * tile_height)
        for elem in self.animations.values():
            elem.pos = self.pos

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)

    def animate(self, key):
        self.animations[key].update()
        if direction_of_movement_enemy == 'left':
            self.image = pygame.transform.flip(self.animations[key].re_img(), 1, 0)
        else:
            self.image = self.animations[key].re_img()


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, animation=None):
        super().__init__(boss_group, tiles_group, all_sprites)
        self.animations = {'idle': animation[0], 'walk': animation[1]}
        self.image = boss_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.move(pos_x * tile_width, pos_y * tile_height)

        self.pos = (pos_x, pos_y)
        for elem in self.animations.values():
            elem.pos = self.pos

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)

    def animate(self, key):
        self.animations[key].update()
        if direction_of_movement_boss == 'left':
            self.image = pygame.transform.flip(self.animations[key].re_img(), 1, 0)
        else:
            self.image = self.animations[key].re_img()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x=WIDTH // 2, pos_y=HEIGHT // 2, animation=None):
        super().__init__(player_group, all_sprites)
        self.animations = {'idle': animation[0], 'walk': animation[1], 'jump': animation[2], 'attack1': animation[3]}
        self.image = player_image
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.pos = (pos_x, pos_y)
        self.move(pos_x, pos_y)

        self.lives = 3

        self.need_left_move_for_flip = True
        self.need_right_move_for_flip = False

        for elem in self.animations.values():
            elem.pos = self.pos

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)

    def animate(self, key):
        self.animations[key].update()
        if direction_of_movement == 'left':
            self.image = pygame.transform.flip(self.animations[key].re_img(),1, 0)
            if self.need_left_move_for_flip:
                self.move(self.rect.x - 24, self.rect.y)
                self.need_left_move_for_flip = False
                self.need_right_move_for_flip = True
        else:
            self.image = self.animations[key].re_img()
            if self.need_right_move_for_flip:
                self.move(self.rect.x + 24, self.rect.y)
                self.need_right_move_for_flip = False
                self.need_left_move_for_flip = True


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)
        self.pos = (x, y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                time_rect = pygame.transform.scale(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)),
                                                   (90, 90))
                self.frames.append(pygame.transform.scale(time_rect, (75, 75)))

    def re_img(self):
        return self.image

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def reapply(self, obj):
        obj.rect.x += -self.dx
        obj.rect.y += -self.dy
        print(obj.rect.x, obj.rect.y)

    def update(self):
        global change
        if change[0] != 0 or change[1] != 0:
            self.dx = -change[0]
            self.dy = -change[1]
        change = (0, 0)
        # if self.dx != 0 or self.dy != 0:
        #     print(self.dx, self.dy)


def load_image(name, colorkey=None, scale=False):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if scale:
        image = pygame.transform.scale(image, (50, 50))
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def move(player, movement):
    global direction_of_movement
    global change
    global speed_y
    x, y = player.pos
    if movement == 'up':
        if y > 50:
            change = (0, -speed_x)
    elif movement == 'down':
        if y < level_y - 90:
            change = (0, speed_x)
    elif movement == 'left':
        if x > 50:
            change = (-speed_x, 0)
            direction_of_movement = 'left'
    elif movement == 'right':
        if x < level_x - 90:
            change = (speed_x, 0)
            direction_of_movement = 'right'
    elif movement == 'fall':
        if speed_y < 4:
            speed_y += 1
        if moving == 'right':
            change = (speed_x - 1, speed_y)
        elif moving == 'left':
            change = (-speed_x + 1, speed_y)
        else:
            change = (0, speed_y)


def generate_level(level):
    new_player, new_enemy, new_boss, x, y = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Plat('wall', x, y)
            elif level[y][x] == '?':
                Tile('empty', x, y)
                new_enemy = Enemy(x, y, [enemy_idle, enemy_flight, enemy_attack])
            elif level[y][x] == '*':
                Tile('empty', x, y)
                new_boss = Boss(x, y, [boss_idle, boss_shoot])

    new_player = Player(WIDTH // 2 - 50, HEIGHT // 2 - 50, [player_idle, player_walk, player_jump, player_attack])
    return new_player, new_enemy, new_boss, WIDTH, HEIGHT


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


def enemy_movement_attack():
    global direction_of_movement_enemy
    global enemy_attack_ready
    global health
    if enemy.rect[0] - player.rect[0] < 150:
        if enemy.rect[0] - player.rect[0] >= 24:
            enemy_attack_ready = False
            direction_of_movement_enemy = ''
            if counter % 10 == 0:
                enemy.animate('walk')
                enemy.rect[0] -= 4

        else:
            if player.rect[0] - enemy.rect[0] < 150:
                if counter % 10 == 0:
                    enemy.animate('walk')
                    enemy_attack_ready = True
                if player.rect[0] - enemy.rect[0] >= 44:
                    if counter % 10 == 0:
                        enemy.rect[0] += 4
                    direction_of_movement_enemy = 'left'
                    enemy_attack_ready = True
            else:
                if counter % 17 == 0:
                    enemy.animate('idle')
                    enemy_attack_ready = False
    else:
        if counter % 17 == 0:
            enemy.animate('idle')
            enemy_attack_ready = False

    if enemy_attack_ready:
        if counter % 17 == 0:
            enemy.animate('attack')
            health += 1
            if health == 6:
                player.lives -= 1
                health = 0


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
plat_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

player_idle = AnimatedSprite(load_image('Woodcutter_idle.png'), 4, 1, WIDTH // 2, HEIGHT // 2)
player_image = player_idle.frames[0]
player_walk = AnimatedSprite(load_image('Woodcutter_walk.png'), 6, 1, WIDTH // 2, HEIGHT // 2)
player_jump = AnimatedSprite(load_image('Woodcutter_jump.png'), 6, 1, WIDTH // 2, HEIGHT // 2)
player_attack = AnimatedSprite(load_image('Woodcutter_attack1.png'), 6, 1, WIDTH // 2, HEIGHT // 2)
tile_width = tile_height = 50

enemy_idle = AnimatedSprite(load_image("Enemy_movement/Enemy_idle.png"), 4, 1, 0, 0)
enemy_image = enemy_idle.frames[0]
enemy_flight = AnimatedSprite(load_image("Enemy_movement/Enemy_walk.png"), 4, 1, 0, 0)
enemy_attack = AnimatedSprite(load_image("Enemy_movement/Enemy_attack.png"), 4, 1, 0, 0)

boss_idle = AnimatedSprite(load_image("Boss_movement/Boss_idle.png"), 4, 1, 0, 0)
boss_image = boss_idle.frames[0]
boss_shoot = AnimatedSprite(load_image("Boss_movement/Boss_shoot.png"), 3, 1, 0, 0)

heart = pygame.image.load("data/Health.png")

tile_width = tile_height = 50

player = None
enemy = None
boss = None  # группы спрайтов

level_map = load_level('map.txt')

player, enemy, boss, level_x, level_y = generate_level(load_level('map.txt'))


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
    counter = 0
    enemy_anim_count = 0
    running = True
    current_press = ''
    attack = ''
    counter_atack_anim = 0
    reapp = False

    while running:
        enemy_movement_attack()

        if player.lives == 3:
            screen.blit(heart, (100, 100))

        if change != (0, 0):
            print(change)

        move(player, 'fall')

        already_do = False
        if attack == '1':
            already_do = True
            if counter % 10 == 0 and counter_atack_anim != 6:
                player.animate('attack1')
                counter_atack_anim += 1
            if counter_atack_anim == 6:
                attack = ''
        if not already_do:
            if current_press == 'w':
                if counter % 2 == 0:
                    move(player, 'up')
                    already_do = True
                    if counter % 5 == 0:
                        player.animate('walk')
            if current_press == 's':
                if counter % 2 == 0:
                    move(player, 'down')
                    already_do = True
                    if counter % 5 == 0:
                        player.animate('walk')
            if current_press == 'a':
                if counter % 2 == 0:
                    move(player, 'left')
                    already_do = True
                    if counter % 5 == 0:
                        player.animate('walk')
            if current_press == 'd':
                if counter % 2 == 0:
                    move(player, 'right')
                    already_do = True
                    if counter % 5 == 0:
                        player.animate('walk')
            if current_press == 'j':
                if counter % 15 == 0:
                    player.animate('jump')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    move(player, 'up')
                    current_press = 'w'
                    already_do = True
                    player.animate('walk')
                if event.key == pygame.K_s:
                    move(player, 'down')
                    current_press = 's'
                    already_do = True
                    player.animate('walk')
                if event.key == pygame.K_a:
                    move(player, 'left')
                    current_press = 'a'
                    moving = 'left'
                    already_do = True
                    player.animate('walk')
                if event.key == pygame.K_d:
                    move(player, 'right')
                    current_press = 'd'
                    moving = 'right'
                    already_do = True
                    player.animate('walk')

                if event.key == pygame.K_SPACE:
                    speed_y = -16
                    current_press = 'j'
                    already_do = True
                    player.animate('jump')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.animate('attack1')
                    attack = '1'
                    counter_atack_anim = 0
            if event.type == pygame.KEYUP:
                current_press = ''
                moving = ''
                counter = 0
                Counter_ticks = False
            if event.type == pygame.MOUSEBUTTONUP:
                if counter_atack_anim > 5:
                    attack = ''
        counter += 1

        # изменяем ракурс камеры
        camera.update()
        # обновляем положение всех спрайтов
        for sprite in tiles_group:
            camera.apply(sprite)
        for elem in plat_group:
        # if pygame.sprite.spritecollideany(player, plat_group):
            if pygame.sprite.collide_mask(elem, player):
                reapp = True
            if pygame.sprite.collide_mask(elem, player) and counter_atack_anim < 6:
                pass
        if reapp:
            for sprite in tiles_group:
                camera.reapply(sprite)
            reapp = False
        camera.dx = 0
        camera.dy = 0
        if counter % 15 == 0 and (not already_do or counter_atack_anim == 6):
            player.animate('idle')
        screen.fill('black')
        tiles_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        boss_group.draw(screen)

        pygame.display.flip()
        clock.tick(100)
