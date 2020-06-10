#!/usr/bin/env python

# Toy piano in PyGame

import pygame

BLACK = 0, 0, 0
WHITE = 255, 255, 255
LW = 10
BKW = 22
BKH = 200
H = 350

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

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                p = self.pos2key(x,y)
                print(x,y,p)
                if p != None:
                    self.play(p)

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

    def draw_wkey(self, k, c):
        "Draw white key"
        pygame.draw.rect(self.screen, BLACK, (100*k, 0, 100, H))
        pygame.draw.rect(self.screen, c, (int(100*k+LW/2), LW, 100-LW, H-2*LW))

    def draw_bkey(self, k, c):
        "Draw black key"
        pygame.draw.rect(self.screen, BLACK, (100*k-BKW, 0, 2*BKW, BKH))

    def pos2key(self, x, y):
        "Get key num from mouse click position"
        bkeys = {1: 1, 2: 3, 4: 6, 5: 8, 6: 10}
        wkeys = {0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11, 7: 12}
        for k in 1, 2, 4, 5, 6:
            if y < BKH and (100*k-BKW < x < 100*k+BKW):
                return bkeys[k]
        for k in range(8):
            if 100*k < x < 100*(k+1):
                return wkeys[k]

    def update(self):
        self.screen.fill((255,0,0))
        for k in range(8):
            self.draw_wkey(k, WHITE)
        for k in 1, 2, 4, 5, 6:
            self.draw_bkey(k, BLACK)

        
        pygame.display.flip()

c = Piano()
c.run()

