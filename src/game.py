'''
Created on 2009-05-27

@author: seler
'''
import pygame
from pygame.locals import *
from sys import exit
from vector2 import Vector2
from math import *
import units
class Game:
    '''
    Class holding all the game
    '''
    def __init__(self, resolution, fullscreen = False):
        '''
        Constructor
        '''
        self.resolution = resolution
        if not pygame.display.get_init():
            pygame.init()
        self.fullscreen = fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(resolution, FULLSCREEN, 32)
        else:
            self.screen = pygame.display.set_mode(resolution, 0, 32)

        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(resolution[0]/2, resolution[1]/2)
        self.mouse_image_filepath = '../images/crosshair.png'
        self.mouse_cursor = pygame.image.load(self.mouse_image_filepath).convert_alpha()
        self.background_image_filepath = '../images/bg.jpg'
        self.background = pygame.image.load(self.background_image_filepath).convert()
        self.clock = pygame.time.Clock()
        
        self.tank = units.Tank((100,100))
        self.tank2 = units.Tank((1000,200))
        self.font = pygame.font.SysFont("arial", 26);
        self.font_height = self.font.get_linesize()
    def key_things(self):
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    if event.key == K_f:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode(self.resolution, FULLSCREEN, 32)
                        else:
                            self.screen = pygame.display.set_mode(self.resolution, 0, 32)
                                        
            pressed_keys = pygame.key.get_pressed()
            self.tank.body.set_rotation_direction(0)
            self.tank.body.set_movement_direction(0)
    
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.tank.body.set_rotation_direction(+1)
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.tank.body.set_rotation_direction(-1)
            if pressed_keys[K_UP] or pressed_keys[K_w]:
                #self.tank.body.set_movement_direction(+1)
                if self.tank.body.speed >= self.tank.body.max_front_speed:
                    self.tank.body.speed = self.tank.body.max_front_speed
                else:
                    self.tank.body.speed += self.tank.body.acceleration
            if pressed_keys[K_DOWN] or pressed_keys[K_s]:
                #self.tank.body.set_movement_direction(-1)
                if self.tank.body.speed <= self.tank.body.max_rear_speed:
                    self.tank.body.speed = self.tank.body.max_rear_speed
                else:
                    self.tank.body.speed -= self.tank.body.acceleration
            
            mlb, mmb, mrb = pygame.mouse.get_pressed()
            if mlb:
                self.tank.turret.weapon.shoot(self.mouse_pos)
    def blit_things(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.tank.body.rotated_sprite, self.tank.body.draw_pos)
        for bullet in self.tank.turret.weapon.bullets:
            self.screen.blit(bullet.rotated_sprite, bullet.draw_pos)
        self.screen.blit(self.tank.turret.rotated_sprite, self.tank.turret.draw_pos)
        if self.tank2.alive:
            self.screen.blit(self.tank2.body.rotated_sprite, self.tank2.body.draw_pos)
            for bullet in self.tank2.turret.weapon.bullets:
                self.screen.blit(bullet2.sprite, bullet.draw_pos)
            self.screen.blit(self.tank2.turret.rotated_sprite, self.tank2.turret.draw_pos)
        mx, my = self.mouse_pos
        self.screen.blit(self.mouse_cursor, (mx-self.mouse_cursor.get_width()/2, my-self.mouse_cursor.get_height()/2))
        self.screen.blit(self.font.render('framerate = '+str(self.framerate), True, (0, 0, 0)), (0, 0))
    def data_collector(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.time_passed = self.clock.tick(50)
        self.time_passed_seconds = self.time_passed / 1000.0
        self.framerate = int(1/self.time_passed_seconds)
    def distance(self, ax,ay,bx,by):
        return sqrt((bx-ax)*(bx-ax)+(by-ay)*(by-ay))
    def collide(self, a, b, a_radius, b_radius):
        ax, ay = a.pos.x, a.pos.y
        bx, by = b.pos.x, b.pos.y
        d = self.distance(ax, ay, bx, by) - a_radius - b_radius
        print d
        if d <= 0:
            return True
        else:
            return False
            
    def play(self):
        while True:
            self.data_collector()
            self.key_things()
            self.blit_things()
            for i in self.tank.turret.weapon.bullets:
                #pygame.draw.line(self.screen, (0,0,0), (i.pos.x, i.pos.y), (self.tank2.body.pos.x, self.tank2.body.pos.y), 5)
                if self.collide(i, self.tank2.body, 10, 60):
                    self.tank.turret.weapon.bullets.remove(i)
                    self.tank.turret.weapon.damage(self.tank2)
            self.tank.be(self.time_passed_seconds, self.mouse_pos)
            self.tank2.be(self.time_passed_seconds, self.tank.body.pos)
            pygame.display.update()





#############
#############
#############