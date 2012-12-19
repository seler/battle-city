'''
Created on 2009-05-26

@author: seler
'''
import pygame
from pygame.locals import *
from vector2 import Vector2
from math import *

class Body:
    def __init__(self, (pos_x, pos_y)):
        level = 1
        self.image_filepath = '../images/tank_lvl_'+str(level)+'.png'
        self.level = level
        self.sprite = pygame.image.load(self.image_filepath).convert_alpha()
        self.sprite = pygame.transform.rotate(self.sprite, 90)
        self.pos = Vector2(pos_x, pos_y)
        self.speed = 200.
        self.max_front_speed = 200.
        self.max_rear_speed = -100.
        self.acceleration = 10. # acceleration per second
        self.deceleration = 4. # deceleration per second
        self.rotation = 50.
        self.rotation_speed = 45. # Degrees per second
        self.rotation_direction = 0.
        self.movement_direction = 0.
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        w, h = self.rotated_sprite.get_size()
        self.draw_pos = Vector2(self.pos.x-w/2, self.pos.y-h/2)
    def set_rotation_direction(self, r):
        self.rotation_direction = r
    def set_movement_direction(self, m):
        self.movement_direction = m
    def be(self, time_passed_seconds):
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        w, h = self.rotated_sprite.get_size()
        self.draw_pos = Vector2(self.pos.x-w/2, self.pos.y-h/2)
        self.rotation += self.rotation_direction * self.rotation_speed * time_passed_seconds
        heading_x = sin(radians(self.rotation))
        heading_y = cos(radians(self.rotation))
        self.heading = Vector2(heading_x, heading_y)
        if self.speed > 0:
            self.speed -= self.deceleration
        elif self.speed < 0:
            self.speed += self.deceleration
        #self.heading *= self.movement_direction
        self.pos+= self.heading * self.speed * time_passed_seconds

class Turret:
    def __init__(self, (pos_x, pos_y)):
        level = 1
        self.image_filepath = '../images/turret_lvl_'+str(level)+'.png'
        self.level = level
        self.sprite = pygame.image.load(self.image_filepath).convert_alpha()
        self.sprite = pygame.transform.rotate(self.sprite, 90)
        self.pos = Vector2(pos_x, pos_y)
        self.rotation = 0.
        self.rotation_speed = 180. # Degrees per second
        self.rotation_direction = 0.
        self.movement_direction = 0.
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        self.draw_pos = self.pos
        self.weapon = Weapon(50, 300, 600, 0.5, 30, 30, self)
    def set_rotation_direction(self, r):
        self.rotation_direction = r
    def set_movement_direction(self, m):
        self.movement_direction = m
    def be(self, time_passed_seconds, (pos_x, pos_y), (mx, my)):
        self.time_passed_seconds = time_passed_seconds
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        self.pos = Vector2(pos_x, pos_y)
        w, h = self.rotated_sprite.get_size()
        self.draw_pos = Vector2(self.pos.x-w/2, self.pos.y-h/2)
        ax, ay = self.pos
        mx = mx-ax
        my = (my-ay)*-1
        if mx != 0:
            angle = atan(my/mx)/(pi/180.)
        else:
            angle = -90
        if mx<0:
            angle += 180.
        if mx>=0 and my<0:
            angle += 360.
        self.rotation = angle+90
        self.weapon.be(self.time_passed_seconds)

        return self.draw_pos
    def shoot(self, destination):
        if self.weapon.shoot(destination, self.time_passed_seconds):
            return True
        else:
            return False

class Bullet:
    def __init__(self, (from_x, from_y), (to_x, to_y)):
        self.pos = Vector2(from_x, from_y)
        self.destination = Vector2(to_x, to_y)
        self.heading = Vector2.from_points(self.pos, self.destination)
        self.heading.normalize()
        self.speed = 500 #pixels per second
        self.total_distance = 0
        self.sprite = pygame.image.load('../images/bullet_lvl_2.png').convert_alpha()
        w, h = self.sprite.get_size()
        if w > 10:
            ratio = 10./w
            h = int(h*ratio)
            self.sprite = pygame.transform.scale(self.sprite, (10, h))
        self.rotation = 0
        to_x = to_x-from_x
        to_y = (to_y-from_y)*-1
        if to_x != 0:
            angle = atan(to_y/to_x)/(pi/180.)
        else:
            angle = -90
        if to_x<0:
            angle += 180.
        if to_x>=0 and to_y<0:
            angle += 360.
        self.rotation = angle-90
        self.pos += self.heading * 100 #dodaje dlugos lugy
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        w, h = self.rotated_sprite.get_size()
        self.draw_pos = Vector2(self.pos.x-w/2, self.pos.y-h/2)
    def be(self, t):
        distance_moved = t * self.speed
        self.total_distance += distance_moved
        self.pos += self.heading * distance_moved
        w, h = self.rotated_sprite.get_size()
        self.draw_pos = Vector2(self.pos.x-w/2, self.pos.y-h/2)
class Weapon:
    def __init__(self, hitpoints, speed, range, reload_time, clip_size, burst, marksman):
        self.hitpoints = hitpoints
        self.speed = speed
        self.range = range
        self.reload_time = reload_time
        self.reload_time_passed = reload_time
        self.clip_size = clip_size
        self.burst = burst
        self.ammo = clip_size
        self.bullets = []
        self.marksman = marksman
    def be(self, time_passed_seconds):
        self.reload_time_passed += time_passed_seconds
        for i in self.bullets:
            i.be(time_passed_seconds)
            if i.total_distance > 1500:
                self.bullets.remove(i)
    def shoot(self, destination):
        if self.reload_time_passed >= self.reload_time:
            self.reload_time_passed = 0
            start_pos = self.marksman.pos
            self.bullets.append(Bullet(start_pos, destination))
            return True
        else:
            return False
    def damage(self, looser):
        looser.hitpoints -= self.hitpoints

class Tank:
    def __init__(self, (pos_x, pos_y)):
        self.body = Body((pos_x, pos_y))
        self.turret = Turret((pos_x, pos_y))
        self.max_hitpoints = 100
        self.hitpoints = self.max_hitpoints
        self.alive = True
    def be(self, t, mouse_pos):
        self.body.be(t)
        self.turret.be(t, self.body.pos, mouse_pos)
        if self.hitpoints <= 0:
            self.alive = False
if __name__ == '__main__':
    pass