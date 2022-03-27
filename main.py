import pygame
import neat
import os
import time
import random
pygame.font.init()

WIN_HEIGHT =800
WIN_WIDTH = 600

BIRD_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pla.png")))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","roadf.png")))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","xp.png")),(600,800))

# Font

FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    IMG = BIRD_IMG

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img = self.IMG # to reference bird img

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


    def draw(self,win):

        win.blit(self.img,(self.x,self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height-self.PIPE_TOP.get_height() # gets height
        self.bottom = self.height+ self.GAP

    def move(self):
        self.x -= self.VEL
    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x,self.top - round(bird.y))
        bottom_offset = (self.x - bird.x,self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset) # none if no collide
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG,(self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))





def draw_window(win,bird,pipes,base, score):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = FONT.render("Score : "+ str(score), True, (255, 255, 255))
    win.blit(text,(WIN_WIDTH-10 - text.get_width(),10))
    bird.draw(win)
    base.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200,200)
    base = Base(650)
    pipes = [Pipe(600)]
    score = 0
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    flag = True
    while flag:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                bird.jump()



        bird.move()
        rem =[]
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        # if touches ground
        if bird.y >= 730:
            pass



        base.move()
        draw_window(win,bird,pipes,base,score)

    pygame.quit()
    quit()

main()









