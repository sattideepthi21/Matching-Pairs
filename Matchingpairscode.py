import pygame
import os
import random 
from pygame import display, event, image , transform,mixer
from time import sleep

IMAGE_SIZE = 128
SCREEN_SIZE = 512
NUM_TILES_SIDE = 4
NUM_TILES_TOTAL = 16
MARGIN = 8
p=0

ASSET_DIR = 'assets'
ASSET_FILES = [x for x in os.listdir(ASSET_DIR) if x[-3:].lower() == 'png']
assert len(ASSET_FILES) == 8

animals_count = dict((a, 0) for a in ASSET_FILES)

def available_animals():
    return [animal for animal, count in animals_count.items() if count < 2]

class Animal:
    def __init__(self, index):
        self.index = index
        self.name = random.choice(available_animals())
        self.image_path = os.path.join(ASSET_DIR, self.name)
        self.row = index // NUM_TILES_SIDE
        self.col = index % NUM_TILES_SIDE
        self.skip = False
        self.image = image.load(self.image_path)
        self.image = transform.scale(self.image, (IMAGE_SIZE - 2 * MARGIN, IMAGE_SIZE - 2 * MARGIN))
        self.box = self.image.copy()
        animals_count[self.name] += 1
        self.box.fill((200, 200, 200))     

def find_index_from_xy(x, y):
    row = y // IMAGE_SIZE
    col = x // IMAGE_SIZE
    index = row * NUM_TILES_SIDE + col
    return row, col, index

pygame.init()
mixer.init()
display.set_caption('Matching Pairs')
screen = display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
matched = image.load('other_assets/matched.png')
won = image.load('other_assets/won.jpg')
start=image.load('start.jpg')
rule=image.load('rule.jpg')
scre=image.load('scre.png')
scre=transform.scale(scre,(512,512))
start=transform.scale(start,(512,512))
rule=transform.scale(rule,(512,512))
won=transform.scale(won,(512,512))
running = True
tiles = [Animal(i) for i in range(0, NUM_TILES_TOTAL)]
current_images_displayed = []
v,i,k=0,0,0
while running:
    if(i==0):
        screen.blit(start,(0,0))
        display.flip()
        mixer.music.load("mat.mp3")
        mixer.music.play()
        sleep(2)
        screen.blit(rule,(0,0))
        display.flip()
        sleep(5)
    i+=1
    if(k==0):
        mixer.music.pause()
        screen.blit(scre,(0,0))
        display.flip()
        li_tile=[]
        li_ind=[]
        ma=[]
        for g,tile in enumerate(tiles):
            li_tile.append(tile)
            li_ind.append(g)
        while(len(ma)!=16):
            na = random.choice(li_ind)
            if(na not in ma):
                row=na//4
                col=na%4
                tile1=li_tile[na].image
                screen.blit(tile1,(col* IMAGE_SIZE + MARGIN, row * IMAGE_SIZE + MARGIN))
                display.flip()
                sleep(0.15)
                ma.append(na)
            if(len(ma)==16):
                sleep(1)
            
    k+=1
    current_events = event.get()

    for e in current_events:
        if e.type == pygame.QUIT:
            pygame.quit()
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            mixer.music.load("tik.mp3")
            mixer.music.play()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col, index = find_index_from_xy(mouse_x, mouse_y)
            if index not in current_images_displayed:
                if len(current_images_displayed) > 1:
                    current_images_displayed = current_images_displayed[1:] + [index]
                else:
                    current_images_displayed.append(index)

    # Display animals
    screen.fill((255, 255, 255))

    total_skipped = 0

    for i, tile in enumerate(tiles):
        current_image = tile.image if i in current_images_displayed else tile.box
        if not tile.skip:
            screen.blit(current_image, (tile.col * IMAGE_SIZE + MARGIN, tile.row * IMAGE_SIZE + MARGIN))
        else:
            total_skipped += 1
    display.flip()

    # Check for matches
    if len(current_images_displayed) == 2:
        idx1, idx2 = current_images_displayed
        if tiles[idx1].name == tiles[idx2].name:
            tiles[idx1].skip = True
            tiles[idx2].skip = True
            # display matched message
            sleep(0.2)
            v+=1
            if(v==8):
                mixer.music.load("win.mp3")
                mixer.music.play()
                screen.blit(won, (0, 0))
                display.flip()
                sleep(2)               
            else:
                screen.blit(matched, (0, 0))
                display.flip()
                sleep(0.5)
            current_images_displayed = []

    
