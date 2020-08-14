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


### add code here ###
class Tile :
    """

    """
    def __init__(self, name, selectable=True) :
        '''

        :param name:
        :param selectable:
        '''
        self.name = name
        self.id = 'tile'
        self.select = selectable

    def get_name(self) :
        '''

        :return:
        '''
        return self.name

    def get_id(self) :
        '''

        :return:
        '''
        return self.id

    def set_select(self, select):
        '''

        :param select:
        :return:
        '''
        self.select = select

    def can_select(self) :
        '''

        :return:
        '''
        return self.select

    def __str__(self) :
        return f"Tile('{self.name}', {self.select})"

    def __repr__(self) :
        return f"Tile('{self.name}', {self.select})"


class Pipe(Tile) :
    '''

    '''
    def __init__(self, name, orientation: int = 0, selectable=True) :
        '''

        :param name:
        :param orientation:
        :param selectable:
        '''
        self.name = name
        self.id = 'pipe'
        self.orientation = orientation
        self.select = selectable

    def get_connected(self, side) :
        '''

        :param side:
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
            dir1 = ['N', 'S']
            dir2 = ['W', 'E']
            if side in dir1 :
                dir1.remove(side)
                return dir1
            elif side in dir2 :
                dir2.remove(side)
                return dir2

    def rotate(self, direction) :
        '''

        :param direction:
        :return:
        '''
        position = self.orientation + direction
        self.orientation = position % 4

    def get_orientation(self) :
        '''

        :return:
        '''
        return self.orientation

    def __str__(self) :
        return f"Pipe('{self.name}', {self.orientation})"

    def __repr__(self) :
        return f"Pipe('{self.name}', {self.orientation})"


class SpecialPipe(Pipe) :
    '''

    '''
    def __init__(self, name, orientation: int = 0, selectable=False) :
        '''

        :param name:
        :param orientation:
        :param selectable:
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

    '''
    def __init__(self, orientation = 0,selectable=False):
        '''

        :param orientation:
        '''
        self.name = 'start'
        self.id = 'special_pipe'
        self.orientation = orientation
        self.select = selectable

    def get_connected(self, side=None) :
        '''

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

    '''
    def __init__(self, orientation = 0, selectable=False):
        '''

        :param orientation:
        '''
        self.name = 'end'
        self.id = 'special_pipe'
        self.orientation = orientation
        self.select = selectable

    def get_connected(self, side=None) :
        '''

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
        """
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self.board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
                              Tile('tile', True), Tile('tile', True)],
                             [StartPipe(1), Tile('tile', True), Tile('tile', True), \
                              Tile('tile', True), Tile('tile', True), Tile('tile', True)],
                             [Tile('tile', True), Tile('tile', True), \
                              Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)],
                             [Tile('tile', True), \
                              Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False),
                              Tile('tile', True)], \
                             [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True),
                              EndPipe(3), \
                              Tile('tile', True)],
                             [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
                              Tile('tile', True), Tile('tile', True)]]

        self.playable_pipes = {'straight' : 1, 'corner' : 1, 'cross' : 1, 'junction-t' : 1, 'diagonals' : 1,
                               'over-under' : 1}
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self.start = (0, 0)
        self.end = (0, 0)
        self.end_pipe_positions()
        ### add code here ###

    def get_board_layout(self) :
        '''

        :return:
        '''
        return self.board_layout

    def get_playable_pipes(self) :
        '''

        :return:
        '''
        return self.playable_pipes

    def change_playable_amount(self, pipe_name: str, number: int) :
        '''

        :param pipe_name:
        :param number:
        :return:
        '''
        num = self.playable_pipes[pipe_name]
        self.playable_pipes[pipe_name] = num + number

    def get_pipe(self, position) :
        '''

        :param position:
        :return:
        '''
        x, y = position
        return self.board_layout[x][y]

    def set_pipe(self, pipe: Pipe, position) :
        '''

        :param pipe:
        :param position:
        :return:
        '''
        x, y = position
        self.board_layout[x][y] = pipe
        self.playable_pipes[pipe.get_name()] -= 1

    def pipe_in_position(self, position) :
        '''

        :param position:
        :return:
        '''
        x, y = position
        if self.board_layout[x][y].get_name() == 'tile' or self.board_layout[x][y] .get_name()== 'locked' or self.board_layout[x][y] is None :
            return None
        else :
            return self.board_layout[x][y]

    def remove_pipe(self, position) :
        '''

        :param position:
        :return:
        '''
        x, y = position
        self.playable_pipes[self.board_layout[x][y].get_name()] += 1
        self.board_layout[x][y] = Tile('tile')

    def position_in_direction(self, direction, position) :
        '''

        :param direction:
        :param position:
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

        :return:
        '''
        return self.start

    def get_ending_position(self) :
        '''

        :return:
        '''
        return self.end

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
