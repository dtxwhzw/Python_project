from a1_support import *


def display_game(game, grid_size) :
    '''
    This functions prints out a grid_shaped representation of the game, given the game string and the grid size as arguments.
    :param game(str): game string
    :param grid_size(int): size of game
    :print the game interface
    '''
    str_title = '  ' + WALL_VERTICAL
    str_boundary = WALL_HORIZONTAL * (grid_size + 1) * 4
    for i in range(1, grid_size + 1) :
        if i < 10 :
            str_title += ' ' + str(i) + ' ' + WALL_VERTICAL
        else :
            str_title += ' ' + str(i) + WALL_VERTICAL
    print(str_title)
    print(str_boundary)
    for i in range(grid_size) :
        str_main = ALPHA[i] + ' ' + WALL_VERTICAL
        for j in range(grid_size) :
            n = i * grid_size + j
            str_main += ' ' + game[n] + ' ' + WALL_VERTICAL
        print(str_main)
        print(str_boundary)


def parse_position(action, grid_size) :
    '''
    This function checks if the input action is in a valid format. if the action is valid then return the location
    represented by the action. If the action if invalid then return nothing.
    :param action(str): action command
    :param grid_size(int): size of the game
    :return(tuple<int,int>): return a tuple which represents the location in the game
    '''
    alpha = ALPHA[:grid_size]
    if action == "" :
        return None
    elif action[0] == ' ' :
        return None
    elif action[0] == 'f' :
        if action[2] in alpha :
            if int(action[3 :]) <= grid_size :
                return alpha.index(action[2]), int(action[3 :]) - 1
    elif action[0] in alpha :
        if len(action) == 1 :
            return None
        elif action[1].isalpha() :
            return None
        elif int(action[1 :]) <= grid_size :
            return alpha.index(action[0]), int(action[1 :]) - 1
    else :
        return None


def position_to_index(position, grid_size) :
    '''
    This function should convert the row, column coordinate in the grid to the game strings index. The function returns
    an integer representing the index of the cell in the game string.
    :param position (tuple<int,int>): the location in the game interface
    :param grid_size (int): size of game
    :return(int): the index of the cell in the game string.
    '''
    x, y = position
    index = x * grid_size + y
    return index


def replace_character_at_index(game, index, character) :
    '''
    This function returns an updated game string with the specified character placed at the specified index.
    :param game(str): the game string
    :param index(int): the index in the game string
    :param character(str): the new icon
    :return(str): return a new game string
    '''
    new_game = game[:index] + character + game[index + 1 :]
    return new_game


def flag_cell(game, index) :
    '''
    This function returns an updated game string after "toggling" the flag at the specified index in the game string.
    :param game (str): the game string
    :param index (int): the index in the game string
    :return (str): return a new game string.
    '''
    if game[index] != FLAG :
        new_game = game[:index] + FLAG + game[index + 1 :]
    else :
        new_game = game[:index] + '~' + game[index + 1 :]
    return new_game


def index_in_direction(index, grid_size, direction) :
    '''
    This function takes in the index to a cell in the game string and returns a new index corresponding to an adjacent
    cell in the specified direction. Return None for invalid directions.
    :param index(int): the index in the game string
    :param grid_size(int): size of the gamne
    :param direction(str): the direction of the cell the valid directions are in the DIRECTIONS
    :return(int): returns the index of the cells in the valid directions
    '''
    if direction == UP :
        if index // grid_size == 0 :
            return None
        else :
            return index - grid_size
    elif direction == DOWN :
        if index // grid_size == grid_size - 1 :
            return None
        else :
            return index + grid_size
    elif direction == LEFT :
        if index % grid_size == 0 :
            return None
        else :
            return index - 1
    elif direction == RIGHT :
        if index % grid_size == grid_size - 1 :
            return None
        else :
            return index + 1
    elif direction == f"{UP}-{LEFT}" :
        if index // grid_size == 0 or index % grid_size == 0 :
            return None
        else :
            return int(index - grid_size - 1)
    elif direction == f"{UP}-{RIGHT}" :
        if index // grid_size == 0 or index % grid_size == grid_size - 1 :
            return None
        else :
            return index - grid_size + 1
    elif direction == f"{DOWN}-{LEFT}" :
        if index // grid_size == grid_size - 1 or index % grid_size == 0 :
            return None
        else :
            return index + grid_size - 1
    elif direction == f"{DOWN}-{RIGHT}" :
        if index // grid_size == grid_size - 1 or index % grid_size == grid_size - 1 :
            return None
        else :
            return index + grid_size + 1


def neighbour_directions(index, grid_size) :
    '''
    This function returns a list of indexes of indexes that have a neighbouring cell. create a new list which contains
    all the possible index, and remove the None.
    :param index(int): the index in the game string
    :param grid_size(int): size of the game
    :return: return a list contain the valid neighbor index.
    '''
    list_neighbour_temp = [index_in_direction(index, grid_size, UP),
                           index_in_direction(index, grid_size, DOWN),
                           index_in_direction(index, grid_size, RIGHT),
                           index_in_direction(index, grid_size, LEFT),
                           index_in_direction(index, grid_size, f"{UP}-{LEFT}"),
                           index_in_direction(index, grid_size, f"{UP}-{RIGHT}"),
                           index_in_direction(index, grid_size, f"{DOWN}-{LEFT}"),
                           index_in_direction(index, grid_size, f"{DOWN}-{RIGHT}")]
    list_neighbour = [x for x in list_neighbour_temp if x is not None]
    return list_neighbour


def number_at_cell(game, pokemon_locations, grid_size, index) :
    '''
    This function returns the number of Pokemon in neighbouring cells.
    :param game(str): game string.
    :param pokemon_locations(tuple<int>): A tuple containing  indexes where the pokemons are created for the game string.
    :param grid_size(int): the size of the game
    :param index(int): the index in the game string
    :return(int): returns the number of Pokemon in neighbouring cells.
    '''
    num = 0
    neighbour = neighbour_directions(index, grid_size)
    for i in neighbour :
        if i in pokemon_locations :
            num += 1
    return num


def check_win(game, pokemon_location) :
    '''
    This function returns True if the player has won the game and return False otherwise.
    :param game(str): the game string.
    :param pokemon_location(tuple<int>): A tuple containing  indexes where the pokemons are created for the game string.
    :return: return True or False.
    '''
    number_of_pokemon = len(pokemon_location)
    num = 0
    for i in range(number_of_pokemon) :
        if game[pokemon_location[i]] != FLAG :
            return False
    for i in range(len(game)) :
        if game[i] == FLAG :
            num += 1
    if num == number_of_pokemon and '~' not in game :
        return True
    else :
        return False


def main():
    '''
    This function handles player interaction. At the begining, the player should be promoted to set the size of the game
    and the number of the pokemons. And the the pokemon location are initialized and so does the game string. And then
    the game interface should be displayed.
    If the check_win function doesn't return True, the player shoulded be promoted to enter the action.
    The game will finish if all the pokemons are flaged or the player decide to quit or the player hit the pokemon.
    :return:
    '''
    global index
    grid_size = int(input('Please input the size of the grid: '))
    number_of_pokemons = int(input("Please input the number of pokemons: "))
    pokemon_location = generate_pokemons(grid_size, number_of_pokemons)
    game = '~' * grid_size * grid_size
    display_game(game, grid_size)
    while check_win(game, pokemon_location) is not True :
        action = input("\nPlease input action: ")
        position = parse_position(action, grid_size)
        if action == ':)':
            print("It's rewind time.")
            game = '~' * grid_size * grid_size
            pokemon_location = generate_pokemons(grid_size, number_of_pokemons)
            display_game(game,grid_size)
        elif action == 'h':
            print(HELP_TEXT)
            display_game(game, grid_size)
            continue
        elif action == 'q' :
            decision = input("You sure about that buddy? (y/n): ")
            if decision == 'n' :
                print("Let's keep going.")
                display_game(game, grid_size)
                continue
            elif decision == 'y' :
                print("Catch you on the flip side.")
                break
            else :
                print("That ain't a valid action buddy.")
                display_game(game, grid_size)
        else:
            if position is None :
                print("That ain't a valid action buddy.")
                display_game(game, grid_size)
                continue
            else :
                index = position_to_index(position, grid_size)
            if action[0] == 'f':
                if game[index] == FLAG :
                    game = replace_character_at_index(game, index, '~')
                else :
                    game = replace_character_at_index(game, index, FLAG)
                display_game(game, grid_size)
                continue
            if index in pokemon_location :
                if game[index] == FLAG :
                    display_game(game, grid_size)
                    continue
                for i in pokemon_location :
                    game = replace_character_at_index(game, i, POKEMON)
                display_game(game, grid_size)
                print("You have scared away all the pokemons.")
                break
            else:
                number_location = big_fun_search(game,grid_size,pokemon_location,index)
                number_location.append(index)
                for i in number_location:
                    if game[i] == FLAG:
                        continue
                    else:
                        game = game[:i] + str(number_at_cell(game,pokemon_location,grid_size,i)) + game[i+1:]
                display_game(game,grid_size)
    if check_win(game,pokemon_location):
        print("You win.")


def big_fun_search(game, grid_size, pokemon_locations, index) :
    """Searching adjacent cells to see if there are any Pokemon"s present.

	Using some sick algorithms.

	Find all cells which should be revealed when a cell is selected.

	For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
	neighbours are revealed. If one of the neighbouring cells is also zero then
	all of that cell"s neighbours are also revealed. This repeats until no
	zero value neighbours exist.

	For cells which have a non-zero value (i.e. cells with neightbour pokemons), only
	the cell itself is revealed.

	Parameters:
		game (str): Game string.
		grid_size (int): Size of game.
		pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
		index (int): Index of the currently selected cell

	Returns:
		(list<int>): List of cells to turn visible.
	"""
    queue = [index]
    discovered = [index]
    visible = []

    if game[index] == FLAG :
        return queue

    number = number_at_cell(game, pokemon_locations, grid_size, index)
    if number != 0 :
        return queue

    while queue :
        node = queue.pop()
        for neighbour in neighbour_directions(node, grid_size) :
            if neighbour in discovered or neighbour is None :
                continue

            discovered.append(neighbour)
            if game[neighbour] != FLAG :
                number = number_at_cell(game, pokemon_locations, grid_size, neighbour)
                if number == 0 :
                    queue.append(neighbour)
            visible.append(neighbour)
    return visible


if __name__ == "__main__" :
    main()
