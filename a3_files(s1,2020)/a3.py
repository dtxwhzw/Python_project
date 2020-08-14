import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import random
import json
import os


UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")

POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"
TASK_ONE = 'color_mode'
TASK_TWO = 'image_mode'
TITLE = 'Pokemon: Got 2 Find Them All!'
WIN = 'win'
LOST = 'lost'
RUNNING = 'running'
NUMBER_LIST = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']


class BoardModel:
    '''
    Class to maintain game data
    '''
    def __init__(self,grid_size, num_pokemon):
        '''
        Initiate an instance
        :param grid_size (int): The grid size of the game.
        :param num_pokemon (int): The number of pokemons that the game will have.
        '''
        self.grid_size = grid_size
        self.num_pokemon = num_pokemon
        self._board = UNEXPOSED * self.grid_size ** 2
        self._pokemon_locations = self.generate_pokemons()

    def generate_pokemons(self):
        """Pokemons will be generated and given a random index within the game.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = self.grid_size ** 2
        pokemon_locations = ()

        for _ in range(self.num_pokemon):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count - 1)

            while index in pokemon_locations:
                index = random.randint(0, cell_count - 1)

            pokemon_locations += (index,)

        return pokemon_locations

    def get_game(self):
        """
        Returns an appropriate representation of the current state of the game board.
        """
        return self._board

    def get_pokemon_locations(self):
        """
        Returns the indices describing all pokemon locations.
        """
        return self._pokemon_locations

    def get_num_attempted_catches(self):
        """
        Returns the number of pokeballs currently placed on the board.
        """
        num = 0
        for i in self._board:
            if i == FLAG:
                num += 1
        return num

    def restart_game(self):
        '''
        Reset game board to unexposed state, do not change the pokemon locations
        '''
        for index in range(len(self._board)):
            self.replace_character_at_index(index, UNEXPOSED)

    def new_game(self):
        '''
        Generate new pokemon locations then reset the game board
        '''
        self._pokemon_locations = self.generate_pokemons()
        self.restart_game()

    def index_to_position(self,index):
        '''
        :param index: the index to be transformed
        Returns the (row, col) coordinate corresponding to the supplied index.
        '''
        x = index // self.grid_size
        y = index % self.grid_size
        return x, y

    def position_to_index(self,position):
        '''
        Returns the index represents the position
        :param position: <int,int>
        :return: <int>
        '''
        x, y = position
        index = x * self.grid_size + y
        return int(index)

    def replace_character_at_index(self, index, character):
        """A specified index in the game string at the specified index is replaced by
        a new character.
        Parameters:
            game (str): The game string.
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """
        self._board = self._board[:index] + character + self._board[index + 1:]

    def flag_cell(self, index):
        """Toggle Flag on or off at selected index. If the selected index is already
            revealed, the game would return with no changes.

            Parameters:
                index (int): The index in the game string where a flag is placed.
            Returns
                (str): the original state of the index place
        """
        if self._board[index] == FLAG:
             self.replace_character_at_index(index, UNEXPOSED)
             return FLAG

        elif self._board[index] == UNEXPOSED:
            self.replace_character_at_index(index, FLAG)
            return UNEXPOSED

    def _index_in_direction(self, index, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        For example:
          | 1 | 2 | 3 |
        A | i | j | k |
        B | l | m | n |
        C | o | p | q |

        The index of m is 4 in the game string.
        if the direction specified is "up" then:
        the updated position corresponds with j which has the index of 1 in the game string.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
        # convert index to row, col coordinate
        col = index % self.grid_size
        row = index // self.grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        # Notice the use of if, not elif here
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1
        if not (0 <= col < self.grid_size and 0 <= row < self.grid_size):
            return None
        return self.position_to_index((row, col))

    def _neighbour_directions(self, index):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self._index_in_direction(index, direction)
            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def number_at_cell(self, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
        if self._board[index] != UNEXPOSED:
            return int(self._board[index])

        number = 0
        for neighbour in self._neighbour_directions(index):
            if neighbour in self._pokemon_locations:
                number += 1

        return number

    def reveal_cells(self, index):
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (str): The updated game string
        """
        number = self.number_at_cell(index)
        self.replace_character_at_index(index, str(number))
        clear = self._big_fun_search(index)
        for i in clear:
            if self._board[i] != FLAG:
                number = self.number_at_cell(i)
                self.replace_character_at_index(i, str(number))

    def _big_fun_search(self, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Using some sick algorithms.

        Find all cells which should be revealed when a cell is selected.

        For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
        neighbours are revealed. If one of the neighbouring cells is also zero then
        all of that cell"s neighbours are also revealed. This repeats until no
        zero value neighbours exist.

        For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
        the cell itself is revealed.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []

        if self._board[index] == FLAG:
            return queue

        number = self.number_at_cell(index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self._neighbour_directions(node):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if self._board[neighbour] != FLAG:
                    number = self.number_at_cell(neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def load_data(self, board=None, pokemon_locaitons=None):
        '''
        Update variables from given values
        '''
        if board:
            self._board = board
        if pokemon_locaitons:
            self._pokemon_locations = pokemon_locaitons


class PokemonGame:
    '''
    Class to control the game running
    '''
    SCORE_TXT_PATH = 'scores.txt'
    def __init__(self, master, grid_size=10, num_pokemon=15,task=TASK_ONE):
        '''
        :param master: game window
        :param grid_size: grid_size
        :param num_pokemon: number of pokemons
        :param task: task mode
        '''
        self._master = master
        self.grid_size = grid_size
        self.num_pokemon = self.pokeball_left = num_pokemon
        self.attempted_catches = 0
        self.task = task
        self.board_view =  BoardView(self._master, self.grid_size)

        self._master.title(TITLE)
        self._master.configure(background='white')
        self.game_state = RUNNING
        self._title_label = tk.Label(master=self._master, text=TITLE, fg='white', bg='Crimson',
                                     width=40, font=('', 20, 'bold'), relief='raised')
        self._title_label.pack()

        if self.task == TASK_TWO:
            # Some variables that only needed in task two
            self.board_view = ImageBoardView(self._master, self.grid_size)
            self.status_bar = StatusBar(self._master, self.pokeball_left)
            self.bind_status_bar()
            self.status_bar.after(1000, self.update_time_elapsed)
            self.status_bar.pack(side=tk.BOTTOM)
            self.time_elapsed = 0
            self.generate_menu()
            self.win_window = None
            self.scores_window = None
        self.bind_game_board()

    def run(self):
        '''
        Start mainloop, run the game
        '''
        self._board_model = BoardModel(self.grid_size, self.num_pokemon)
        self.flash_game_board()
        self._master.mainloop()

    def reset(self):
        '''
        Some variables need to be reset when the game starts
        '''
        self.time_elapsed = 0
        self.game_state = RUNNING
        self.attempted_catches = 0
        self.pokeball_left = self.num_pokemon
        self.win_window = None
        self.scores_window = None
        self.status_bar.reset()
        self.status_bar.after(1000, self.update_time_elapsed)

    def restart_game(self, event=None):
        '''
        Restart the current game, do not change the pokemon locations
        '''
        self._board_model.restart_game()
        self.reset()
        self.flash_game_board()

    def new_game(self, event=None):
        '''
        Start a new game with new locations of pokemons
        '''
        self._board_model.new_game()
        self.reset()
        self.flash_game_board()

    def flash_game_board(self):
        '''
        flash the game board by destroy the existing one and create a new one
        '''
        if self.board_view:
            self.board_view.destroy()
        if self.task == TASK_ONE:
            self.board_view = BoardView(self._master, self.grid_size)
        else:
            self.board_view = ImageBoardView(self._master, self.grid_size)
        self.board_view.pack()
        self.bind_game_board()
        self.board_view.draw_board(self._board_model.get_game())
        self.show_result()

    def update_time_elapsed(self):
        '''
        Update elapsed time using after method of tkinter.
        Every 1000 microseconds passed the elapsed time + 1
        '''
        if self.game_state == RUNNING:
            self.time_elapsed += 1
            self.status_bar.after(1000, self.update_time_elapsed)
            self.status_bar.update_values(time_elapsed=self.time_elapsed)

    def bind_game_board(self):
        '''
        Bind events of board_view, left click and right click
        '''
        if self.board_view:
            self.board_view.bind('<Button-1>', self._handle_left_click)
            self.board_view.bind('<Button-2>', self._handle_right_click)
            self.board_view.bind('<Button-3>', self._handle_right_click)

    def bind_status_bar(self):
        '''
        Bind events of status bar: new game and restart game
        '''
        self.status_bar.new_game_btn.bind('<Button-1>', self.new_game)
        self.status_bar.restart_game_btn.bind('<Button-1>', self.restart_game)

    def _handle_click(self, event):
        '''
        Basic function to handle click event(both left and right)
        Calculate position and index
        '''
        if self.game_state == RUNNING:
            x = event.x
            y = event.y
            position = self.board_view.pixel_to_position((x, y))
            index = self._board_model.position_to_index(position)
            return index
        else:
            return None

    def _handle_left_click(self, event):
        '''
        Function to handle left click event
        1. Get the clicked grid
        2. Get current state of the clicked grid
        3. Reveal it if it is not flag
        '''
        index = self._handle_click(event)
        if not index and index!=0 :
            return None
        board = self._board_model.get_game()
        if board[index] == FLAG:
            pass
        elif index in self._board_model.get_pokemon_locations():
            self.game_state = LOST
            for loc in self._board_model.get_pokemon_locations():
                self._board_model.replace_character_at_index(loc, POKEMON)
        else:
            self._board_model.reveal_cells(index)

        if self.check_win():
            self.game_state = WIN
            if self.task == TASK_TWO:
                self.show_win_window()
        self.flash_game_board()

    def show_win_window(self):
        '''
        After player win, create a window to allow the player enter a name
        '''
        self.win_window = tk.Tk()
        win_text = f'You win in {self.status_bar.format_time(self.time_elapsed)}! Enter your name:\n'
        win_label = tk.Label(master=self.win_window, text=win_text)
        self.name_entry = tk.Entry(master=self.win_window)
        enter_btn = tk.Button(master=self.win_window, text='enter', command=self.after_enter_name)
        win_label.pack()
        self.name_entry.pack()
        enter_btn.pack()

    def after_enter_name(self, event=None):
        '''
        After player entered a name and confirmed
        1. Get current scores list from the file
        2. Compare the player's score with the list,
            insert into appropriate position
        3. Write the new list to the file
        '''
        index = None
        name = self.name_entry.get()
        if len(name) == 0:
            pass
        else:
            score_text = name + ': ' + str(self.time_elapsed) + '\n'
            scores, scores_text = self.get_scores()
            if len(scores) == 0:
                index = 0
            for s in scores:
                if self.time_elapsed < s:
                    index = scores.index(s)
                    break
            if not index and len(scores) <3:
                index = len(scores)
            if index or index==0:
                scores_text.insert(index, score_text)
            if len(scores_text) > 3:
                del scores_text[-1]
            with open(self.SCORE_TXT_PATH, 'w') as f:
                f.write(''.join(scores_text))
            self.win_window.destroy()

    def _handle_right_click(self, event):
        '''
        Function to handle left click event
        1. Get the clicked grid
        2. Get current state of the clicked grid
        3. Flag it if it is not flag or unflag it if it is flag,
           note the change of the number of left pokeballs and attempted catches
        '''
        index = self._handle_click(event)
        if not index and index!=0 :
            return None
        response = self._board_model.flag_cell(index)
        if response == UNEXPOSED:
            self.pokeball_left -= 1
            if self.pokeball_left < 0:
                self.pokeball_left = 0
                self._board_model.flag_cell(index)
            else:
                self.attempted_catches += 1
        else:
            self.attempted_catches -= 1
            if self.attempted_catches < 0:
                self.attempted_catches = 0
                self._board_model.flag_cell(index)
            else:
                self.pokeball_left += 1
        self.flash_game_board()
        if self.check_win():
            self.game_state = WIN
            if self.task == TASK_TWO:
                self.show_win_window()
        if self.task == TASK_TWO:
            self.status_bar.update_values(pokeball_left=self.pokeball_left,
                                      attempted_catches=self.attempted_catches)

    def check_win(self):
        """Checking if the player has won the game.
        Returns:
            (bool): True if the player has won the game, false if not.
        """
        board = self._board_model.get_game()
        return UNEXPOSED not in board and board.count(FLAG) == self.num_pokemon

    def show_result(self):
        '''
        Show a result messagebox when the player win or lose
        '''
        if self.task == TASK_ONE:
            if self.game_state == LOST:
                messagebox.showinfo(title='LOSE', message='You lose!')
            elif self.game_state == WIN:
                messagebox.showinfo(title='WIN', message='You win!')
        else:
            if self.game_state == LOST:
                response = messagebox.askokcancel(title='Game Over',
                                                  message='You lose! Would you like to play again?')
                if response:
                    self.new_game()
                else:
                    self.quit()

    def quit(self):
        '''
        Quit root window
        '''
        self._master.quit()

    def save_game(self):
        '''
        Use a dict to record the current game data
        Save it into a json file
        '''
        game_data = {
            'board': self._board_model.get_game(),
            'pokemon_locations': self._board_model.get_pokemon_locations(),
            'time_elapsed': self.time_elapsed
        }
        save_path = filedialog.askdirectory()
        with open(save_path + '/game_data.json', 'w') as f:
            json.dump(game_data, f)
        messagebox.showinfo(title='Save Game', message='Successfully saved!')

    def load_game(self):
        '''
        Read game data from the json file
        '''
        load_path = filedialog.askopenfilename()
        with open(load_path, 'r') as f:
            game_data = json.load(f)
        self.time_elapsed = game_data.get('time_elapsed')
        self._board_model.load_data(board=game_data.get('board'),
                                    pokemon_locaitons=game_data.get('pokemon_locations'))
        self.flash_game_board()
        messagebox.showinfo(title='Load Game', message='Successfully loaded!')

    def generate_menu(self):
        '''
        Generate the menu bar and all the commands
        '''
        filemenu = tk.Menu(self._master)
        filemenu.add_command(label='Save Game', command=self.save_game)
        filemenu.add_command(label='Load Game', command=self.load_game)
        filemenu.add_command(label='Restart Game', command=self.restart_game)
        filemenu.add_command(label='New Game', command=self.new_game)
        filemenu.add_command(label='Quit', command=self.quit)
        filemenu.add_command(label='High Scores', command=self.show_high_scores)
        self._master.config(menu=filemenu)
        return filemenu

    def show_high_scores(self):
        '''
        Get scores from the score file
        Transform them to appropriate format to display
        '''
        self.scores_window = tk.Tk()
        head_label = tk.Label(master=self.scores_window, text='High Scores', fg='white', bg='Crimson',
                            font=('', 20, 'bold'), relief='raised')
        head_label.pack()
        scores_text_list = self.get_scores()[1]
        scores_text = ''
        if len(scores_text_list) > 0:
            for i in scores_text_list:
                name = i.split(':')[0]
                time_elapsed = i.split(':')[1]
                scores_text += (name+': '+self.status_bar.format_time(time_elapsed)+'\n')
        scores_label = tk.Label(master=self.scores_window, text=scores_text, font=('', 14, 'bold'))
        scores_label.pack()
        done_btn = tk.Button(master=self.scores_window, text='Done', command=self.scores_window.destroy)
        done_btn.pack()

    def get_scores(self):
        '''
        Get scores from score file
        '''
        scores_text = []
        scores = []
        if not (os.path.exists(self.SCORE_TXT_PATH)):
            with open(self.SCORE_TXT_PATH, 'w') as f:
                pass
        with open(self.SCORE_TXT_PATH, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                for line in lines:
                    time_elapsed = int(line.split(':')[1])
                    scores.append(time_elapsed)
                    scores_text.append(line)
        return scores, scores_text


class BoardView(tk.Canvas):
    '''
    Class to display the game board
    '''

    TALL_GRASS_COLOR = 'darkgreen'
    SHORT_GRASS_COLOR = 'lightgreen'
    ATTEMPTED_CATCH_COLOR = 'red'
    EXPOSED_POKEMON_COLOR = 'yellow'

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        '''
        Initiate constructor
        :param master: the game windowleft pokeballs, from controller
        :param grid_size: number of grid size, from controller
        :param board_width: board width
        '''
        super().__init__(master, width=board_width, height=board_width, *args, **kwargs)
        self._master = master
        self.grid_size = grid_size
        self.board_width = board_width
        self.grid_length = board_width/10
        self.grid_list = []

    def draw_board(self, board):
        '''
        Draw the game board based on the board state
        Loop the board state, for different state, draw grid with specific color
        :param board: board state
        '''
        for i in range(len(board)):
            position = self.index_to_position(i)
            state = board[i]
            if state == POKEMON:
                grid = self.draw_grid(position, self.EXPOSED_POKEMON_COLOR)
            elif state == FLAG:
                grid = self.draw_grid(position, self.ATTEMPTED_CATCH_COLOR)
            elif state == UNEXPOSED:
                grid = self.draw_grid(position, self.TALL_GRASS_COLOR)
            else:
                grid = self.draw_grid(position, self.SHORT_GRASS_COLOR)
                self.create_text(self.position_to_pixel(position), text=state)
            self.grid_list.append(grid)
        self.bind('<Motion>', self.highlight_grid)

    def highlight_grid(self, event):
        '''
        Highlight an unrevealed grid when mouse on
        Calculate the grid index based on the pixel of mouse
        Change outline width and color of the grid
        '''
        pixel = (event.x, event.y)
        position = self.pixel_to_position(pixel)
        index = self.position_to_index(position)
        for i in range(len(self.grid_list)):
            if index == i:
                self.itemconfig(self.grid_list[i], width=2, outline='gold')
            else:
                self.itemconfig(self.grid_list[i], width=1, outline='black')

    def draw_grid(self, position, fill_color):
        '''
        Draw grid based on given color
        '''
        pixel = self.position_to_pixel(position)
        r, c = pixel
        half_length = self.grid_length/2
        return self.create_rectangle(r-half_length, c-half_length, r+half_length, c+half_length,
                              fill=fill_color)

    def index_to_position(self, index):
        '''
        :param index: the index to be transformed
        Returns the (row, col) coordinate corresponding to the supplied index.
        '''
        x = index % self.grid_size
        y = index // self.grid_size
        return (x, y)

    def position_to_index(self, position):
        '''
        Returns the index represents the position
        :param position: <int,int>
        :return: <int>
        '''
        x, y = position
        return int(x*self.grid_size+y)

    def pixel_to_position(self, pixel):
        '''
        :param pixel: the pixel to be transformed
        Returns the (row, col) coordinate corresponding to the supplied pixel.
        '''
        return (pixel[1]//self.grid_length, pixel[0]//self.grid_length)

    def position_to_pixel(self, position):
        '''
        Returns the pixel represents the position
        :param position: <int,int>
        :return: <int>
        '''
        return ((position[0]+0.5)*self.grid_length, (position[1]+0.5)*self.grid_length)


class ImageBoardView(BoardView):
    '''
    Class to display game using images
    '''
    POKEMON_NAME_LIST = ['charizard', 'cyndaquil', 'pikachu', 'psyduck', 'togepi', 'umbreon']
    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        '''
        Compared to normal board view, just need load images
        '''
        super().__init__(master, grid_size, board_width, *args, **kwargs)
        self.load_images()

    def draw_board(self, board):
        '''
        Draw the game board based on the board state
        Loop the board state, for different state, draw grid with specific image
        :param board: board state
        '''
        sprite_index = 0

        for i in range(len(board)):
            position = self.index_to_position(i)
            state = board[i]
            if state == POKEMON:
                grid = self.draw_grid(position, random.choice(self.sprite_images))
                sprite_index += 1
            elif state == FLAG:
                grid = self.draw_grid(position, self.pokeball_image)
            elif state == UNEXPOSED:
                grid = self.draw_grid(position, self.unrevealed_image)
            else:
                grid = self.draw_grid(position, self.number_images[int(state)])
            self.grid_list.append(grid)
        self.bind('<Motion>', lambda event: self.highlight_unrevealed_grid(event, board))

    def draw_grid(self, position, image):
        '''
        Draw grid based on given image
        '''
        pixel = self.position_to_pixel(position)
        x, y = pixel
        return self.create_image(x, y, image=image)

    def load_images(self):
        '''
        Load all of the needed images to memory
        '''
        self.unrevealed_image = self.get_image('unrevealed')
        self.unrevealed_moved_image = self.get_image('unrevealed_moved')
        self.pokeball_image = self.get_image('pokeball')
        self.unrevealed_image = self.get_image('unrevealed')
        self.unrevealed_image = self.get_image('unrevealed')
        self.load_number_images()
        self.load_sprites_images()

    def load_number_images(self):
        '''
        Load all number adjacent images to memory
        Use a list to store them so that we can use them when we need
        '''
        self.number_images = []
        for number in NUMBER_LIST:
            number_name = number + '_adjacent'
            image = self.get_image(number_name)
            self.number_images.append(image)

    def load_sprites_images(self):
        '''
        Load all pokemon images to memory
        Use a list to store them so that we can use them when we need
        '''
        self.sprite_images = []
        for name in self.POKEMON_NAME_LIST:
            sprite_name = 'pokemon_sprites/' + name
            image = self.get_image(sprite_name)
            self.sprite_images.append(image)

    def highlight_unrevealed_grid(self, event, board):
        '''
        Highlight an unrevealed grid when mouse on
        Calculate the grid index based on the pixel of mouse
        Change image of the grid
        '''
        pixel = (event.x, event.y)
        position = self.pixel_to_position(pixel)
        index = self.position_to_index(position)
        for i in range(len(self.grid_list)):
            if board[i] == UNEXPOSED:
                if index == i:
                    self.itemconfig(self.grid_list[i], image=self.unrevealed_moved_image)
                else:
                    self.itemconfig(self.grid_list[i], image=self.unrevealed_image)

    def get_image(self, image_name):
        """(tk.PhotoImage) Get a image file based on capability.

        If a .png doesn't work, default to the .gif image.
        """
        try:
            image = tk.PhotoImage(file='images/' + image_name + ".png")
        except tk.TclError:
            image = tk.PhotoImage(file='images/' + image_name + ".gif")
        return image


class StatusBar(tk.Frame):
    '''
    Class to display status
    '''
    def __init__(self, master, pokeball_left, attempted_catches=0, time_elapsed=0, board_width=600, *args, **kwargs):
        '''
        Initiate constructor
        :param master: the game window
        :param pokeball_left: number of left pokeballs, from controller
        :param attempted_catches: number of placed pokeballs, from controller
        :param time_elapsed: elapsed time, from controller
        :param board_width:
        '''
        super().__init__(master, width=board_width, *args, **kwargs)
        self._master = master
        self.attempted_catches = self.init_attempted_catches = attempted_catches
        self.pokeball_left = self.init_pokeball_left = pokeball_left
        self.time_elapsed = self.init_time_elapsed = time_elapsed
        self.configure(background='white')
        self.pokeball_text = tk.StringVar()
        self.pokeball_text.set(f'{self.attempted_catches} attemped catches\n'
                               f'{self.pokeball_left} pokeball left')
        self.clock_text = tk.StringVar()
        self.clock_text.set(f'Time elapsed\n'
                            f'{self.format_time(self.time_elapsed)}')
        self.draw()

    def draw(self):
        '''
        Generate widgets and pack them
        '''
        self._generate_all_widgets()
        self._pack_all_widgets()

    def reset(self):
        '''
        Update all values to initiate state
        '''
        self.update_values(pokeball_left=self.init_pokeball_left,
                           attempted_catches=self.init_attempted_catches,
                           time_elapsed=self.init_time_elapsed)

    def _generate_all_widgets(self):
        '''
        Generate all needed widgets
        '''
        self.pokeball_image = self.get_image(image_name='full_pokeball')
        self.clock_image = self.get_image(image_name='clock')
        self.pokeball_image_label = tk.Label(self, image=self.pokeball_image, borderwidth=0)
        self.clock_image_label = tk.Label(self, image=self.clock_image, borderwidth=0)
        self.pokeball_text_label = tk.Label(self, bg='white', textvariable=self.pokeball_text)
        self.clock_text_label = tk.Label(self, bg='white', textvariable=self.clock_text)
        self.new_game_btn = tk.Button(self, bg='white', borderwidth=1, text='New game')
        self.restart_game_btn = tk.Button(self, bg='white', borderwidth=1, text='Restart game')

    def _pack_all_widgets(self):
        '''
        Pack all widgets on status bar
        '''
        self.pokeball_image_label.pack(side=tk.LEFT)
        self.pokeball_text_label.pack(side=tk.LEFT)
        self.clock_image_label.pack(side=tk.LEFT)
        self.clock_text_label.pack(side=tk.LEFT)
        self.new_game_btn.pack(side=tk.TOP)
        self.restart_game_btn.pack(side=tk.BOTTOM)

    def update_values(self, pokeball_left=None, attempted_catches=None, time_elapsed=None):
        '''
        The api to update values
        Note that after updating the text of label should change along with them
        '''
        if attempted_catches or attempted_catches==0:
            self.attempted_catches = attempted_catches
        if pokeball_left or pokeball_left==0:
            self.pokeball_left = pokeball_left
        if time_elapsed or time_elapsed==0:
            self.time_elapsed = time_elapsed
        self.pokeball_text.set(f'{self.attempted_catches} attemped catches\n'
                               f'{self.pokeball_left} pokeball left')
        self.clock_text.set(f'Time elapsed\n'
                            f'{self.format_time(self.time_elapsed)}')

    def get_image(self, image_name):
        """(tk.PhotoImage) Get a image file based on capability.

        If a .png doesn't work, default to the .gif image.
        """
        try:
            image = tk.PhotoImage(file='images/' + image_name + ".png")
        except tk.TclError:
            image = tk.PhotoImage(file='images/' + image_name + ".gif")
        return image

    def format_time(self, seconds):
        '''
        Return a format text to represent the given seconds
        Calculate minutes and seconds
        examples: 63 -> 1m3s
        '''
        seconds = int(seconds)
        minutes = seconds//60
        seconds = seconds%60
        return f'{minutes}m {seconds}s'


def main():
    '''
    The entry of the program
    Create a root Tk as game window
    Create a pokemon game instance and run it
    '''
    game_window = tk.Tk()
    pokemon_game = PokemonGame(master=game_window, grid_size=10, num_pokemon=15, task=TASK_TWO)
    pokemon_game.run()


if __name__ == '__main__':
    main()