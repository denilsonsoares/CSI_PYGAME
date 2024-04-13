import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

from entities.Fire import Fire
from entities.Player import Player
from utils.Imports import Imports
pygame.init()

pygame.display.set_caption("Platform")

WIDTH, HEIGHT = (1000, 800)
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))



def get_block(size):
    path = join("assets", "Terrain","Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size),pygame.SRCALPHA,32)
    rect = pygame.Rect(96, 0, size,size)
    surface.blit(image,(0,0),rect)
    return pygame.transform.scale2x(surface)


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x,y, width, height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image,(self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width +1):
       for j in range (HEIGHT // height + 1):
            pos = [i*width, j*height]
            tiles.append(pos)
    return tiles, image

def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)

    return collided_objects

def collide(player, objects, dx):
    player.move(dx,0)
    player.update()
    collided_objects = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_objects = obj
            break
    player.move(-dx,0)
    player.update()
    return collided_objects

def handle_move(player,objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL*2)
    collide_right = collide(player, objects, PLAYER_VEL*2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96

    player = Player(100,100,50, 50)
    fire = Fire(100, HEIGHT - block_size -64, 16, 32)
    fire.on()
    floor = [Block(i*block_size, HEIGHT - block_size,block_size) for i in range(-WIDTH//block_size, (WIDTH*2)//block_size)]

    objects = [*floor, Block(0,HEIGHT - block_size*2,block_size),
               Block(block_size*3,HEIGHT - block_size*4,block_size),
               fire]

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count <2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        handle_move(player,objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x>= WIDTH - scroll_area_width and player.x_vel > 0) or
                (player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0)):
            offset_x += player.x_vel


    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)