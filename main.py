import os
import sys
import time
import random
import pygame

gravity = 0.25
FPS = 100
pygame.init()
size = WIDTH, HEIGHT = 750, 422
screen = pygame.display.set_mode(size)
speed_x = 4
speed_y = 4
change = (0, 0)
direction_of_movement = ''
player_pos = (WIDTH // 2, HEIGHT // 2)
direction_of_movement_enemy = ''
direction_of_movement_boss = 'left'
direction_of_movement_mushroom = ''
enemy_attack_ready = False
level_teleport = 1
health = 0  # счётчик ударов. 3удара = -1hp

moving = ''


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, back_group, all_sprites)
        self.image = tile_images[tile_type]
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Plat(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(plat_group, tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, animation=None):
        super().__init__(enemy_group, tiles_group, all_sprites)
        self.animations = {'idle': animation[0], 'walk': animation[1], 'attack': animation[2], 'die': animation[3],
                           'hurt': animation[4]}
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        self.lives = 3

        self.pos = (pos_x, pos_y)
        self.move(pos_x * tile_width, pos_y * tile_height)
        for elem in self.animations.values():
            elem.pos = self.pos

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)

    def attack(self):
        global health
        global direction_of_movement_enemy
        global enemy_attack_ready
        if abs(player.rect[1] - self.rect[1]) <= 4 and (
                (self.rect[0] - player.rect[0] <= 24 and self.rect[0] > player.rect[0]) or (
                player.rect[0] - self.rect[0] <= 44 and player.rect[0] > self.rect[0])):

            enemy_attack_ready = True
        else:
            if self.rect[0] - player.rect[0] < 250:
                if self.rect[0] - player.rect[0] >= 24:
                    if counter % 10 == 0:
                        self.animate('walk')
                        self.rect[0] -= 4
                    enemy_attack_ready = False
                    direction_of_movement_enemy = ''
                    if self.rect[1] > player.rect[1]:
                        if counter % 10 == 0:
                            self.animate('walk')
                            self.rect[1] -= 4

                    elif self.rect[1] < player.rect[1]:
                        if counter % 10 == 0:
                            self.animate('walk')
                            self.rect[1] += 4

                else:
                    if player.rect[0] - self.rect[0] < 250:
                        if player.rect[0] - self.rect[0] >= 44:
                            if counter % 10 == 0:
                                self.animate('walk')
                                self.rect[0] += 4
                            direction_of_movement_enemy = 'left'
                            enemy_attack_ready = False
                        if self.rect[1] > player.rect[1]:
                            if counter % 10 == 0:
                                self.animate('walk')
                                self.rect[1] -= 4

                        elif self.rect[1] < player.rect[1]:
                            if counter % 10 == 0:
                                self.animate('walk')
                                self.rect[1] += 4

                    else:
                        if counter % 17 == 0:
                            self.animate('idle')
                            enemy_attack_ready = False
            else:
                if counter % 17 == 0:
                    self.animate('idle')
                    enemy_attack_ready = False

        if enemy_attack_ready:
            if counter % 20 == 0:
                enemy.animate('attack')
                player.animate("damage")
                health += 1
                if health == 6:
                    player.lives -= 1
                    health = 0

    def animate(self, key):
        self.animations[key].update()
        if direction_of_movement_enemy == 'left':
            self.image = pygame.transform.flip(self.animations[key].re_img(), 1, 0)
        else:
            self.image = self.animations[key].re_img()


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, animation=None):
        super().__init__(boss_group, tiles_group, all_sprites)
        self.animations = {'idle': animation[0], 'hurt': animation[1], 'die': animation[2]}
        self.image = boss_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 20)
        self.move(pos_x * tile_width, pos_y * tile_height - 20)

        self.live = 3

        self.i = 1
        self.pos = (pos_x, pos_y)
        self.attack_x, self.attack_y = self.rect[0], self.rect[1] + 60
        for elem in self.animations.values():
            elem.pos = self.pos

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)

    def attack(self):
        if counter % 20 == 0:
            boss_s.animate('idle')
        self.attack_y = self.rect[1] + 40

        if boss_s.rect[0] - player.rect[0] < 250:
            if counter % 10 == 0:
                boss_attack.get_rect().move(self.attack_x, self.attack_y)

            if self.attack_x < 0:
                self.attack_x = self.rect[0]
                self.i = 1

        if counter % 10 == 0:
            self.attack_x = self.rect[0] - (4 * self.i)
            self.i += 1

        if abs(player.rect[0] - self.attack_x) < 4 and abs(self.attack_y - player.rect[1]) < 50:
            player.animate('damage')
            player.lives -= 1
            self.attack_x = self.rect[0]
            self.i = 1

    def animate(self, key):
        self.animations[key].update()
        if direction_of_movement_boss == 'left':
            self.image = pygame.transform.flip(self.animations[key].re_img(), 1, 0)
        else:
            self.image = self.animations[key].re_img()


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, animation=None):
        super().__init__(mushroom_group, tiles_group, all_sprites)
        self.animations = {'walk': animation[0], 'boom': animation[1]}
        self.image = mushroom_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 20)
        self.move(pos_x * tile_width, pos_y * tile_height - 20)
        self.pos = (pos_x, pos_y)
        self.lives = 1
        for elem in self.animations.values():
            elem.pos = self.pos

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)

    def attack(self):
        global direction_of_movement_mushroom
        if abs(self.rect[0] - player.rect[0]) < 250:
            if abs(self.rect[0] - player.rect[0]) <= 24 and abs(self.rect[1] - player.rect[1]) <= 50:
                if counter % 20 == 0:
                    player.animate('damage')
                    player.lives -= 1
                    self.animate('boom')
                    self.lives -= 1
            else:
                direction_of_movement_mushroom = 'left'
                if self.rect[0] - player.rect[0] > 24:
                    if counter % 10 == 0:
                        self.rect[0] -= 4
                        self.animate('walk')
                else:
                    if self.rect[0] - player.rect[0] < 24:
                        if counter % 10 == 0:
                            self.rect[0] += 4
                            self.animate('walk')

    def animate(self, key):
        self.animations[key].update()
        if direction_of_movement_boss == 'left':
            self.image = pygame.transform.flip(self.animations[key].re_img(), 1, 0)
        else:
            self.image = self.animations[key].re_img()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x=WIDTH // 2, pos_y=HEIGHT // 2, animation=None):
        super().__init__(player_group, all_sprites)
        self.animations = {'idle': animation[0], 'walk': animation[1], 'jump': animation[2], 'attack1': animation[3],
                           'damage': animation[4], 'die': animation[5], 'dead': animation[6]}
        self.image = player_image
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.pos = (pos_x, pos_y)
        self.move(pos_x, pos_y)
        with open('points.txt') as f:
            self.money = int(f.readline())
        self.lives = 6

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
            self.image = pygame.transform.flip(self.animations[key].re_img(), 1, 0)
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


all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group=all_sprites, need_scale=True, scaling=(75, 75)):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, need_scale, scaling)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)
        self.pos = (x, y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)

    def cut_sheet(self, sheet, columns, rows, need_scale, scaling):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                time_rect = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                if need_scale:
                    self.frames.append(pygame.transform.scale(time_rect, scaling))
                else:
                    self.frames.append(time_rect)

    def re_img(self):
        return self.image

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(button_group)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)
        self.pos = (x, y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.fon_apply = False
        self.fon_reapply = False

    def apply(self, obj):
        obj.pos = (obj.pos[0] + self.dx,
                   obj.pos[1] + self.dy)
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def reapply(self, obj):
        obj.pos = (obj.pos[0] - self.dx,
                   obj.pos[1] - self.dy)
        obj.rect.x += -self.dx
        obj.rect.y += -self.dy

    def update(self):
        global change
        self.fon_apply = False
        self.fon_reapply = False
        if change[0] != 0 or change[1] != 0:
            self.dx = -change[0]
            self.dy = -change[1]
        change = (0, 0)


class Portal(AnimatedSprite):
    def __init__(self, level, x, y, sheet, columns, rows, group=all_sprites, need_scale=True, scaling=(75, 75)):
        super().__init__(sheet, columns, rows, x, y, group, need_scale, scaling)
        self.level = level
        self.rect = self.image.get_rect().move(
            x * tile_width, y * tile_height)
        self.frames = self.frames[:-1]

    def teleport(self):
        global player, enemy, boss_s, mushroom, level_x, level_y, level_teleport
        player, enemy, boss_s, mushroom, level_x, level_y = generate_level(self.level)
        if level_teleport == 0:
            level_teleport = 1
        else:
            level_teleport = 0
    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)


class NPC(AnimatedSprite):

    def __init__(self, sheet, columns, rows, x, y, group=all_sprites, need_scale=True, scaling=(75, 75)):
        super().__init__(sheet, columns, rows, x, y, group, need_scale, scaling)
        self.rect = self.image.get_rect().move(
            x * tile_width, y * tile_height)
        self.frames = self.frames[:]


class Coins(AnimatedSprite):
    def __init__(self, gold, sheet, columns, rows, x, y, group=all_sprites, need_scale=True, scaling=(75, 75)):
        super().__init__(sheet, columns, rows, x, y, group, need_scale, scaling)
        self.gold = gold
        self.pos = x * tile_width, y * tile_height
        self.rect = self.image.get_rect().move(
            self.pos)

    def get(self):
        player.money += self.gold

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(x, y)


class Fountain(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, group=all_sprites, need_scale=True, scaling=(75, 75)):
        super().__init__(sheet, columns, rows, x, y, group, need_scale, scaling)
        self.pos = x * tile_width, y * tile_height
        self.rect = self.image.get_rect().move(
            self.pos)

    def heal(self):
        player.lives += 1


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
    global npc, level_teleport
    new_player, new_enemy, new_boss, x, y, new_mushroom = None, None, None, None, None, None
    sdv = 5
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x - sdv, y - sdv)
            elif level[y][x] == '#':
                Plat('wall', x - sdv, y - sdv)
            elif level[y][x] == '?':
                Tile('empty', x - sdv, y - sdv)
                new_enemy = Enemy(x - sdv, y - sdv, [enemy_idle, enemy_flight, enemy_attack, enemy_die, enemy_hurt])
            elif level[y][x] == '*':
                Tile('empty', x - sdv, y - sdv)
                new_boss = Boss(x - sdv, y - sdv, [boss_idle, boss_damage, boss_die])
            elif level[y][x] == ',':
                Tile('empty', x - sdv, y - sdv)
                new_mushroom = Mushroom(x - sdv, y - sdv, [mushroom_walk, mushroom_boom])
                Tile('empty', x - sdv, y - sdv)

            elif level[y][x] == 'P':
                Tile('empty', x - sdv, y - sdv)
                Portal(levels_sp[level_teleport], x - sdv, y - sdv - 1, load_image('portal.png'), 7, 6,
                       group=[all_sprites, portal_group, tiles_group], scaling=(200, 200))

            elif level[y][x] == 'N':
                Tile('empty', x - sdv, y - sdv)
                npc = NPC(load_image('npc/Sprites/BLACKSMITH.png'), 7, 1, x - sdv, y - sdv - 0.75,
                          group=[all_sprites, npc_group, tiles_group], scaling=(100, 100))
            elif level[y][x] == 'M':
                Tile('empty', x - sdv, y - sdv)
                rand = random.choice([10, 15, 20])

                Coins(10, load_image('coins/coin_1_anim.png'), 2, 2, x - sdv, y - sdv + 0.4,
                      group=[all_sprites, tiles_group, coins_group], scaling=(25, 25))
    new_player = Player(player_pos[0], player_pos[1],
                        [player_idle, player_walk, player_jump, player_attack, player_damage, player_die, player_dead])
    return new_player, new_enemy, new_boss, new_mushroom, WIDTH, HEIGHT


def terminate():
    with open('position.txt', 'w') as f:
        f.writelines(f"{player.pos[0]} {player.pos[1]}")
    with open('points.txt', 'w') as f:
        f.writelines(str(player.money))
    end_coint = player.money * 5
    end_screen([end_coint])
    pygame.quit()
    sys.exit()


clock = pygame.time.Clock()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # max_width = max(map(len, level_map))
    return list(level_map)
    # return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("particle.png")]
    for scale in (2, 3, 4):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites, particle_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = gravity

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.y > 422:
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('texture_fon.png')
}

fountain_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
npc_group = pygame.sprite.Group()
back_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
plat_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
cursors_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
technical_sprite_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
fon_group = pygame.sprite.Group()
castle_group = pygame.sprite.Group()
fon = AnimatedSprite(load_image('fon2.png'), 1, 1, HEIGHT * 2, -300, scaling=(1200 * 1.5, 680 * 1.5),
                     group=[castle_group, tiles_group])
player_idle = AnimatedSprite(load_image('Player_movement/Woodcutter_idle.png'), 4, 1, WIDTH // 2, HEIGHT // 2,
                             scaling=(65, 65))
mushroom_group = pygame.sprite.Group()

player_idle = AnimatedSprite(load_image('Player_movement/Woodcutter_idle.png'), 4, 1, WIDTH // 2, HEIGHT // 2)
player_image = player_idle.frames[0]
player_idle = AnimatedSprite(load_image('Player_movement/Woodcutter_idle.png'), 4, 1, WIDTH // 2, HEIGHT // 2,
                             scaling=(65, 65))
player_walk = AnimatedSprite(load_image('Player_movement/Woodcutter_walk.png'), 6, 1, WIDTH // 2, HEIGHT // 2,
                             scaling=(65, 65))
player_jump = AnimatedSprite(load_image('Player_movement/Woodcutter_jump.png'), 6, 1, WIDTH // 2, HEIGHT // 2,
                             scaling=(65, 65))
player_attack = AnimatedSprite(load_image('Player_movement/Woodcutter_attack1.png'), 6, 1, WIDTH // 2, HEIGHT // 2,
                               scaling=(65, 65))
player_damage = AnimatedSprite(load_image('Player_movement/Woodcutter_hurt.png'), 3, 1, WIDTH // 2, HEIGHT // 2,
                               scaling=(65, 65))
player_die = AnimatedSprite(load_image('Player_movement/Woodcutter_death.png'), 6, 1, WIDTH // 2, HEIGHT // 2,
                            scaling=(65, 65))
player_dead = AnimatedSprite(load_image('Player_movement/Woodcutter_dead.png'), 1, 1, WIDTH // 2, HEIGHT // 2,
                             scaling=(65, 65))
fon = AnimatedSprite(load_image('fon_anim.png'), 1, 4, 0, 0, group=fon_group, need_scale=True, scaling=(WIDTH, HEIGHT))
button_play = AnimatedSprite(load_image('button_anim.png'), 1, 2, WIDTH // 2 - 125, 500,
                             group=button_group, need_scale=True, scaling=(250, 73))

enemy_idle = AnimatedSprite(load_image("Enemy_movement/Enemy_idle.png"), 4, 1, 0, 0)
enemy_image = enemy_idle.frames[0]
enemy_flight = AnimatedSprite(load_image("Enemy_movement/Enemy_walk.png"), 4, 1, 0, 0)
enemy_attack = AnimatedSprite(load_image("Enemy_movement/Enemy_attack.png"), 4, 1, 0, 0)
enemy_die = AnimatedSprite(load_image("Enemy_movement/Enemy_die.png"), 4, 1, 0, 0)
enemy_hurt = AnimatedSprite(load_image("Enemy_movement/Enemy_hurt.png"), 3, 1, 0, 0)

boss_idle = AnimatedSprite(load_image("Boss_movement/Boss_idle.png"), 4, 1, 0, 0)
boss_image = boss_idle.frames[0]
boss_damage = AnimatedSprite(load_image("Boss_movement/Boss_hurt.png"), 2, 1, 0, 0)
boss_die = AnimatedSprite(load_image("Boss_movement/Boss_die.png"), 6, 1, 0, 0)
fountain = AnimatedSprite(load_image('fountain/fountainanim2.png'), 1, 16, HEIGHT + 1750, 200, scaling=(200, 200),
                          group=[fountain_group, tiles_group])
boss_attack = load_image("Boss_movement/Boss_shoot_1.png")

mushroom_walk = AnimatedSprite(load_image("mushrooms/mushroom_left.png"), 3, 1, 0, 0)
mushroom_image = mushroom_walk.frames[0]
mushroom_boom = AnimatedSprite(load_image("mushrooms/mushroom_boom.png"), 3, 1, 0, 0)

tile_width = tile_height = 50
level_map_1 = load_level('map.txt')
level_map_2 = load_level('map2.txt')
levels_sp = [level_map_1, level_map_2]
cursor = AnimatedSprite(load_image('cursor1_2.png'), 1, 1, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                        need_scale=True, scaling=(40, 40), group=cursors_group)
double_cursor = AnimatedSprite(load_image('double_cursor.png'), 1, 1, pygame.mouse.get_pos()[0],
                               pygame.mouse.get_pos()[1], group=technical_sprite_group, need_scale=False)

player, enemy, boss_s, mushroom, level_x, level_y = generate_level(load_level('map.txt'))


def end_screen(txt=[]):
    screen.fill('black')
    fountain_group.empty()
    coins_group.empty()
    npc_group.empty()
    back_group.empty()
    plat_group.empty()
    enemy_group.empty()
    boss_group.empty()
    cursors_group.empty()
    technical_sprite_group.empty()
    particle_group.empty()
    castle_group.empty()
    portal_group.empty()
    player_group.empty()
    mushroom_group.empty()
    npc_group.empty()
    pygame.mouse.set_visible(0)
    intro_text = map(lambda x: str(x), txt)
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(f'Результат: {line}', 1, pygame.Color('Yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (WIDTH // 2) - intro_rect.width // 2
        text_coord += intro_rect.height
    counter = 0
    while True:
        counter += 1
        out = False
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.collide_mask(button_play, double_cursor):
                    button_play.update()
                    out = True
        cursor.move(pygame.mouse.get_pos()[0] - 6, pygame.mouse.get_pos()[1])
        double_cursor.move(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        technical_sprite_group.draw(screen)
        fon_group.draw(screen)
        button_group.draw(screen)
        if pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] > 0 and pygame.mouse.get_pos()[0] < WIDTH - 1 and \
                pygame.mouse.get_pos()[1] < HEIGHT - 1:
            cursors_group.draw(screen)
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        if out:
            time.sleep(0.1)
            return
        clock.tick(FPS)
        if counter == 100:
            fon.update()
            counter = 0


def start_screen():
    pygame.mouse.set_visible(0)
    intro_text = []
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
    counter = 0
    while True:
        counter += 1
        out = False
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.collide_mask(button_play, double_cursor):
                    button_play.update()
                    out = True
        cursor.move(pygame.mouse.get_pos()[0] - 6, pygame.mouse.get_pos()[1])
        double_cursor.move(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        technical_sprite_group.draw(screen)
        fon_group.draw(screen)
        if button_play.rect.y > HEIGHT // 2 - button_play.rect.height // 2:
            button_play.rect.y -= 6
        button_group.draw(screen)
        if pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] > 0 and pygame.mouse.get_pos()[0] < WIDTH - 1 and \
                pygame.mouse.get_pos()[1] < HEIGHT - 1:
            cursors_group.draw(screen)
        pygame.display.flip()
        if out:
            time.sleep(0.1)
            return
        clock.tick(FPS)
        if counter == 100:
            fon.update()
            counter = 0


if __name__ == '__main__':
    start_screen()
    camera = Camera()
    counter = 0
    enemy_anim_count = 0
    counter_death_anim = 0
    running = True
    current_press = ''
    attack = ''
    counter_atack_anim = 0
    counter_death_anim_enemy = 0
    counter_death_anim_boss = 0
    reapp = False
    can_jump = True
    font = pygame.font.Font(None, 30)
    need_blackout = False
    surf = pygame.Surface((WIDTH, HEIGHT))
    button_created = False
    button_group.empty()
    while running:
        if boss_s:
            if boss_s.live == 0:
                end_screen()
        if player.lives != 0:
            for el in mushroom_group:
                if el.lives > 0:
                    el.attack()
            for el in boss_group:
                if el.live > 0:
                    el.attack()

                else:
                    if counter % 10 == 0 and counter_death_anim_boss != 5:
                        el.animate('die')
                        counter_death_anim_boss += 1
                        need_blackout = True
            for elem in enemy_group:
                if elem.lives > 0:
                    elem.attack()
                else:
                    if counter % 10 == 0:
                        if counter_death_anim_enemy != 3:
                            elem.animate('die')
                            counter_death_anim_enemy += 1

        else:
            for elem in enemy_group:
                if counter % 17 == 0:
                    elem.animate('idle')
                if counter % 10 == 0 and counter_death_anim != 5:
                    player.animate('die')
                    counter_death_anim += 1
                    already_do = True
        for elem in enemy_group:
            if elem.lives == 0 and elem.rect[1] != 0:
                if counter % 2 == 0:
                    elem.rect[1] += 4

        move(player, 'fall')
        if player.lives > 0:
            already_do = False
        if attack == '1':
            already_do = True
            if counter % 10 == 0 and counter_atack_anim != 6:
                player.animate('attack1')
                counter_atack_anim += 1
            if counter_atack_anim == 6:
                attack = ''
        if not already_do:
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
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    for elem in portal_group:
                        if pygame.sprite.collide_mask(elem, player):
                            screen.fill('black')
                            fountain_group.empty()
                            coins_group.empty()
                            npc_group.empty()
                            back_group.empty()
                            plat_group.empty()
                            enemy_group.empty()
                            boss_group.empty()
                            cursors_group.empty()
                            technical_sprite_group.empty()
                            particle_group.empty()
                            castle_group.empty()
                            portal_group.empty()
                            player_group.empty()
                            mushroom_group.empty()
                            npc_group.empty()
                            elem.teleport()
                            elem.level = level_map_1
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
                if event.key == pygame.K_SPACE and can_jump:
                    speed_y = -16
                    current_press = 'j'
                    already_do = True
                    can_jump = False
                    player.animate('jump')
                if event.key == pygame.K_e:
                    need_blackout = not (need_blackout)
                    if need_blackout:
                        surf.set_alpha(200)
                    else:
                        surf.set_alpha(255)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.animate('attack1')
                    attack = '1'
                    counter_atack_anim = 0
                    for element in enemy_group:
                        if abs(player.rect[0] - element.rect[0]) <= 44 and abs(
                                player.rect[1] - element.rect[1]) <= 4 and element.lives > 0:
                            element.animate('hurt')
                            element.lives -= 1
                    for el in boss_group:
                        if abs(el.rect[0] - player.rect[0]) <= 44 and el.live > 0:
                            el.animate('hurt')
                            el.live -= 1

            if event.type == pygame.KEYUP:
                current_press = ''
                moving = ''
                counter = 0
                Counter_ticks = False
            if event.type == pygame.MOUSEBUTTONUP:
                if counter_atack_anim > 5:
                    attack = ''
        counter += 1
        camera.update()
        for sprite in tiles_group:
            camera.apply(sprite)
        for elem in plat_group:
            if pygame.sprite.collide_mask(elem, player):
                reapp = True
                if elem.rect.x <= player.rect.x:
                    can_jump = True
        for elem in coins_group:
            if pygame.sprite.collide_mask(elem, player):
                create_particles(elem.pos)
                elem.get()
                elem.kill()
        if reapp:
            for sprite in tiles_group:
                camera.reapply(sprite)
            reapp = False
        camera.dx = 0
        camera.dy = 0
        if counter % 15 == 0 and (not already_do or counter_atack_anim == 6):
            player.animate('idle')
        if need_blackout:
            if not button_created:
                buttom_tmp = AnimatedSprite(load_image('button_Anim_ob.png'), 2, 1, WIDTH // 2, 400,
                                            group=[all_sprites, button_group], need_scale=False)
                button_created = True
            for elem in button_group:
                elem.rect.x = WIDTH // 2 - elem.rect.x // 2
                if elem.rect.y > HEIGHT // 2:
                    elem.rect.y -= 6
        else:
            button_created = False
            button_group.empty()
        screen.fill('black')
        surf.fill('black')
        castle_group.draw(surf)
        back_group.draw(surf)
        plat_group.draw(surf)
        portal_group.draw(surf)
        fountain_group.draw(surf)
        npc_group.draw(surf)
        player_group.draw(surf)
        enemy_group.draw(surf)
        boss_group.draw(surf)
        coins_group.draw(surf)
        particle_group.draw(surf)
        mushroom_group.draw(surf)
        particle_group.update()
        surf.blit(load_image(f"Hearts/Health_{player.lives}.png"), (0, 0))
        screen.blit(load_image(f"Hearts/Health_{player.lives}.png"), (0, 0))

        for el in boss_group:
            if el.live > 0:
                screen.blit(boss_attack, (el.attack_x, el.attack_y))

        text = font.render(str(player.money), 1, pygame.Color('Yellow'))
        surf.blit(text, (WIDTH - 50, 10))
        screen.blit(surf, (0, 0))
        button_group.draw(screen)
        pygame.display.flip()
        if counter % 5 == 0:
            portal_group.update()
        if counter % 10 == 0:
            npc_group.update()
            coins_group.update()
            fountain_group.update()
        clock.tick(100)
        player_pos = player.pos
