import math
import tkinter as tk
import tkinter.font as tkFont
from tkmacosx import Button
import tkmacosx
import tkinter.messagebox
import time
import re
from tkinter import messagebox
from tkinter import simpledialog
from a1_solution import *
from a2_solution import *
from a1_support import *


class BoardModel:
    def __init__(self,grid_size, num_pokemon):
        self.grid_size = grid_size
        self.num_pokemon = num_pokemon
        self._board = []

    def get_game(self):
        """
        Returns an appropriate representation of the current state of the game board.
        """
        self._board = UNEXPOSED * self.grid_size ** 2

        return self._board

    def get_pokemon_locations(self):
        """
        Returns the indices describing all pokemon locations.
        :return:
        """
        return generate_pokemons(self.grid_size, self.num_pokemon)

    def get_num_attempted_catches(self):
        """
        Returns the number of pokeballs currently placed on the board.
        """
        num = 0
        for i in self._board:
            if i == FLAG:
                num += 1
        return num

    def get_num_pokemon(self):
        """
        Returns the number of pokemon hidden in the game.
        """
        num = 0
        for i in self._board:
            if i == FLAG:
                if self.index_to_position(i) in self.get_pokemon_locations():
                    num += 1
        return self.num_pokemon - num

    def check_loss(self):
        """
        Returns True iff the game has been lost, else False.
        """
        for i in self.get_pokemon_locations():
            j = self.positon_to_index(i)
            if self._board[j] != UNEXPOSED:
                return True

    def index_to_position(self,index):
        """
        Returns the (row, col) coordinate corresponding to the supplied index.
        """
        x = index // self.grid_size
        y = index % self.grid_size
        return x,y

    def positon_to_index(self,position):
        '''
        Returns the index represents the position
        :param position: <int,int>
        :return: <int>
        '''
        x, y = position
        index = x * self.grid_size + y
        return index


class PokemonGame:
    def __init__(self, master: tk.Tk, grid_size=10, num_pokemon=15,task=1):
        self._master = master
        self.grid_size = grid_size
        self.num_pokemon = num_pokemon
        self._game = BoardModel(self.grid_size,self.num_pokemon)
        self.task = task

        self._selection, self._board_view, self._button_frame = None, None, None
        self.draw()

    def open_cell(self):
        pass

    def flag_cell(self):
        pass
        # if game[index] == FLAG :
        #     game = replace_character_at_index(game, index, UNEXPOSED)
        #
        # elif game[index] == UNEXPOSED :
        #     game = replace_character_at_index(game, index, FLAG)

    def redraw(self):
        """Redraw the whole game window."""
        self._selection.destroy()
        self._board_view.destroy()
        self._button_frame.destroy()

        self.draw()

    def draw(self):
        try:
            self._board_view = BoardView(self._master, self._grid_size, self.board_width)
            self._board_view.draw_board(board)
            self._board_view.pack(side=tk.LEFT)
        except AttributeError:
            print("get_board_layout() method needs to be implemented correctly.",
                  "\n")


class BoardView(tk.Canvas):
    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._master = master

        self.grid_size = grid_size
        self.board_width = board_width

    def draw_board(self,board):
        labels = []
        for y, row in enumerate(board) :
            board_row = []
            for x, num in enumerate(row) :
                cell = tkmacosx.Button(height=60, width=60, bg='#228B22')
                cell.grid(row=y + 2, column=x, sticky='W + E + N + S', padx=1, pady=1)

                self.bind_clicks(cell, num, (y,x))
                board_row.append(cell)

            labels.append(board_row)

        return labels

    def get_bbox(self,pixel):
        bbox = []
        x,y = self.pixel_tp_position(pixel)
        if y != 0:
            bbox.append((x-1,y))
        if y != self.grid_size:
            bbox.append((x+1,y))
        if x != 0:
            bbox.appned((x,y-1))
        if x != self.grid_size:
            bbox.append((x,y+1))
        return bbox

    def position_to_pixel(self,position):
        x, y = position
        x_pixel = x * 60 + 30
        y_pixel = y * 60 + 30
        return x_pixel,y_pixel

    def pixel_tp_position(self,pixel):
        x, y = pixel
        x_position = x // 60
        y_position = y // 60
        return x_position, y_position

    def bind_clicks(self, button, index, position):
        """Bind clicks on a label to the left and right click handlers.

        Parameters:
            label (tk.Widget): Label which clicks should bound to.
            tile (Tile): Tile to pass as a parameter to the handlers.
            position (tuple<int, int>): Position to pass as a parameter to the handlers.
        """
        # bind left click
        button.bind("<Button-1>", lambda e, index=index, position=position: self._handle_left_click(index, position))
        # bind right click
        # right click can be either Button-2 or Button-3 depending on operating system
        for i in range(2, 4):
            button.bind(f"<Button-{i}>",
                       lambda e, index=index, position=position: self._handle_right_click(index, position))

    def _handle_left_click(self, pipe, position):
        pass
        """Handle left clicking on a tile to place a pipe.

        Calls the provided place_pipe method if available and pipe is selectable.
        """
        if self.place_pipe is not None and pipe.can_select():
            self.place_pipe(position)

    def _handle_right_click(self, pipe, position):
        pass
        """Handle right clicking on a tile"""
        if self.remove_pipe is not None and pipe.get_id() == "pipe" and pipe.can_select():
            if pipe.get_name() in PIPES.values():
                self.remove_pipe(position)

    # def _load_tile_image(self, tile):
    #     """Load the PhotoImage to use for a given tile.
    #
    #     If the tile class has not been fully implemented defaults to images/tile
    #     """
    #     try:
    #         if tile.get_id() != "tile":
    #             image = get_image(f"images/{tile.get_name()}{tile.get_orientation()}")
    #         else:
    #             image = get_image(f"images/{tile.get_name()}")
    #     except AttributeError:
    #         print("get_name(), get_orientation() and get_id() methods need to be implemented correctly.",
    #               "\n",
    #               "Make sure all class attributes are defined correctly.",
    #               "\n")
    #         image = get_image("images/tile")
    #
    #     return image

#
# def get_image(image_name):
#     """(tk.PhotoImage) Get a image file based on capability.
#
#     If a .png doesn't work, default to the .gif image.
#     """
#     try:
#         image = tk.PhotoImage(file=image_name + ".png")
#     except tk.TclError:
#         image = tk.PhotoImage(file=image_name + ".gif")
#     return image


def main():
    root = tk.Tk()
    root.title("Pokemon: Got 2 Fins Them All!")
    root.geometry('+500+200')
    root.config(bg='black')
    ft = tkFont.Font(family='Fixdsys', size=12, weight=tkFont.BOLD)
    tk.Label(root,text='Pokemon: Got 2 Fins Them All!', fg='white', bg='#F08080', height=3, font=ft).grid(row=0,sticky='we',columnspan=10)
    PokemonGame(root)
    root.mainloop()


if __name__ == '__main__':
    main()