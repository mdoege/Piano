#!/usr/bin/env python

# Toy piano in PyGame

import pygame

import time

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
LW = 10
BKW = 22
BKH = 200
H = 350
bkeys = {1: 1, 2: 3, 4: 6, 5: 8, 6: 10}
wkeys = {0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11, 7: 12}

class Piano:
    def __init__(self):
        pygame.init()
        self.res = 800, H
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption('Piano')
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        self.audio = {}
        for n in range(13):
            self.audio[n] = pygame.mixer.Sound("snd/piano_%02u.ogg" % n)
        self.playnote = None
        self.playtime = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                p = self.pos2key(x,y)
                print(x,y,p)
                if p != None:
                    self.play(p)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.play(0)
                if event.key == pygame.K_d:
                    self.play(2)
                if event.key == pygame.K_f:
                    self.play(4)
                if event.key == pygame.K_g:
                    self.play(5)
                if event.key == pygame.K_h:
                    self.play(7)
                if event.key == pygame.K_j:
                    self.play(9)
                if event.key == pygame.K_k:
                    self.play(11)
                if event.key == pygame.K_l:
                    self.play(12)

                if event.key == pygame.K_e:
                    self.play(1)
                if event.key == pygame.K_r:
                    self.play(3)
                if event.key == pygame.K_y or event.key == pygame.K_z:  # QWERTY/QWERTZ layout
                    self.play(6)
                if event.key == pygame.K_u:
                    self.play(8)
                if event.key == pygame.K_i:
                    self.play(10)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
        pygame.quit()

    def play(self, k):
        "Play a note"
        self.audio[k].play()
        self.playnote = k
        self.playtime = time.time()

    def draw_wkey(self, k, c):
        "Draw white key"
        pygame.draw.rect(self.screen, BLACK, (100*k, 0, 100, H))
        pygame.draw.rect(self.screen, c, (int(100*k+LW/2), LW, 100-LW, H-2*LW))

    def draw_bkey(self, k, c):
        "Draw black key"
        pygame.draw.rect(self.screen, c, (100*k-BKW, 0, 2*BKW, BKH))

    def pos2key(self, x, y):
        "Get key num from mouse click position"
        for k in 1, 2, 4, 5, 6:
            if y < BKH and (100*k-BKW < x < 100*k+BKW):
                return bkeys[k]
        for k in range(8):
            if 100*k < x < 100*(k+1):
                return wkeys[k]

    def update(self):
        self.screen.fill((255,0,0))
        if time.time() - self.playtime > 0.2:
            self.playnote = None
        for k in range(8):
            c = WHITE
            for x in wkeys.keys():
                if x == k and wkeys[x] == self.playnote:
                    c = GREEN
            self.draw_wkey(k, c)
        for k in 1, 2, 4, 5, 6:
            c = BLACK
            for x in bkeys.keys():
                if x == k and bkeys[x] == self.playnote:
                    c = GREEN
            self.draw_bkey(k, c)

        
        pygame.display.flip()

c = Piano()
c.run()

