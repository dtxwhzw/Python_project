EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

SPECIAL_TILES = {
    "S" : START_PIPE,
    "E" : END_PIPE,
    "L" : LOCKED_TILE
}

PIPES = {
    "ST" : "straight",
    "CO" : "corner",
    "CR" : "cross",
    "JT" : "junction-t",
    "DI" : "diagonals",
    "OU" : "over-under"
}


class Tile :
    """
    implement the tile class, tile is a an avaliable space in the game board, it has name, id , and can be selectable or
    not and locked or not.
    """
    def __init__(self, name, selectable=True) :
        '''

        :param name: tile's name
        :param isselectable: whether this tile is selectable and it has been set to be selectable default.
        '''
        self.name = name
        self.id = 'tile'
        self.select = selectable

    def get_name(self) :
        '''
        return the tile's name
        :return:
        '''
        return self.name

    def get_id(self) :
        '''
        return the tile's id which is string 'tile'
        :return:
        '''
        return self.id

    def set_select(self, select):
        '''
        change the tile's selectable attribute
        :param select:
        :return:
        '''
        self.select = select

    def can_select(self) :
        '''
        return the tile's selectable attribute
        :return:
        '''
        return self.select

    def __str__(self) :
        return f"Tile('{self.name}', {self.select})"

    def __repr__(self) :
        return f"Tile('{self.name}', {self.select})"


class Pipe(Tile) :
    '''
    Pipe class represent a pipe in the game, it is a subclass of Tile. This class can be connected to other pipe in the
    game board.
    '''
    def __init__(self, name, orientation: int = 0, selectable=True) :
        '''

        :param name: Pipe's name, there are 6 kinds of pipes.
        :param orientation: Pipe's orientation, which could be 0,1,2,3.
        :param selectable: Pipe's selectable attribute and it must be True.
        '''
        self.name = name
        self.id = 'pipe'
        self.orientation = orientation
        self.select = selectable

    def get_connected(self, side) :
        '''
        this instance help to find out which direction are connected with each other. Because there are 6 kinds of pipes,
        so we need to consider 6 conditions.
        if pipe is straight:
            north and south or east and west are connected,if the orientation isn't in one of this set, it will return
            None.
        if pipe is corner the situation is same as staright, two directions are connected to each other.
        if pipe is cross, the four directions are connected.
        if pipe is junction-t, if the side are not in the connection set, it will return none, otherwise it will return
        the other two directions
        if pipe is diagonal the situation is quite like the straight and corner, but it only has two conditions so it will
        become much simple.
        if pipe is over-under, in this situation the north and south are connected and east and west are connect, so i
        set two conditions, find out which set has side, and return another one.
        :param side: the input side from former pipe.
        :return:
        '''
        if self.name == 'straight' :
            if self.orientation == 0 or self.orientation == 2 :
                if side == 'N' :
                    return ['S']
                elif side == 'S' :
                    return ['N']
                else :
                    return []
            elif self.orientation == 1 or self.orientation == 3 :
                if side == 'W' :
                    return ['E']
                elif side == 'E' :
                    return ['W']
                else :
                    return []
        elif self.name == 'corner' :
            if self.orientation == 0 :
                if side == 'N' :
                    return ['E']
                elif side == 'E' :
                    return ['N']
                else :
                    return []
            elif self.orientation == 1 :
                if side == 'E' :
                    return ['S']
                elif side == 'S' :
                    return ['E']
                else :
                    return []
            elif self.orientation == 2 :
                if side == 'S' :
                    return ['W']
                elif side == 'W' :
                    return ['S']
                else :
                    return []
            else :
                if side == 'W' :
                    return ['N']
                elif side == 'N' :
                    return ['W']
                else :
                    return []
        elif self.name == 'cross' :
            direction = ['N', 'E', 'S', 'W']
            direction.remove(side)
            return direction
        elif self.name == 'junction-t' :
            direction = ['N', 'E', 'S', 'W']
            if side == direction[self.orientation] :
                return []
            else :
                direction.remove(direction[self.orientation])
                direction.remove(side)
                return direction
        elif self.name == 'diagonals' :
            if self.orientation % 2 == 0 :
                if side == 'N' :
                    return ['E']
                elif side == 'E' :
                    return ['N']
                elif side == 'S' :
                    return ['W']
                else :
                    return ['S']
            elif self.orientation % 2 == 1 :
                if side == 'N' :
                    return ['W']
                elif side == 'W' :
                    return ['N']
                elif side == 'S' :
                    return ['E']
                elif side == 'E' :
                    return ['S']
        elif self.name == 'over-under' :
            direction_NS = ['N', 'S']
            direction_WS = ['W', 'E']
            if side in direction_NS :
                direction_NS.remove(side)
                return direction_NS
            elif side in direction_WS :
                direction_WS.remove(side)
                return direction_WS

    def rotate(self, direction) :
        '''
        change the pipe's orientation
        :param direction: this defines how much would the orientation changed.
        :return:
        '''
        position = self.orientation + direction
        self.orientation = position % 4

    def get_orientation(self) :
        '''
        get the pipe's orientation
        :return:
        '''
        return self.orientation

    def __str__(self) :
        return f"Pipe('{self.name}', {self.orientation})"

    def __repr__(self) :
        return f"Pipe('{self.name}', {self.orientation})"


class SpecialPipe(Pipe) :
    '''
    this is the special pipe class, it is a subclass of pipe, and only startpipe and endpipe are special pipe.
    '''
    def __init__(self, name, orientation: int = 0, selectable=False) :
        '''

        :param name: pipe's name
        :param orientation: pipe's orientation
        :param selectable: pipe's selectable, and the special pipes can not be selected.
        '''
        self.id = 'special_pipe'
        self.orientation = orientation
        self.name = name
        self.select = selectable

    def __str__(self) :
        return f"SpecialPipe({self.orientation})"

    def __repr__(self) :
        return f"SpecialPipe({self.orientation})"


class StartPipe(SpecialPipe) :
    '''
    this is the start pipe class, which indicate the start positon of the game.
    '''
    def __init__(self, orientation = 0,selectable=False):
        '''

        :param orientation: pipe's orientation
        :param selectable: pipe's selectable
        and this class' name is start
        '''
        self.name = 'start'
        self.id = 'special_pipe'
        self.orientation = orientation
        self.select = selectable

    def get_connected(self, side=None) :
        '''
        find the connected direction of the start pipe,0 refer to north, 1 refer to east, 2 refer to south, and 3 refer
        to west.
        :param side:
        :return:
        '''
        if self.orientation == 0 :
            return ['N']
        elif self.orientation == 1 :
            return ['E']
        elif self.orientation == 2 :
            return ['S']
        else :
            return ['W']

    def __str__(self) :
        return f"StartPipe({self.orientation})"

    def __repr__(self) :
        return f"StartPipe({self.orientation})"


class EndPipe(SpecialPipe) :
    '''
    the end pipe class which is the destination of the game.
    '''
    def __init__(self, orientation = 0, selectable=False):
        '''

        :param orientation: pipe's orientation
        :param selectable:  pipe's selectable attribute
        and this class' name is end.
        '''
        self.name = 'end'
        self.id = 'special_pipe'
        self.orientation = orientation
        self.select = selectable

    def get_connected(self, side=None) :
        '''
        get the side of the former pipe which end points to. This is opposite with the start pipe. 0 refer to south, 1
        refer to west, 2 refer to north, 3 refer to east.
        :param side:
        :return:
        '''
        if self.orientation == 0 :
            return ['S']
        elif self.orientation == 1 :
            return ['W']
        elif self.orientation == 2 :
            return ['N']
        else :
            return ['E']

    def __str__(self) :
        return f"EndPipe({self.orientation})"

    def __repr__(self) :
        return f"EndPipe({self.orientation})"


class PipeGame :
    """
    A game of Pipes.
    """

    def __init__(self, game_file='game_1.csv') :
        """
        Construct a game of Pipes from a file name.

        Parameters:
            game_file (str): name of the game file.
            playable_pipes (dict): the pipe in the choose list.
            board_layout (list): the playing board.
            start tuple <int,int>: the start position.
            end tuple <int,int>: the end position.
        """
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        # self.board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        #                       Tile('tile', True), Tile('tile', True)],
        #                      [StartPipe(1), Tile('tile', True), Tile('tile', True), \
        #                       Tile('tile', True), Tile('tile', True), Tile('tile', True)],
        #                      [Tile('tile', True), Tile('tile', True), \
        #                       Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)],
        #                      [Tile('tile', True), \
        #                       Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False),
        #                       Tile('tile', True)], \
        #                      [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True),
        #                       EndPipe(3), \
        #                       Tile('tile', True)],
        #                      [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        #                       Tile('tile', True), Tile('tile', True)]]
        #
        # self.playable_pipes = {'straight' : 1, 'corner' : 1, 'cross' : 1, 'junction-t' : 1, 'diagonals' : 1,
        #                        'over-under' : 1}
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self.filename = game_file
        self.playable_pipes = self.load_file(self.filename)[0]
        self.board_layout = self.load_file(self.filename)[1]
        self.start = (0, 0)
        self.end = (0, 0)
        self.end_pipe_positions()

    def get_board_layout(self) :
        '''
        return list the board_layout
        :return:
        '''
        return self.board_layout

    def get_playable_pipes(self) :
        '''
        return the dictionary of playable pipes.
        :return:
        '''
        return self.playable_pipes

    def change_playable_amount(self, pipe_name: str, number: int) :
        '''
        change the palyable pipes' amount, after a pipe has been used.
        :param pipe_name (str) : the pipe's name
        :param number (int): the number of used pipes
        :return:
        '''
        num = self.playable_pipes[pipe_name]
        self.playable_pipes[pipe_name] = num + number

    def get_pipe(self, position) :
        '''
        return the pipe in the give position
        :param position tuple <int,int>: the position of the pipe.
        :return:
        '''
        x, y = position
        return self.board_layout[x][y]

    def set_pipe(self, pipe: Pipe, position) :
        '''
        put the pipe in the given position. And the number of pipes would need changed.
        :param pipe: the pipe which will set in the given position.
        :param position: the given position.
        :return:
        '''
        x, y = position
        self.board_layout[x][y] = pipe
        self.playable_pipes[pipe.get_name()] -= 1

    def pipe_in_position(self, position) :
        '''
        return the pipe in the given position. if it is a tile in the given position, this instance will return None.
        :param position:the given position.
        :return:
        '''
        x, y = position
        if self.board_layout[x][y].get_name() == 'tile' or self.board_layout[x][y] .get_name()== 'locked' or self.board_layout[x][y] is None :
            return None
        else :
            return self.board_layout[x][y]

    def remove_pipe(self, position) :
        '''
        remove the pipe in the given position
        :param position: the given position
        :return:
        '''
        x, y = position
        self.playable_pipes[self.board_layout[x][y].get_name()] += 1
        self.board_layout[x][y] = Tile('tile')

    def position_in_direction(self, direction, position) :
        '''
        find the position after moved in the given direction. If the position after moving in out range, it will return
        None.
        :param direction: The moving direction.
        :param position: The given position.
        :return:
        '''
        x_max = len(self.board_layout)
        y_max = len(self.board_layout[0])
        x, y = position
        direction_new = ''
        if direction == 'W' :
            y -= 1
            direction_new = 'E'
        elif direction == 'E' :
            y += 1
            direction_new = 'W'
        elif direction == 'N' :
            x -= 1
            direction_new = 'S'
        elif direction == 'S' :
            x += 1
            direction_new = 'N'
        if x < 0 or x > x_max - 1 or y < 0 or y > y_max - 1 :
            return None
        else :
            return direction_new, (x, y)

    def end_pipe_positions(self) :
        '''
        This function use to find the start pipe and end pipe's position.
        :return:
        '''
        x_max = len(self.board_layout)
        y_max = len(self.board_layout[0])
        for i in range(x_max) :
            for j in range(y_max) :
                if isinstance(self.board_layout[i][j], StartPipe) :
                    self.start = (i, j)
                if isinstance(self.board_layout[i][j], EndPipe) :
                    self.end = (i, j)

    def get_starting_position(self) :
        '''
        return the start position.
        :return:
        '''
        return self.start

    def get_ending_position(self) :
        '''
        return the end position.
        :return:
        '''
        return self.end

    def load_file(self,filename: str):
        '''
        Load the game file, and chang it into the game form. use the open instance to load the file, and use the strip()
        and split to remove the '\n' and ',', and change it into list type. And use two for loop to change each character
        into their corresponding tile or pipe. And combine them together to build the board_layout list. And the last list
        refer to the number of playable pipes. Set the number to the corresponding name and build the playable pipes dict.
        And return them.
        :param filename:
        :return:
        '''
        board_layout = []
        playable_pipes = {}
        file = open(filename)
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip().split(',')
        row = len(lines) - 1
        col = len(lines[0])
        for i in range(row) :
            for j in range(col) :
                if lines[i][j] == '#':
                    lines[i][j] = Tile('tile')
                elif lines[i][j] == 'L':
                    lines[i][j] = Tile('locked',False)
                elif lines[i][j].startswith('E'):
                    if len(lines[i][j]) == 1 :
                        lines[i][j] = EndPipe()
                    else :
                        direct = lines[i][j][1]
                        lines[i][j] = EndPipe(direct)
                elif lines[i][j] == 'JT' :
                    lines[i][j] = Pipe('junction-t')
                elif lines[i][j].startswith('S') :
                    direct = int(lines[i][j][1])
                    lines[i][j] = StartPipe(direct)
                elif lines[i][j] == 'S' :
                    lines[i][j] = StartPipe()
        board_layout = lines[:row]
        playable_pipes['straight'] = int(lines[-1][0])
        playable_pipes['corner'] = int(lines[-1][1])
        playable_pipes['cross'] = int(lines[-1][2])
        playable_pipes['junction-t'] = int(lines[-1][3])
        playable_pipes['diagonals'] = int(lines[-1][4])
        playable_pipes['over-under'] = int(lines[-1][5])
        return playable_pipes, board_layout

    # #########################UNCOMMENT THIS FUNCTION WHEN READY#######################
    def check_win(self) :
        """
        (bool) Returns True  if the player has won the game False otherwise.
        """
        position = self.get_starting_position()
        pipe = self.pipe_in_position(position)
        queue = [(pipe, None, position)]
        discovered = [(pipe, None)]
        while queue :
            pipe, direction, position = queue.pop()
            for direction in pipe.get_connected(direction) :

                if self.position_in_direction(direction, position) is None :
                    new_direction = None
                    new_position = None
                else :
                    new_direction, new_position = self.position_in_direction(direction, position)
                if new_position == self.get_ending_position() and direction == self.pipe_in_position(
                        new_position).get_connected()[0] :
                    return True

                pipe = self.pipe_in_position(new_position)
                if pipe is None or (pipe, new_direction) in discovered :
                    continue
                discovered.append((pipe, new_direction))
                queue.append((pipe, new_direction, new_position))
        return False
    # #########################UNCOMMENT THIS FUNCTION WHEN READY#######################


def main() :
    print("Please run gui.py instead")


if __name__ == "__main__" :
    main()
