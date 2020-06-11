#!/usr/bin/env python

# Toy piano and Simon/Atari Touch Me game in PyGame

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
GRAY = 120, 120, 120
LW = 10        # outline width
BKW = 22       # black key width
BKH = 200      # black key height
H = 350        # white key height
bkeys = {1: 1, 2: 3, 4: 6, 5: 8, 6: 10}
wkeys = {0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11, 7: 12}
RECT_NORMAL = pygame.Rect((236, 432, 130, 55))  # button rects
RECT_SIMON = pygame.Rect((400, 432, 150, 55))
RECT_VOL = pygame.Rect((25, 432, 200, 22))
RECT_OCT = pygame.Rect((570, 432, 210, 22))
NOTELEN = 0.6
SIMONCOL = (RED, ORANGE, GREEN, ORANGE, BLUE, ORANGE, ORANGE, YELLOW)  # colors when in Simon mode

class Piano:
    def __init__(self):
        pygame.init()
        self.res = 800, H + 150
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption('Piano')
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        self.volume = 5
        self.octave = 1
        self.sust = True
        self.load_inst()
        self.setvol()
        self.overlay = pygame.image.load("img/piano.png")
        self.keys = 13 * [False]
        self.simon = False
        self.simonseq = []
        self.simonlen = 1
        self.simonplay = False
        self.simonstart = 0
        self.lastplayed = -1
        self.userseq = []

    def load_inst(self):
        "Load instrument samples"
        self.audio, self.sustain = {}, {}
        if self.octave == 0:
            o = "_low"
        elif self.octave == 2:
            o = "_high"
        else:
            o = ""
        for n in range(13):
            self.audio[n] = pygame.mixer.Sound("snd/piano%s_%02u.ogg" % (o, n))
            self.sustain[n] = pygame.mixer.Sound("snd/piano%s_sustain_%02u.ogg" % (o, n))
        self.audio["buzz"] = pygame.mixer.Sound("snd/buzz.ogg")

    def setvol(self):
        "Set volume for all loaded sounds"
        for n in range(13):
            self.audio[n].set_volume(self.volume / 10)
            self.sustain[n].set_volume(self.volume / 10)

    def setoct(self):
        "Change octave"
        self.load_inst()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                p = self.pos2key(x,y)
                if p != None:
                    self.play(p)
                if RECT_VOL.collidepoint(x, y):
                    self.volume = int(1 + 10 * (x - RECT_VOL.left) / RECT_VOL.width)
                    self.setvol()
                if RECT_OCT.collidepoint(x, y):
                    self.octave = int(3 * (x - RECT_OCT.left) / RECT_VOL.width)
                    self.setoct()
                if RECT_NORMAL.collidepoint(x, y) and self.simon:
                    self.simon = False
                    pygame.display.set_caption('Piano')
                if RECT_SIMON.collidepoint(x, y) and not self.simon:
                    self.simon = True
                    self.simonseq = [random.choice([0, 4, 7, 12]) for q in range(100)]
                    self.simonlen = 1
                    self.simonplay = True
                    self.simonstart = time.time()
                    pygame.display.set_caption('Simon')

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                p = self.pos2key(x,y)
                if p != None:
                    self.stop(p)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.stopall()

                if event.key == pygame.K_c:
                    self.sust = not self.sust

                # volume
                if event.key == pygame.K_b:
                    if self.volume < 10:
                        self.volume += 1
                    self.setvol()
                if event.key == pygame.K_v:
                    if self.volume > 1:
                        self.volume -= 1
                    self.setvol()

                # octave
                if event.key == pygame.K_m:
                    if self.octave < 2:
                        self.octave += 1
                    self.setoct()
                if event.key == pygame.K_n:
                    if self.octave > 0:
                        self.octave -= 1
                    self.setoct()

                # piano key press
                if event.key == pygame.K_s or event.key == pygame.K_1 or event.key == pygame.K_LEFT:
                    self.play(0)
                if event.key == pygame.K_d:
                    self.play(2)
                if event.key == pygame.K_f or event.key == pygame.K_2 or event.key == pygame.K_DOWN:
                    self.play(4)
                if event.key == pygame.K_g:
                    self.play(5)
                if event.key == pygame.K_h or event.key == pygame.K_3 or event.key == pygame.K_RIGHT:
                    self.play(7)
                if event.key == pygame.K_j:
                    self.play(9)
                if event.key == pygame.K_k:
                    self.play(11)
                if event.key == pygame.K_l or event.key == pygame.K_4 or event.key == pygame.K_UP:
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

            # piano key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s or event.key == pygame.K_1 or event.key == pygame.K_LEFT:
                    self.stop(0)
                if event.key == pygame.K_d:
                    self.stop(2)
                if event.key == pygame.K_f or event.key == pygame.K_2 or event.key == pygame.K_DOWN:
                    self.stop(4)
                if event.key == pygame.K_g:
                    self.stop(5)
                if event.key == pygame.K_h or event.key == pygame.K_3 or event.key == pygame.K_RIGHT:
                    self.stop(7)
                if event.key == pygame.K_j:
                    self.stop(9)
                if event.key == pygame.K_k:
                    self.stop(11)
                if event.key == pygame.K_l or event.key == pygame.K_4 or event.key == pygame.K_UP:
                    self.stop(12)

                if event.key == pygame.K_e:
                    self.stop(1)
                if event.key == pygame.K_r:
                    self.stop(3)
                if event.key == pygame.K_y or event.key == pygame.K_z:  # QWERTY/QWERTZ layout
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
        self.audio[k].play()
        if user and self.sust:
            self.sustain[k].play(loops = -1)
        self.keys[k] = True

    def stop(self, k, user = True):
        "Stop playing a note"
        self.audio[k].stop()
        self.sustain[k].stop()
        self.keys[k] = False

        # check if user melody matches Simon's
        if self.simon and user == True:
            self.userseq.append(k)
            if self.userseq == self.simonseq[:self.simonlen]:
                print(self.simonlen, "CORRECT!")
                self.update()
                time.sleep(NOTELEN)
                if self.simonlen < len(self.simonseq):
                    self.simonlen += 1
                self.simonplay = True
                self.simonstart = time.time()
                pygame.display.set_caption('Simon (%u notes correct)' % (self.simonlen - 1))
            if self.userseq and self.userseq[-1] != self.simonseq[len(self.userseq) - 1]:
                print("WRONG!")
                self.audio["buzz"].play()
                self.update()
                time.sleep(1.5)
                self.simonplay = True
                self.simonstart = time.time()
                self.userseq = []

    def stopall(self):
        "Stop all notes"
        for k in range(13):
            self.sustain[k].stop()
            self.keys[k] = False

    def draw_wkey(self, k, c):
        "Draw white key"
        pygame.draw.rect(self.screen, BLACK, (100*k, 0, 100, H))
        pygame.draw.rect(self.screen, c, (int(100*k+LW/2), LW, 100-LW, H-2*LW))

    def draw_bkey(self, k, c):
        "Draw black key"
        pygame.draw.rect(self.screen, c, (100*k-BKW, 0, 2*BKW, BKH))

    def pos2key(self, x, y):
        "Get key number from mouse click position"
        for k in 1, 2, 4, 5, 6:
            if y < BKH and (100*k-BKW < x < 100*k+BKW):
                return bkeys[k]
        for k in range(8):
            if y < H and 100*k < x < 100*(k+1):
                return wkeys[k]

    def update(self):
        # Simon plays its melody
        if self.simon and self.simonplay:
            f = ((time.time() - self.simonstart) / NOTELEN) % 1
            if f > 0.8:
                self.keys = 13 * [False]
            n = int((time.time() - self.simonstart) / NOTELEN)
            if n >= self.simonlen:
                self.simonplay = False
                self.simonstart = 0
                self.lastplayed = -1
                self.userseq = []
            elif n > self.lastplayed:
                self.stopall()
                self.play(self.simonseq[n], user = False)
                self.lastplayed = n

        # draw keyboard
        self.screen.fill(BACKGROUND)
        for k in range(8):
            c = WHITE
            for x in wkeys.keys():
                if x == k and self.keys[wkeys[x]]:
                    if self.simon:
                        c = SIMONCOL[k]
                    else:
                        c = ORANGE
            self.draw_wkey(k, c)
        for k in 1, 2, 4, 5, 6:
            c = BLACK
            for x in bkeys.keys():
                if x == k and self.keys[bkeys[x]]:
                    c = ORANGE
            self.draw_bkey(k, c)

        # draw buttons
        if not self.simon:
            pygame.draw.rect(self.screen, ORANGE, RECT_NORMAL, 3)
        else:
            pygame.draw.rect(self.screen, ORANGE, RECT_SIMON, 3)

        # draw volume indicator
        for i in range(1, 11):
            if self.volume >= i:
                c = ORANGE
            else:
                c = GRAY
            pygame.draw.rect(self.screen, c, (20*i+5, 432, 18, 22))

        # draw octave indicator
        for i in 0, 1, 2:
            if self.octave == i:
                c = ORANGE
            else:
                c = GRAY
            pygame.draw.rect(self.screen, c, (70*i+570, 432, 65, 22))

        self.screen.blit(self.overlay, (0, 0))

        pygame.display.flip()

c = Piano()
c.run()

