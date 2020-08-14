from PIL import Image
import os
import pygame as pg
import pygame.display
#import Thread


class SpriteSheetLoader:

    def __init__(self):
        self._character_file_name ="spritesheets/characters.png"
        self._enemies_file_name = "/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/enemies.png"
        self._items_file_name = "/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/items.png"
        self.screen = pg.display.get_surface()

    def get_character(self):
        im = Image.open(self._character_file_name)
        # # left = 80
        # # right = 95
        # box_stand = (80,34,95,49)
        # box_run1 = (97,34,112,49)
        # box_run2 = (114,34,129,49)
        # box_run3 = (131,34,146,49)
        # box_run4 = (148,34,163,49)
        # box_jump = (165,34,180,49)
        stand = im.crop((80,34,95,49))
        run1 = im.crop((97,34,112,49))
        run2 = im.crop((114,34,129,49))
        run3 = im.crop((131,34,146,49))
        run4 = im.crop((148,34,163,49))
        jump = im.crop((165,34,180,49))
        run1_left = run1.transpose(Image.FLIP_LEFT_RIGHT)
        run2_left = run2.transpose(Image.FLIP_LEFT_RIGHT)
        run3_left = run3.transpose(Image.FLIP_LEFT_RIGHT)
        run4_left = run4.transpose(Image.FLIP_LEFT_RIGHT)
        jump_left = jump.transpose(Image.FLIP_LEFT_RIGHT)
        stand.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/stand.png")
        run1.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/run1.png")
        run2.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/run2.png")
        run3.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/run3.png")
        run4.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/run4.png")
        jump.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/jump.png")
        run1_left.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/run1_left.png")
        run2_left.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/run2_left.png")
        run3_left.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/run3_left.png")
        run4_left.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/run4_left.png")
        jump_left.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/jump_left.png")

    def get_enemies(self):
        im = Image.open(self._enemies_file_name)
        # mob_walk1 = (0,16,16,32)
        # mob_walk2 = (16,16,32,32)
        # mob_jumped = (32,16,48,32)
        walk1 = im.crop((0,16,16,32))
        walk2 = im.crop((16,16,32,32))
        jumped = im.crop((32,16,48,32))
        walk1.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/walk1.png")
        walk2.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/walk2.png")
        jumped.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/jumped.png")

    def get_item(self):
        im = Image.open(self._items_file_name)
        # coin1 = (0,98,14,112)
        # coin2 = (0,113,14,127)
        # bounce_block1 = (80,0,96,32)
        # bounce_block2 = (96,0,112,32)
        # bounce_block3 = (112,0,128,32)
        coin1 = im.crop((0,98,14,112))
        coin2 = im.crop((0,113,14,127))
        bounce_block1 = im.crop((80,0,96,32))
        bounce_block2 = im.crop((96,0,112,32))
        bounce_block3 = im.crop((112,0,128,32))
        coin1.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/coin1.png")
        coin2.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/coin2.png")
        bounce_block1.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/bounce_block1.png")
        bounce_block2.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/bounce_block2.png")
        bounce_block3.save("/Users/osx/Desktop/CSSE7030/a3——new/a3_files/spritesheets/bounce_block3.png")


def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', 'jpg', 'bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


if __name__ == "__main__" :
    s = SpriteSheetLoader()
    s.get_character()
    #print(load_all_gfx(os.path.join("images")))