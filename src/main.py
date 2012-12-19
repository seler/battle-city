'''
Created on 2009-05-27

@author: seler
'''
import pygame

if __name__ == '__main__':
    import game
    resolution = (1280, 800)
    #resolution = (800, 600)
    fullscreen = True
    game = game.Game(resolution, fullscreen)
    game.play()