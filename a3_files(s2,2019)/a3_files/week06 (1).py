def find_functions(filename):
    """Writes the name of each function defined in a given file to functions.txt.

    Parameters:
        filename (str): Name of the file from which to extract functions.
    """

    # Open the input and output files with the appropriate modes
    fin = open(filename, 'r')
    fout = open('functions.txt', 'w')

    # Iterate over each line in the input file
    for line in fin:
        # If the current line begins with 'def ', then a function is defined
        # on this line.
        if line.startswith('def '):
            # Write the function definition to the output file.
            fout.writeline(line.rstrip())
            # Alternatively, this can also be achieved by printing to the
            # output file, like so:
            # print >> fout, line.rstrip()

    # Make sure to close the input and output files once finished.
    fin.close()
    fout.close()

    # -----------------------------------------------------------------------
    # We could alternatively write this method using with blocks, which
    # would automatically close the files for us at the end of the block.
    #
    # with open(filename, 'rU') as fin, open('functions.txt', 'w') as fout:
    #     for line in fin:
    #         if line.startswith('def '):
    #             print >> fout, line.rstrip()
    # -----------------------------------------------------------------------


def find_functions(filename):
    """Returns a list of tuples describing the functions found in 'filename'.

    Returns a list of tuples of the line on which a function was found,
    the name of the function, and the name of the function's parameters,
    in the form (line, function_name, parameters).

    Parameters:
        filename (str): Name of the file from which to extract functions.

    Return:
        list<tuple>: List of line number & function definitions found in 'filename'.
    """
    # Start with an empty list which will be used to hold the tuples.
    functions = []

    with open(filename, 'r') as fd:
        # Iterate over each line (with its line number, in the file)
        # Second argument to enumerate begins the count at 1 (since the first
        # line is line 1, not line 0)
        for line_num, line in enumerate(fd, 1):
            if line.startswith('def '):
                # Get the part of the text after 'def '
                line = line.split('def ', 1)[1]
                # There are many ways to achieve this, others include:
                # _, _, line = line.partition('def ')
                # line = line[4:]
                # etc.

                # The name of the function is the part of the line before the
                # opening parenthesis.
                name, _, line = line.partition('(')
                # Note: line is now everything after the opening parenthesis.

                # The arguments come between the opening parenthesis (which
                # is no longer included in the line) and the closing
                # parenthesis.
                args, _, _ = line.partition(')')

                # We need to convert args to a tuple. Since it is of
                # arbitrary length, we need to build a list and then convert
                # that to a tuple using the tuple method.
                args_list = []
                for arg in args.split(','):
                    args_list.append(arg.strip())

                # As an aside, if we know that each argument is separated by
                # a comma and exactly one space, we could use the following:
                # args = tuple(args.split(', '))

                # As a further aside, the above for loop can be written using
                # list comprehension (introduced later in the course). I.e.
                # args = tuple([arg.strip() for arg in arg.split(',')])

                # Append a tuple with the line number, the name of the
                # function, and its parameters (arguments) to the result.
                functions.append((line_num, name, args))

    return functions


#############################################################################


def read_config(filename):
    """Returns a dictionary representation of the configuration data.

    Configuration data is in sections, indicated by [Section Name].
    Within each section is a set of key to value maps as key=value.

    Parameters:
        filename (str): Name of the configuration file from which to extract data.

    Return:
        dict<str: dict<str: str>>: Sections are keys for dictionaries containing the section's entries.
                                   Each key-value pair within a section is a dictionary entry.
    """

    fd = open(filename, 'r')

    # Resulting configuration dictionary
    config = {}

    # Store the current heading (i.e. the last one encountered)
    heading = None

    # Iterate over each line in the file.
    for line in fd:
        # First strip the line of surrounding whitespace.
        line = line.strip()

        if line.startswith('[') and line.endswith(']'):
            # If the line is wrapped with square brackets, it is a major key.

            # The heading does not include [ or ]
            heading = line[1:-1]

            # Create a new dictionary for the settings under this heading.
            config[heading] = {}

        elif line.count('=') == 1 and heading is not None:
            # Else if this line contains equals and we've seen a heading.

            # Get the name and value from this line.
            name, value = line.split('=')

            # Set the appropriate key/value in the configuration dictionary
            # for the current heading.
            config[heading][name.strip()] = value.strip()

        else:
            # If the config file is invalid, raise a ValueError.
            raise ValueError('Invalid config file.')

    fd.close()

    return config


def get_value(config, name):
    """Returns the setting name from the configuration dictionary.

    Parameters:
        config (dict<str: dict<str: str>>): Section to Setting-Value mapping.
        name (str): Name of the setting we want to identify.

    Return:
        (str): Value of 'name's setting.
    """
    # Split the name of the setting over the fullstop.
    a, b = name.split('.')

    # Return the appropriate value.
    return config[a][b]


def main():
    ############################################################
    #                     Scrabble Scores                      #
    ############################################################
    # Load the scores from the score file
    # Note that all capitals represents a constant (i.e. the value is not
    # intended to change).
    SCORES = read_scores('scrabble_scores.txt')

    import pprint
    pprint.pprint(SCORES)

    print(get_score(SCORES, 'quack'))

    ############################################################
    #                       Config File                        #
    ############################################################
    config = read_config('config.txt')
    print(get_value(config, 'user.mobile'))
    print(get_value(config, 'notifications.email'))
