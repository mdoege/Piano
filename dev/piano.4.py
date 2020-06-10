#!/usr/bin/env python

# Toy piano in PyGame

import pygame

import time, random

BLACK = 0, 0, 0
WHITE = 255, 255, 255
ORANGE = 255, 136, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
BACKGROUND = 12, 54, 87
LW = 10
BKW = 22
BKH = 200
H = 350
bkeys = {1: 1, 2: 3, 4: 6, 5: 8, 6: 10}
wkeys = {0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11, 7: 12}
RECT_NORMAL = pygame.Rect((236, 432, 130, 55))
RECT_SIMON = pygame.Rect((400, 432, 150, 55))
NOTELEN = 0.6
SIMONCOL = (RED, ORANGE, GREEN, ORANGE, BLUE, ORANGE, ORANGE, YELLOW)

class Piano:
    def __init__(self):
        pygame.init()
        self.res = 800, H + 150
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption('Piano')
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        self.audio = {}
        for n in range(13):
            self.audio[n] = pygame.mixer.Sound("snd/piano_%02u.ogg" % n)
        self.overlay = pygame.image.load("img/piano.png")
        self.playnote = None
        self.playtime = 0
        self.simon = False
        self.simonseq = []
        self.simonlen = 1
        self.simonplay = False
        self.simonstart = 0
        self.lastplayed = -1

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                p = self.pos2key(x,y)
                if p != None:
                    self.play(p)
                if RECT_NORMAL.collidepoint(x, y) and self.simon:
                    self.simon = False
                if RECT_SIMON.collidepoint(x, y) and not self.simon:
                    self.simon = True
                    self.simonseq = [random.choice([0, 4, 7, 12]) for q in range(100)]
                    self.simonlen = 3
                    self.simonplay = True
                    self.simonstart = time.time()
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
            if y < H and 100*k < x < 100*(k+1):
                return wkeys[k]

    def update(self):
        if self.simon and self.simonplay:
            n = int((time.time() - self.simonstart) / NOTELEN)
            if n >= self.simonlen:
                self.simonplay = False
                self.simonstart = 0
                self.lastplayed = -1
            elif n > self.lastplayed:
                self.play(self.simonseq[n])
                self.lastplayed = n
        self.screen.fill(BACKGROUND)
        if not self.simon:
            if time.time() - self.playtime > 0.2:
                self.playnote = None
        else:
            if time.time() - self.playtime > .85 * NOTELEN:
                self.playnote = None
        for k in range(8):
            c = WHITE
            for x in wkeys.keys():
                if x == k and wkeys[x] == self.playnote:
                    if self.simon:
                        c = SIMONCOL[k]
                    else:
                        c = ORANGE
            self.draw_wkey(k, c)
        for k in 1, 2, 4, 5, 6:
            c = BLACK
            for x in bkeys.keys():
                if x == k and bkeys[x] == self.playnote:
                    c = ORANGE
            self.draw_bkey(k, c)

        if not self.simon:
            pygame.draw.rect(self.screen, ORANGE, RECT_NORMAL, 3)
        else:
            pygame.draw.rect(self.screen, ORANGE, RECT_SIMON, 3)

        self.screen.blit(self.overlay, (0, 0))

        pygame.display.flip()

c = Piano()
c.run()

