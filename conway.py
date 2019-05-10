# -*- coding: utf-8 -*-
"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

Created on Tue Jan 15 12:21:17 2019

@author: shakes
"""
import numpy as np
from scipy import signal
from scipy import fftpack as fftpack

class GameOfLife:
    '''
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    '''
    def __init__(self, N=256, finite=False, fastMode=False):
        self.grid = np.zeros((N,N), np.uint)
        self.neighborhood = np.zeros((3,3), np.uint) # 8 connected kernel
        self.neighborhood[1,1] = 0 #do not count centre pixel - i used this for something else...
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N
        self.cols = N
        self.golConvolutionKernel = np.ones((3,3), np.uint8)
        self.golConvolutionKernel[1,1] = 0
    def getStates(self):
        '''
        Returns the current states of the cells
        '''
        return self.grid
    
    def getGrid(self):
        '''
        Same as getStates()
        '''
        return self.getStates()
               
    def evolve(self):
        '''
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction
        '''
                    
        #get weighted sum of neighbors
        #PART A & E CODE HERE
        
        #implement the GoL rules by thresholding the weights
        #PART A CODE HERE
        #Part E code
        scoreArray2 = fftpack.ifft2(fftpack.fft2(self.grid) * fftpack.fft2(self.golConvolutionKernel))
        scoreArray = signal.convolve2d(self.grid, self.golConvolutionKernel, mode='full')
        newGrid = np.zeros((self.rows, self.cols), np.uint8)
        for i in range(self.rows):
            for j in range(self.cols):
                self.setNeighbourhood((i,j))
                score2 = self.getNeighbourhoodTotal()
                score = scoreArray2.item(i,j)
                current = self.grid.item(i,j)
                if current == self.aliveValue and score < 2:
                    newGrid[i,j] = self.deadValue
                elif current == self.aliveValue and (score == 2 or score == 3):
                    newGrid[i,j] = self.aliveValue
                elif current == self.aliveValue and score > 3:
                    newGrid[i,j] = self.deadValue
                elif current == self.deadValue and score == 3:
                    newGrid[i,j] = self.aliveValue

        #update the grid
        self.grid = newGrid #UNCOMMENT THIS WITH YOUR UPDATED GRID
    
    def setNeighbourhood(self, index=(0,0)):
        #start at top left and fill each neighbourhood cell (excluding index) with wrapping
        #
        # xxx
        # x0x   
        # xxx
        #
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                test = self.grid.item((index[0] + i) % self.rows, (index[1] + j) % self.cols)
                self.neighborhood[i+1][j+1] = test
    def setNeighbourhoodNoWrap(self, index=(0,0)):
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    continue
                if i + index[0] < 0 or i + index[0] >= self.cols or j + index[1] < 0 or j + index[1] >= self.rows:
                    continue
                self.neighborhood[i+1][j+1] = self.grid.item(index[0], index[1])

    def getNeighbourhoodTotal(self):
        return np.sum(self.neighborhood)
    def insertBlinker(self, index=(0,0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        
    def insertGlider(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+2] = self.aliveValue
        self.grid[index[0]+2, index[1]] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+2] = self.aliveValue
        
    def insertGliderGun(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0]+1, index[1]+26] = self.aliveValue
        
        self.grid[index[0]+2, index[1]+24] = self.aliveValue
        self.grid[index[0]+2, index[1]+26] = self.aliveValue
        
        self.grid[index[0]+3, index[1]+14] = self.aliveValue
        self.grid[index[0]+3, index[1]+15] = self.aliveValue
        self.grid[index[0]+3, index[1]+22] = self.aliveValue
        self.grid[index[0]+3, index[1]+23] = self.aliveValue
        self.grid[index[0]+3, index[1]+36] = self.aliveValue
        self.grid[index[0]+3, index[1]+37] = self.aliveValue
        
        self.grid[index[0]+4, index[1]+13] = self.aliveValue
        self.grid[index[0]+4, index[1]+17] = self.aliveValue
        self.grid[index[0]+4, index[1]+22] = self.aliveValue
        self.grid[index[0]+4, index[1]+23] = self.aliveValue
        self.grid[index[0]+4, index[1]+36] = self.aliveValue
        self.grid[index[0]+4, index[1]+37] = self.aliveValue
        
        self.grid[index[0]+5, index[1]+1] = self.aliveValue
        self.grid[index[0]+5, index[1]+2] = self.aliveValue
        self.grid[index[0]+5, index[1]+12] = self.aliveValue
        self.grid[index[0]+5, index[1]+18] = self.aliveValue
        self.grid[index[0]+5, index[1]+22] = self.aliveValue
        self.grid[index[0]+5, index[1]+23] = self.aliveValue
        
        self.grid[index[0]+6, index[1]+1] = self.aliveValue
        self.grid[index[0]+6, index[1]+2] = self.aliveValue
        self.grid[index[0]+6, index[1]+12] = self.aliveValue
        self.grid[index[0]+6, index[1]+16] = self.aliveValue
        self.grid[index[0]+6, index[1]+18] = self.aliveValue
        self.grid[index[0]+6, index[1]+19] = self.aliveValue
        self.grid[index[0]+6, index[1]+24] = self.aliveValue
        self.grid[index[0]+6, index[1]+26] = self.aliveValue
        
        self.grid[index[0]+7, index[1]+12] = self.aliveValue
        self.grid[index[0]+7, index[1]+18] = self.aliveValue
        self.grid[index[0]+7, index[1]+26] = self.aliveValue
        
        self.grid[index[0]+8, index[1]+13] = self.aliveValue
        self.grid[index[0]+8, index[1]+17] = self.aliveValue
        
        self.grid[index[0]+9, index[1]+14] = self.aliveValue
        self.grid[index[0]+9, index[1]+15] = self.aliveValue
