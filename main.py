import pygame
import neat
import os
import time
import random

WIN_HEIGHT =800
WIN_WIDTH = 600

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0] # to reference bird img

    def jump(self):
        self.vel = -10.5  # top left is 0,0
        self.tick_count =0
        self.height = self.y

    def move(self):  # will be called every single frame for
        self.tick_count +=1 # frame went by
        d = self.vel*self.tick_count + 1.5*self.tick_count**2  #displacment

        if d>= 16:
            d = 16
        if d < 0:
            d-= 2
        self.y = self.y + d

        if d < 0 or self.y < self.height  + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
            else:
                if self.tilt > -90:
                    self.tilt-=  self.ROT_VEL

    def draw(self,win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count ==  self.ANIMATION_TIME*4 +1:
            self.img = self.IMGS[0]
            self.img_count=0
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        win.blit(self.img,(self.x,self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

def draw_window(win,bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200,200)
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    flag = True
    while flag:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        bird.move()
        draw_window(win,bird)

    pygame.quit()
    quit()

main()









