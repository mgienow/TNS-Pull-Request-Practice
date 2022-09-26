import pygame, sys

clock=pygame.time.Clock()

from pygame.locals import *

pygame.init()

pygame.display.set_caption('My Pygame')

WINDOW_SIZE= (600,400)

screen =pygame.display.set_mode(WINDOW_SIZE,0,32)

display = pygame.Surface((300,200))

player_image = (pygame.image.load('waltuh.jpg').convert_alpha())

grass_image = pygame.image.load('grass.jpg').convert_alpha()
grass_image= pygame.transform.scale(grass_image,(16,16))
TILE_SIZE = grass_image.get_width()
dirt_image=pygame.image.load('dirt.png').convert_alpha()
dirt_image= pygame.transform.scale(dirt_image,(16,16))

player_image= pygame.transform.scale(player_image,(20,20))

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],         ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],           ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],           ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],           ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],          ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],         ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],        ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],           ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

while True: # game loop
    display.fill((146,244,255))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    if collisions['top']:
        player_y_momentum = 0

    display.blit(player_image, (player_rect.x, player_rect.y))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps
