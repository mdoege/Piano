#!/usr/bin/env python

# Toy organ with sustain

import pygame

import time, random

BLACK = 0, 0, 0
WHITE = 255, 255, 255
ORANGE = 255, 136, 0
YELLOW = 255, 255, 0
BACKGROUND = 12, 54, 87
LW = 10        # outline width
BKW = 22       # black key width
BKH = 200      # black key height
H = 350        # white key height
bkeys = {1: 1, 2: 3, 4: 6, 5: 8, 6: 10}
wkeys = {0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11, 7: 12}
SOUNDS = ("organ", "piano")
LOOP = (-1, 0)

class Piano:
    def __init__(self):
        pygame.init()
        self.res = 800, H + 150
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption('Organ')
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        self.sel_snd = 0
        self.volume = 0.5
        self.load_sound(SOUNDS[0])

    def load_sound(self, name):
        "Load a sound bank"
        self.audio = {}
        for n in range(13):
            self.audio[n] = pygame.mixer.Sound("snd/%s_%02u.wav" % (name, n))
        self.keys = 13 * [False]
        self.setvol()

    def setvol(self):
        "Set volume for all loaded sounds"
        for n in range(13):
            self.audio[n].set_volume(self.volume)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.sel_snd += 1
                    if self.sel_snd == len(SOUNDS):
                        self.sel_snd = 0
                    self.load_sound(SOUNDS[self.sel_snd])
                if event.key == pygame.K_2:
                    self.sel_snd -= 1
                    if self.sel_snd == -1:
                        self.sel_snd = len(SOUNDS) - 1
                    self.load_sound(SOUNDS[self.sel_snd])

                if event.key == pygame.K_3:
                    self.volume += 0.1
                    self.setvol()
                if event.key == pygame.K_4:
                    self.volume -= 0.1
                    self.setvol()

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
                if event.key == pygame.K_y or event.key == pygame.K_z:
                    self.play(6)
                if event.key == pygame.K_u:
                    self.play(8)
                if event.key == pygame.K_i:
                    self.play(10)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    self.stop(0)
                if event.key == pygame.K_d:
                    self.stop(2)
                if event.key == pygame.K_f:
                    self.stop(4)
                if event.key == pygame.K_g:
                    self.stop(5)
                if event.key == pygame.K_h:
                    self.stop(7)
                if event.key == pygame.K_j:
                    self.stop(9)
                if event.key == pygame.K_k:
                    self.stop(11)
                if event.key == pygame.K_l:
                    self.stop(12)

                if event.key == pygame.K_e:
                    self.stop(1)
                if event.key == pygame.K_r:
                    self.stop(3)
                if event.key == pygame.K_y or event.key == pygame.K_z:
                    self.stop(6)
                if event.key == pygame.K_u:
                    self.stop(8)
                if event.key == pygame.K_i:
                    self.stop(10)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
        pygame.quit()

    def play(self, k, user = True):
        "Play a note"
        self.audio[k].play(loops = LOOP[self.sel_snd])
        self.keys[k] = True

    def stop(self, k, user = True):
        "Stop playing a note"
        self.audio[k].stop()
        self.keys[k] = False

    def draw_wkey(self, k, c):
        "Draw white key"
        pygame.draw.rect(self.screen, BLACK, (100*k, 0, 100, H))
        pygame.draw.rect(self.screen, c, (int(100*k+LW/2), LW, 100-LW, H-2*LW))

    def draw_bkey(self, k, c):
        "Draw black key"
        pygame.draw.rect(self.screen, c, (100*k-BKW, 0, 2*BKW, BKH))

    def update(self):
        self.screen.fill(BACKGROUND)
        for k in range(8):
            c = WHITE
            for x in wkeys.keys():
                if x == k and self.keys[wkeys[x]]:
                    c = ORANGE
            self.draw_wkey(k, c)
        for k in 1, 2, 4, 5, 6:
            c = BLACK
            for x in bkeys.keys():
                if x == k and self.keys[bkeys[x]]:
                    c = ORANGE
            self.draw_bkey(k, c)

        pygame.display.flip()

c = Piano()
c.run()

