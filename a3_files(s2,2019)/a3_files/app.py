"""
Simple 2d world where the player can interact with the items in the world.
"""


__author__ = "Zhiwei Hu"
__date__ = ""
__version__ = "1.1.0"
__copyright__ = "The University of Queensland, 2019"

import math
import tkinter as tk
import tkinter.messagebox
import time
import re

from typing import Tuple, List

import pymunk

from game.block import Block, MysteryBlock
from game.entity import Entity, BoundaryWall
from game.mob import Mob, CloudMob, Fireball
from game.item import DroppedItem, Coin
from game.view import GameView, ViewRenderer
from game.world import World
from game.util import get_collision_direction
from PIL import Image
from tkinter.filedialog import askopenfilename

from level import load_world, WorldBuilder
from player import Player

BLOCK_SIZE = 2 ** 4
MAX_WINDOW_SIZE = (1080, math.inf)

GOAL_SIZES = {
    "flag" : (0.2, 9),
    "tunnel" : (2, 2)
}

BLOCKS = {
    '#' : 'brick',
    '%' : 'brick_base',
    '?' : 'mystery_empty',
    '$' : 'mystery_coin',
    '^' : 'cube',
    'b' : 'bounce',
    'I' : 'flag',
    '=' : 'tunnel',
    'S' : 'switch'
}

ITEMS = {
    'C' : 'coin',
    '*' : 'star',
    "!" : 'flower'
}

MOBS = {
    '&' : "cloud",
    '@' : "mushroom"
}


def create_block(world: World, block_id: str, x: int, y: int, *args) :
    """Create a new block instance and add it to the world based on the block_id.

    Parameters:
        world (World): The world where the block should be added to.
        block_id (str): The block identifier of the block to create.
        x (int): The x coordinate of the block.
        y (int): The y coordinate of the block.
    """
    block_id = BLOCKS[block_id]
    if block_id == "mystery_empty" :
        block = MysteryBlock()
    elif block_id == "mystery_coin" :
        block = MysteryBlock(drop="coin", drop_range=(3, 6))
    elif block_id == "bounce" :
        block = BounceBlock()
    elif block_id == "flag" :
        block = Flag()
    elif block_id == "tunnel" :
        block = Tunnel()
    elif block_id == "switch" :
        block = Switch()

    else :
        block = Block(block_id)

    world.add_block(block, x * BLOCK_SIZE, y * BLOCK_SIZE)


def create_item(world: World, item_id: str, x: int, y: int, *args) :
    """Create a new item instance and add it to the world based on the item_id.

    Parameters:
        world (World): The world where the item should be added to.
        item_id (str): The item identifier of the item to create.
        x (int): The x coordinate of the item.
        y (int): The y coordinate of the item.
    """
    item_id = ITEMS[item_id]
    if item_id == "coin" :
        item = Coin()
    elif item_id == "star" :
        item = Star()
    elif item_id == "flower":
        item = Flower()
    else :
        item = DroppedItem(item_id)

    world.add_item(item, x * BLOCK_SIZE, y * BLOCK_SIZE)


def create_mob(world: World, mob_id: str, x: int, y: int, *args) :
    """Create a new mob instance and add it to the world based on the mob_id.

    Parameters:
        world (World): The world where the mob should be added to.
        mob_id (str): The mob identifier of the mob to create.
        x (int): The x coordinate of the mob.
        y (int): The y coordinate of the mob.
    """
    mob_id = MOBS[mob_id]
    if mob_id == "cloud" :
        mob = CloudMob()
    elif mob_id == "fireball" :
        mob = Fireball()
    elif mob_id == "mushroom" :
        mob = Mushroom()
    else :
        mob = Mob(mob_id, size=(1, 1))

    world.add_mob(mob, x * BLOCK_SIZE, y * BLOCK_SIZE)


def create_unknown(world: World, entity_id: str, x: int, y: int, *args) :
    """Create an unknown entity."""
    world.add_thing(Entity(), x * BLOCK_SIZE, y * BLOCK_SIZE,
                    size=(BLOCK_SIZE, BLOCK_SIZE))


BLOCK_IMAGES = {
    "brick" : "brick",
    "brick_base" : "brick_base",
    "cube" : "cube",
    "bounce" : "bounce_block",
    "flag" : "flag",
    "tunnel" : "tunnel",
    "switch" : "switch"
}

ITEM_IMAGES = {
    "coin" : "coin_item",
    "star" : "star",
    "flower" : "flower"
}

MOB_IMAGES = {
    "cloud" : "floaty",
    "fireball" : "fireball_down",
    "mushroom" : "mushroom"
}
level_name = "level1.txt"


class Mushroom(Mob) :
    """The mushroom mob is a moving entity that moves straight in a direction.

    When colliding with the player it will damage the player and explode.
    """
    _id = "mushroom"

    def __init__(self) :
        super().__init__(self._id, size=(16, 16))
        self._dead = False

    def on_hit(self, event: pymunk.Arbiter, data) :
        '''
        when the player hit the mushroom on both sides, he will loose health and the mushroom will change it's
        moving side. And when the player hit the mushroom on the top, the first time the mushroom will be
        squished and the second time it will be destroyed and removed.
        :param event:
        :param data:
        :return:
        '''
        world, player = data
        if get_collision_direction(player, self) == "R" :
            player.change_health(-1)
            velocity = player.get_velocity()
            player.set_velocity((velocity.x + 50, 0))
        elif get_collision_direction(player, self) == "L" :
            player.change_health(-1)
            velocity = player.get_velocity()
            player.set_velocity((velocity.x - 50, 0))
        elif get_collision_direction(player, self) == "A" :
            if self._dead is not True:
                self._dead = True
                player.set_velocity((0, -120))
            else:
                world.remove_mob(self)
                player.set_velocity((0, -120))

    def is_dead(self):
        return self._dead


class Switch(Block) :

    _id = "switch"
    '''
    This is the switch block, when the player hit it on the top, the bricks around the switch block
    will be removed, and after 10 seconds. they will be added back.
    i use the time.time() as a time counter in this function
    '''
    def __init__(self) :
        super().__init__()
        self._press_time = 0
        self._is_active = True
        self._temp = []

    def on_hit(self, event, data) :
        world, player = data
        if get_collision_direction(player, self) == "A":
            x, y = self.get_position()
            self._temp = world.get_things_in_range(x, y, 20)
            if self._is_active:
                self._is_active = False
                self._press_time = time.time()
                for i in self._temp :
                    if isinstance(i, Block) and not isinstance(i, Switch) :
                        world.remove_block(i)

    def step(self, time_delta, game_data) :
        world, player = game_data
        if time.time() - self._press_time >= 10 and self._is_active is not True:
            # if self._is_active is not True:
                self._is_active = True
                for i in self._temp:
                    if isinstance(i, Block) and not isinstance(i, Switch) :
                        x, y = i.get_position()
                        world.add_block(i, x, y)
                        self._temp =[]

    def is_active(self) -> bool:
        """(bool): Returns true if the block has not yet dropped items."""
        return self._is_active

'''
i write a new MarioViewRenderer class as the postgraduate task. so i don't need it now.
'''
'''
class MarioViewRenderer(ViewRenderer) :
    """A customised view renderer for a game of mario."""

    @ViewRenderer.draw.register(Player)
    def _draw_player(self, instance: Player, shape: pymunk.Shape,
                     view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :

        if shape.body.velocity.x >= 0 :
            image = self.load_image("mario_right")
        else :
            image = self.load_image("mario_left")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="player")]

    @ViewRenderer.draw.register(MysteryBlock)
    def _draw_mystery_block(self, instance: MysteryBlock, shape: pymunk.Shape,
                            view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :
        if instance.is_active() :
            image = self.load_image("coin")
        else :
            image = self.load_image("coin_used")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="block")]

    @ViewRenderer.draw.register(Mushroom)
    def _draw_Mushroom_mob(self, instance: Mushroom, shape: pymunk.Shape,
                           view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :
        if instance.is_dead() :
            image = self.load_image("mushroom_squished")
        else :
            image = self.load_image("mushroom")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="mob")]

    @ViewRenderer.draw.register(Switch)
    def _draw_switch_block(self, instance: Switch, shape: pymunk.Shape,
                            view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :
        if instance.is_active():
            image = self.load_image("switch")
        else :
            image = self.load_image("switch_pressed")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="block")]
    '''


class MarioApp :
    """High-level app class for Mario, a 2d platformer"""

    _world: World

    def __init__(self, master: tk.Tk) :
        """Construct a new game of a MarioApp game.

        Parameters:
            master (tk.Tk): tkinter root widget
        """
        self._master = master
        config_name = askopenfilename(filetypes=( ("Text file", "*.txt"),("HTML files", "*.html;*.htm")))
        self.load_config(config_name)
        self._gravity
        self._level_name
        self._healthdeterminant
        world_builder = WorldBuilder(BLOCK_SIZE, (0,300), fallback=create_unknown)
        world_builder.register_builders(BLOCKS.keys(), create_block)
        world_builder.register_builders(ITEMS.keys(), create_item)
        world_builder.register_builders(MOBS.keys(), create_mob)
        self._builder = world_builder

        self._player = Player(max_health= self._health)
        self._powerup = PowerUp()
        self.reset_world(self._level_name)

        #self._renderer = MarioViewRenderer(BLOCK_IMAGES, ITEM_IMAGES, MOB_IMAGES)
        self._sprite_renderer = SpriteSheetView(BLOCK_IMAGES, ITEM_IMAGES, MOB_IMAGES)
        size = tuple(map(min, zip(MAX_WINDOW_SIZE, self._world.get_pixel_size())))
        self._view = GameView(master, size, self._sprite_renderer)
        self._view.pack()

        self.bind()

        # Wait for window to update before continuing
        master.update_idletasks()

        self._status_view = StatusView(master, self._health)
        self._status_view.pack()
        self._status_view.update_score(self._player.get_score())
        self._status_view.update_health(self._player.get_health())

        self._setup_collision_handlers()
        master.update_idletasks()
        self._start_time = 0
        self.step()
        self.menu = MenuBar(master, [("File", {"Reset" : self._reset,
                                               "Load Level" : self._import_new_level,
                                               "Exit" : self._close,
                                               "High Score": self._status_view.high})])
        self._collide = False

    def load_config(self,file_name):
        """
        load a configuration file, which contain the parameter of this game
        this file will define the new character ,level path, loading position,
        weight, health value and max_velocity.
        :param file_name:
        :return:
        """
        result = []
        f = open(file_name, "r")
        for line in f.readlines() :
            result.append(line.strip('\n'))

        for i in range(len(result)) :
            if result[i] == '==World==' :
                gravity_re = result[i + 1]
                gravity = re.findall(r'(\d+)', gravity_re)
                a = int(gravity[0])
                self._gravity = range(0,a)
                start_level = result[i + 2]
                level = start_level.split(' ')
                self._level_name = level[2]
            if result[i] == '==Player==' :
                character_re = result[i + 1]
                character = character_re.split(' ')
                b = character[2]
                x_re = result[i + 2]
                x = re.findall(r'(\d+)', x_re)
                x = int(x[0])
                y_re = result[i + 3]
                y = re.findall(r'(\d+)', y_re)
                y = int(y[0])
                mass_re = result[i + 4]
                mass = re.findall(r'(\d+)', mass_re)
                mass = int(mass[0])
                health_re = result[i + 5]
                health = re.findall(r'(\d+)', health_re)
                self._health = int(health[0])
                velocity_re = result[i + 6]
                velocity = re.findall(r'(\d+)', velocity_re)
                velocity = int(velocity[0])

    def reset_world(self, new_level: str):
        '''
        reset the current world, and bind the buttons again
        :param new_level:
        :return:
        '''
        self._world = load_world(self._builder, new_level)
        self._world.add_player(self._player, BLOCK_SIZE, BLOCK_SIZE)
        self._builder.clear()
        self.bind()

        self._setup_collision_handlers()

    def bind(self) :
        """Bind all the keyboard events to their event handlers."""
        self._master.bind("<space>", lambda a : self._jump())
        self._master.bind("<Up>", lambda a : self._jump())
        self._master.bind("w", lambda a : self._jump())
        self._master.bind("a", lambda a : self._move(-1, 0))
        self._master.bind("<Left>", lambda a : self._move(-1, 0))
        self._master.bind("d", lambda a : self._move(1, 0))
        self._master.bind("<Right>", lambda a : self._move(1, 0))
        self._master.bind("s", lambda a : self._duck())
        self._master.bind("<Down>", lambda a : self._duck())
        if self._powerup.get_powerup():
            self._master.bind("z", lambda a : self._powerup.fire((self._world, self._player)))

    def _import_new_level(self) :
        '''
        when the user click the load level entry in file menu, this widget will come out.
        :return:
        '''

        def load() :
            self._player.change_health(self._player.get_max_health() - self._player.get_health())
            self._player.change_score(-self._player.get_score())
            level_name = new_name.get()
            self.reset_world(level_name)
            Level_load_new.destroy()

        Level_load_new = tk.Toplevel()
        Level_load_new.geometry('400x100')
        Level_load_new.title('Load New Level')
        new_name = tk.StringVar()
        new_name.set('level1.txt')
        tk.Label(Level_load_new, text='Please enter the level name: ').place(x=10, y=10)
        entry_new_name = tk.Entry(Level_load_new, textvariable=new_name)
        entry_new_name.place(x=200, y=10)
        btn_comfirm = tk.Button(Level_load_new, text='OK', command=load)
        btn_comfirm.place(x=180, y=80)

    def _reset(self) :
        '''reset the current level'''
        self._player.change_health(self._player.get_max_health() - self._player.get_health())
        self._player.change_score(-self._player.get_score())
        self.reset_world(level_name)

    def _close(self) :
        """ Exit the drawing application """
        result = tk.messagebox.askquestion(title="Quiz Window", message="Do you really wanna quiz?")
        if (result == "yes") :
            self._master.destroy()

    def redraw(self) :
        """Redraw all the entities in the game canvas."""
        self._view.delete(tk.ALL)
        self._view.draw_entities(self._world.get_all_things())

    def scroll(self) :
        """Scroll the view along with the player in the center unless
        they are near the left or right boundaries
        """
        x_position = self._player.get_position()[0]
        half_screen = self._master.winfo_width() / 2
        world_size = self._world.get_pixel_size()[0] - half_screen

        # Left side
        if x_position <= half_screen :
            self._view.set_offset((0, 0))

        # Between left and right sides
        elif half_screen <= x_position <= world_size :
            self._view.set_offset((half_screen - x_position, 0))

        # Right side
        elif x_position >= world_size :
            self._view.set_offset((half_screen - world_size, 0))

    def step(self) :
        """Step the world physics and redraw the canvas."""
        data = (self._world, self._player)
        self._world.step(data)

        if self._player.get_health() == 0:
            result = tk.messagebox.askquestion(title="Quiz Window", message="Do you really wanna quiz?")
            if result == "yes":
                self._master.destroy()
            else:
                self._reset()
        self.scroll()
        self.redraw()
        self._master.after(10, self.step)
        self._status_view.update_score((self._player.get_score()))
        if time.time() - self._start_time >= 10 and self._player.get_invincible() is True :
            self._player.set_invincible(False)
        if self._player.get_invincible():
            health = self._player.get_health()
            ratio = health/self._health
            self._status_view._canvas.create_rectangle(0, 0, 1080*ratio, 20, fill="yellow")
            self._status_view._canvas.create_rectangle(1080 * ratio* 0.2, 0, 1080, 20, fill="black")
        else:
            self._status_view.update_health(self._player.get_health())

    def _move(self, dx, dy) :
        ''' make the mario move '''
        self._player.set_velocity((dx * 60, dy * 60))

    def _jump(self) :
        '''make the mario jump'''
        velocity = self._player.get_velocity()
        self._player.set_velocity((velocity.x, -120))

    def _duck(self) :
        '''make the mario duck'''
        velocity = self._player.get_velocity()
        self._player.set_velocity((velocity.x, velocity.y + 120))

    def _tunnel(self, block: Block):
        '''when the player stand on a tunnel and press the <down> or s, this function will bring him to a new level'''
        self.reset_world(new_level=block.get_filename())

    def _setup_collision_handlers(self) :
        self._world.add_collision_handler("player", "item", on_begin=self._handle_player_collide_item)
        self._world.add_collision_handler("player", "block", on_begin=self._handle_player_collide_block,
                                          on_separate=self._handle_player_separate_block)
        self._world.add_collision_handler("player", "mob", on_begin=self._handle_player_collide_mob)
        self._world.add_collision_handler("mob", "block", on_begin=self._handle_mob_collide_block)
        self._world.add_collision_handler("mob", "mob", on_begin=self._handle_mob_collide_mob)
        self._world.add_collision_handler("mob", "item", on_begin=self._handle_mob_collide_item)

    def _handle_mob_collide_block(self, mob: Mob, block: Block, data,
                                  arbiter: pymunk.Arbiter) -> bool :
        '''
        handle when the mob hit other block
        when the mob is fireball and hit a brick, the block will be destroyed
        when the mob is mushroom and hit a brick, it will change its direction
        '''
        if mob.get_id() == "fireball" :
            if block.get_id() == "brick" :
                self._world.remove_block(block)
            self._world.remove_mob(mob)
        if mob.get_id() == "mushroom":
            if get_collision_direction(mob, block) == "L" or get_collision_direction(mob, block) == "R" :
                mob.set_tempo(-mob.get_tempo())
        return True

    def _handle_mob_collide_item(self, mob: Mob, block: Block, data,
                                 arbiter: pymunk.Arbiter) -> bool :
        return False

    def _handle_mob_collide_mob(self, mob1: Mob, mob2: Mob, data,
                                arbiter: pymunk.Arbiter) -> bool :
        '''
        when the mushroom hit a fireball it will be destroyed and when he hit another mushroom it will
        change its direction
        '''
        if mob1.get_id() == "fireball" or mob2.get_id() == "fireball" :
            self._world.remove_mob(mob1)
            self._world.remove_mob(mob2)
        if mob1.get_velocity() == "mushroom" or mob2.get_id() == "mushroom" :
            mob1.set_tempo(-mob1.get_tempo())
            mob2.set_tempo(-mob2.get_tempo())

        return False

    def _handle_player_collide_item(self, player: Player, dropped_item: DroppedItem,
                                    data, arbiter: pymunk.Arbiter) -> bool :
        """Callback to handle collision between the player and a (dropped) item. If the player has sufficient space in
        their to pick up the item, the item will be removed from the game world.

        Parameters:
            player (Player): The player that was involved in the collision
            dropped_item (DroppedItem): The (dropped) item that the player collided with
            data (dict): data that was added with this collision handler (see data parameter in
                         World.add_collision_handler)
            arbiter (pymunk.Arbiter): Data about a collision
                                      (see http://www.pymunk.org/en/latest/pymunk.html#pymunk.Arbiter)
                                      NOTE: you probably won't need this
        Return:
             bool: False (always ignore this type of collision)
                   (more generally, collision callbacks return True iff the collision should be considered valid; i.e.
                   returning False makes the world ignore the collision)
        """

        dropped_item.collect(self._player)
        self._world.remove_item(dropped_item)
        if dropped_item.get_id() == "star" :
            self._player.set_invincible(True)
            self._start_time = time.time()
        if dropped_item.get_id() == "flower":
            self._powerup.set_powerup(True)
        return False

    def _handle_player_collide_block(self, player: Player, block: Block, data,
                                     arbiter: pymunk.Arbiter) -> bool :
        ''' handle when the player hit some blocks, when they are colliding, the on_hit function will run'''
        if block.get_id() == "switch":
            block.on_hit(arbiter, (self._world, player))
            return False
        if block.get_id() == "flag":
            if get_collision_direction(player, block) == "L" or get_collision_direction(player, block) == "R":
                self.reset_world(new_level=block.get_filename())
            if get_collision_direction(player, block) == "A" :
                block.on_hit(arbiter, (self._world, player))
        if block.get_id() == "tunnel":
            if get_collision_direction(player, block) == "A":
                #
                self._master.bind("s", lambda a : self._tunnel(block))
                self._master.bind("<Down>", lambda a : self._tunnel(block))
        else:
            block.on_hit(arbiter, (self._world, player))
        return True

    def _handle_player_collide_mob(self, player: Player, mob: Mob, data,
                                   arbiter: pymunk.Arbiter) -> bool :
        ''' handle when the player hit some mob, when they are colliding, the on_hit function will run'''
        if mob.get_id() == "mushroom" :
            if get_collision_direction(player, mob) == "L" or get_collision_direction(player, mob) == "R" :
                if self._player.get_invincible() :
                    self._world.remove_mob(mob)
                elif self._powerup.get_powerup():
                    self._powerup.set_powerup(False)
                else :
                    mob.on_hit(arbiter, (self._world, player))
                    mob.set_tempo(-mob.get_tempo())
            if get_collision_direction(player, mob) == "A":
                mob.on_hit(arbiter, (self._world, player))
        if mob.get_id() == "fireball" :
            if self._player.get_invincible() :
                self._world.remove_mob(mob)
            elif self._powerup.get_powerup():
                self._powerup.set_powerup(False)
            else :
                mob.on_hit(arbiter, (self._world, player))
                self._world.remove_mob(mob)
        return True

    def _handle_player_separate_block(self, player: Player, block: Block, data,
                                      arbiter: pymunk.Arbiter) -> bool :
        return True


class MenuBar(tk.Menu) :
    """Generic menubar for any window."""

    def __init__(self, master, menus) :
        """
        Parameters:
            master (Tk): Window in which this menu is to be displayed.
            menus (list[tuple(str, dict{str, func})]) :
                         Details of all the menus for this window.
                         List contains the entire set of menus.
                         Tuple is menu name string and dictionary of menu items.
                         Dictionary is menu item name mapped to event handler.
        """
        name_of_menu = 0
        items_of_menu = 1
        super().__init__(master)
        master.config(menu=self)
        for menu_details in menus :
            menu_to_add = tk.Menu(self)
            self.add_cascade(label=menu_details[name_of_menu], menu=menu_to_add)
            for menu_item, event_handler in menu_details[items_of_menu].items() :
                menu_to_add.add_command(label=menu_item, command=event_handler)


class StatusView(tk.Frame) :
    """ status view frame """

    def __init__(self, master,health) :
        """
        Parameters:
            master(tk): windows in which this frame is to be drawn
            health(int): the max health value
        """
        super().__init__(master)

        self._canvas = tk.Canvas(master, width=1080, height=20)
        self._canvas.pack(fill=tk.X)
        self._score_mark = tk.Label(master)
        self._score_mark.pack(side=tk.TOP)
        self._max_health = health

    def update_score(self, new_score_value) :
        '''
        update the score
        :param new_score_value:
        :return:
        '''
        self._score_mark.config(text="Score: {0}".format(new_score_value))

    def update_health(self, new_health_value) :
        '''
        update the health
        use the ratio = health/maxhealth to update the health tag
        :param new_health_value:
        :return:
        '''
        ratio = new_health_value/self._max_health
        if ratio > 0.5:
            self._canvas.create_rectangle(0, 0, 1080*ratio, 20, fill="green")
            self._canvas.create_rectangle(1080 * ratio, 0, 1080, 20, fill="black")
        elif ratio > 0.25:
            self._canvas.create_rectangle(0, 0, 1080 * ratio, 20, fill="orange")
            self._canvas.create_rectangle(1080 * ratio, 0, 1080, 20, fill="black")
        elif ratio >= 0:
            self._canvas.create_rectangle(0, 0, 1080 * ratio, 20, fill="red")
            self._canvas.create_rectangle(1080 * ratio, 0, 1080, 20, fill="black")

    def high(self):
        '''
        the high score widget, but hasn't finished yet
        :return:
        '''
        top = tk.Toplevel()
        top.title('High Score')
        top.geometry('500x300')
        msg = tk.Message(top, text="high score")
        msg.pack()

    def set_score(self, level_name, score):
        self.file_name = level_name + "_score.txt"
        self.high_score = score
        #try:
        file_score = open('self.file_name', "w")
        file_score.write('score')




class BounceBlock(Block) :
    """A bounce block drops items when the player hits its underside.

    The active state of a mystery block is whether it has dropped items or not.
    """
    _id = "bounce"

    def __init__(self) :
        """
        Construct a new mystery block.
        """
        super().__init__()
        self._is_active = False
        self._press_time = 0

    def on_hit(self, event, data) :
        """Callback collision with player event handler."""
        world, player = data
        # Ensure the bottom of the block is being hit
        # if get_collision_direction(player, self) != "A" :
        #     return
        if get_collision_direction(player, self) == "A":
            player.set_velocity((0, -240))
            if self._is_active is not True:
                self._is_active = True
                self._press_time = time.time()
            if time.time()-self._press_time >= 1:
                self._is_active = False
        else :
            return

    def get_active(self):
        return self._is_active


class Star(DroppedItem) :
    ''' this is the star class, when the player hit it, the player will be invincible for 10s'''
    _id = "star"

    def __init__(self) :
        super(Star, self).__init__()
        self._invincible_time = time.time()

    def collect(self, player: Player) :
        pass


class Flag(Block) :
    _id = "flag"
    ''' this is the flag block, when the player hit it, he will go to another level or the game will be finished'''

    def __init__(self, filename="level2.txt") :
        super().__init__()
        self._filename = filename

    def get_cell_size(self) :
        return (0.2, 9)

    def get_filename(self) :
        return self._filename

    def on_hit(self, event, data) :
        pass


class Tunnel(Block) :
    _id = "tunnel"
    ''' 
    this is the tunnel block, when the player stand on it and press and down button,
    he will go to another level
    '''

    def __init__(self, filename="level2.txt") :
        super().__init__()
        self._filename = filename

    def get_cell_size(self) :
        return (2, 2)

    def get_filename(self) :
        return self._filename

    def on_hit(self, event, data) :
        pass


'''
this is the task 3 which entail mario power up and have ability to shoot fireballs
i write a flower class, and use "!" to represent it in the level file. when the player eat the flower he
will grow bigger(hasn't finished yet), and be able to shoot bullet. when the player collide with a fireball
or a mushroom, he will return to origin size and lose the shoot ability.
And a bullet class which represents the bullet.
Finally is a subclass of player, when the player is powered up, this class will be used.
i also want to make the flower drop out of the mystery block, but i hasn't finished yet. 
'''


class Flower(DroppedItem):
    _id = "flower"

    def __init__(self, value: int = 1) :
        """Construct a flower when mario eats it, he will be power up

        """
        super().__init__()

    def collect(self, player: Player) :
        pass


class Bullet(Mob):
    """The fireball mob is a moving entity that moves straight in a direction.

    When colliding with the player it will damage the player and explode.
    """
    _id = "fireball"

    def __init__(self):
        super().__init__(self._id, size=(16, 16), weight=0, tempo=100)

    def on_hit(self, event: pymunk.Arbiter, data):
        world, player = data
        world.remove_mob(Mushroom)


class PowerUp(Player):

    def __init__(self, name: str = "Mario", max_health: float = 20):
        """Construct a new instance of the player.

        Parameters:
            name (str): The player's name
            max_health (float): The player's maximum & starting health
        """
        super().__init__()

        self._powerup = False

    def fire(self, game_data):
        world,player = game_data
        if player.get_powerup:
            x, y = player.get_position()
            drop = Bullet()
            world.add_mob(drop, x+50, y)
        else:
            pass

    def set_powerup(self, powerup: bool):
        self._powerup = powerup

    def get_powerup(self):
        return self._powerup

    # def step(self, time_delta, game_data):
    #     world, player = game_data
    #     x, y = self.get_position()
    #     self._master.bind("<Down>", lambda a : self._duck())
    #     drop = Fireball()
    #     world.add_mob(drop, x, y + 22)


    '''
    Here is the postgraduate task, which contain two classes.
    the first is SpriteSheetLoader, which i use to get the image from the spritesheets floder.
    and the other is SpriteSheetView which is a subclass of ViewRenderer. It is more powerful 
    than the MarioViewRenderer class.
    '''
class SpriteSheetLoader:
    '''
    in this class i use the PIL library to cut the smaller image from the big image, i counter the
    pixel in the big image. and use crop function to cut it down and svae it in the floder.
    there are 3 instances which are used to get the character images, the enemies images and the item images
    '''
    def __init__(self):
        self._character_file_name ="spritesheets/characters.png"
        self._enemies_file_name = "spritesheets/enemies.png"
        self._items_file_name = "spritesheets/items.png"

    def get_character(self):
        im = Image.open(self._character_file_name)
        stand = im.crop((80,34,95,49))
        run1 = im.crop((97,34,112,49))
        run2 = im.crop((114,34,129,49))
        run3 = im.crop((131,34,146,49))
        run4 = im.crop((148,34,163,49))
        jump = im.crop((165,34,180,49))
        stand_left = stand.transpose(Image.FLIP_LEFT_RIGHT)
        run1_left = run1.transpose(Image.FLIP_LEFT_RIGHT)
        run2_left = run2.transpose(Image.FLIP_LEFT_RIGHT)
        run3_left = run3.transpose(Image.FLIP_LEFT_RIGHT)
        run4_left = run4.transpose(Image.FLIP_LEFT_RIGHT)
        jump_left = jump.transpose(Image.FLIP_LEFT_RIGHT)
        stand.save("spritesheets/stand.png")
        run1.save("spritesheets/run1.png")
        run2.save("spritesheets/run2.png")
        run3.save("spritesheets/run3.png")
        run4.save("spritesheets/run4.png")
        jump.save("spritesheets/jump.png")
        stand_left.save("spritesheets/stand_left.png")
        run1_left.save("spritesheets/run1_left.png")
        run2_left.save("spritesheets/run2_left.png")
        run3_left.save("spritesheets/run3_left.png")
        run4_left.save("spritesheets/run4_left.png")
        jump_left.save("spritesheets/jump_left.png")

    def get_enemies(self):
        im = Image.open(self._enemies_file_name)
        walk1 = im.crop((0,16,16,32))
        walk2 = im.crop((16,16,32,32))
        jumped = im.crop((32,16,48,32))
        walk1.save("spritesheets/walk1.png")
        walk2.save("spritesheets/walk2.png")
        jumped.save("spritesheets/jumped.png")

    def get_item(self):
        im = Image.open(self._items_file_name)
        coin1 = im.crop((0,98,14,112))
        coin2 = im.crop((0,113,14,127))
        bounce_block1 = im.crop((80,0,96,32))
        bounce_block2 = im.crop((96,0,112,32))
        bounce_block3 = im.crop((112,0,128,32))
        flower = im.crop((0,32,16,48))
        coin1.save("spritesheets/coin1.png")
        coin2.save("spritesheets/coin2.png")
        bounce_block1.save("spritesheets/bounce_block1.png")
        bounce_block2.save("spritesheets/bounce_block2.png")
        bounce_block3.save("spritesheets/bounce_block3.png")
        flower.save("images/flower.png")


class SpriteSheetView(ViewRenderer):
    '''
    this is the new viewrenderer subclass. which could load image from the new floder
    and make the objects move like animation.
    here i use the time.time() as counter to change to load image, which will looks like
    animation
    '''
    def load_image2(self, file: str) -> tk.PhotoImage:
        """Load an image in the file location of images/{file}.png or images/{file}.gif

        Caches the image within the class so it can be drawn within the canvas.
        """
        if file in self._images:
            return self._images[file]

        #try:
        image = tk.PhotoImage(file="spritesheets/" + file + ".png")
        # except tk.TclError:
        #     image = tk.PhotoImage(file="spritesheets/" + file + ".gif")
        self._images[file] = image

        return image

    @ViewRenderer.draw.register(Coin)
    def _draw_coin_item(self, instance: Coin, shape: pymunk.Shape,
                     view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :

        if time.time() % 0.5 <= 0.25 :
            image = self.load_image2("coin1")
        else :
            image = self.load_image2("coin2")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="item")]

    @ViewRenderer.draw.register(Player)
    def _draw_player(self, instance: Player, shape: pymunk.Shape,
                     view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :
        if shape.body.velocity.y != 0:
            if shape.body.velocity.x >= 0:
                image = self.load_image2("jump")
            else:
                image = self.load_image2("jump_left")
        elif shape.body.velocity.x == 0:
            image = self.load_image("mario_right")
        elif shape.body.velocity.x > 0 :
            if time.time() % 0.6 <= 0.15:
                image = self.load_image2("stand")
            elif time.time() % 0.6 <= 0.3:
                image = self.load_image2("run3")
            elif time.time() % 0.6 <= 0.45:
                image = self.load_image2("run2")
            else:
                image = self.load_image2("run1")
        else :
            if shape.body.velocity.x == 0:
                image = self.load_image("mario_left")
            elif time.time() % 0.6 <= 0.15:
                image = self.load_image2("stand_left")
            elif time.time() % 0.6 <= 0.3:
                image = self.load_image2("run3_left")
            elif time.time() % 0.6 <= 0.45:
                image = self.load_image2("run2_left")
            else:
                image = self.load_image2("run1_left")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="player")]

    @ViewRenderer.draw.register(MysteryBlock)
    def _draw_mystery_block(self, instance: MysteryBlock, shape: pymunk.Shape,
                            view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :
        if instance.is_active() :
            image = self.load_image("coin")
        else :
            image = self.load_image("coin_used")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="block")]

    @ViewRenderer.draw.register(Mushroom)
    def _draw_Mushroom_mob(self, instance: Mushroom, shape: pymunk.Shape,
                           view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :
        if instance.is_dead() :
            image = self.load_image2("jumped")
        else :
            if time.time() % 0.5 <= 0.25:
                image = self.load_image2("walk1")
            else:
                image = self.load_image2("walk2")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="mob")]

    @ViewRenderer.draw.register(Switch)
    def _draw_switch_block(self, instance: Switch, shape: pymunk.Shape,
                           view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :
        if instance.is_active() :
            image = self.load_image("switch")
        else :
            image = self.load_image("switch_pressed")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="block")]

    @ViewRenderer.draw.register(BounceBlock)
    def _draw_bounce_block(self, instance: BounceBlock, shape: pymunk.Shape,
                            view: tk.Canvas, offset: Tuple[int, int]) -> List[int] :
        if instance.get_active() :
            if time.time() %1<= 0.25:
                image = self.load_image2("bounce_block3")
            elif time.time() %1 <= 0.5:
                image = self.load_image2("bounce_block2")
            elif time.time() % 1 <= 0.75:
                image = self.load_image2("bounce_block1")
            else:
                image = self.load_image2("bounce_block2")
        else :
            image = self.load_image2("bounce_block2")

        return [view.create_image(shape.bb.center().x + offset[0], shape.bb.center().y,
                                  image=image, tags="block")]


def main() :
    s = SpriteSheetLoader()
    s.get_character()
    s.get_enemies()
    s.get_item()
    root = tk.Tk()
    root.title("Mario")
    app = MarioApp(root)
    root.mainloop()


if __name__ == "__main__" :
    main()
