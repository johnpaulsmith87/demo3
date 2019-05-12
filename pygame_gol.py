# -*- coding: utf-8 -*-
"""
Game of life script with animated evolution

Created on Tue Jan 15 12:37:52 2019

@author: shakes
"""
import conway
import pygame
import numpy as np
N = 1024

#create the game of life object
life = conway.GameOfLife(N)
#life.insertBlinker((0,0))
#life.insertGlider((0,0))
#life.insertGliderGunFixed((0,0))
life.loadFromFile("2c5-spaceship-gun-p690.rle")
cells = life.getStates() #initial state

#-------------------------------
#plot cells
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation


pygame.init()
screen = pygame.display.set_mode((N,N))
surface = pygame.surfarray.make_surface(np.swapaxes(cells, 0, 1))
surface.set_colorkey((255,255,255))
finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    
    screen.blit(surface, (0,0))
    pygame.display.flip()
    life.evolve()
    cells = life.getStates()
    surface = pygame.surfarray.make_surface(np.swapaxes(cells, 0, 1))
    surface.set_colorkey((255,255,255))
pygame.quit()