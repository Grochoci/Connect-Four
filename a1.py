__author__ = "Paul Grochocinski"
__copyright__ = "Copyright (C) 2013 Paul Grochocinski"
__licence__ = "Public Domain"
__version__ = "1.0"

# Please specify the number of columns and rows you would like to have
# the board show. Also, please select what the desired WIN_LENGTH should
# be for the winner to attain. Finally, please choose the number of
# players that will be playing and their respective symbol of choice.

# The board dimensions.
WIDTH = 7
HEIGHT = 6

# The number of tokens that must be played in a row by a player in
# order to win.
WIN_LENGTH = 4

# The token symbols for the different players.
# There can be more than two players
PLAYERS = "XO"


def get_piece(board, x, y):
    '''(str, int, int) -> str

       Return the piece at position x, y on the board or the empty string
       if the space is empty.

       >>> get_piece('   XOX  XXXX                              ', 0, 2)
       ''
       >>> get_piece('   XOX  XXXX                              ', 0, 3)
       'X'
       >>> get_piece('   XOX  XXXX                              ', 0, 4)
       'O'
    '''

    # Calculate starting position for inputted x on board.
    col_pos = x * (HEIGHT - 1) + (1 * x)
    
    # Calculate exact position of selected x,y.
    piece_pos = board[col_pos + y]

    # Return whether x,y position is an empty str or an
    # occupied str by a player.
    if piece_pos == ' ':
        return ''
    elif piece_pos != ' ':
        return piece_pos


def extract_run(board, x, y, delta_x, delta_y, length):
    '''(str, int, int, int, int, int) -> str

       Return all the non-empty pieces on the board in a line of slope
       delta_y/delta_x starting from position x, y.

       >>> extract_run('     X    XO   XOO  XXOX                  ',
                       0, 5, 1, -1, 4)
       'XXXX'
       >>> extract_run('         123OXOXOX456                     ',
                       0, 2, 0, 1, HEIGHT)
       ' '
    '''

    # Set starting position for the trace calculated in the while loop.
    col_pos = x * (HEIGHT - 1) + (1 * x)
    
    # Adjust the position by adding the y value.
    extract = board[col_pos + y]

    # Set counter for while loop
    count = 1

    # Execute the slope of choice from the starting position
    # and return a str of all the strs that it encounters.
    while count < length:
        x = x + delta_x
        y = y + delta_y
        col_pos = x * (HEIGHT - 1) + (1 * x)
        new_pos = board[col_pos + y]
        extract = extract + new_pos
        count = count + 1

    return extract


def print_board(board):
    '''(str) -> None

       Display the board on the screen.

       Note the blank line before and after the the board.

       >>> print_board('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef')

       Board:
       |1|7|C|I|O|U|a|
       |2|8|D|J|P|V|b|
       |3|9|E|K|Q|W|c|
       |4|0|F|L|R|X|d|
       |5|A|G|M|S|Y|e|
       |6|B|H|N|T|Z|f|
       ---------------

    '''

    # Set counters and initial layout for while loop.
    board_pos = 0
    layout = '\n' + 'Board:\n'
    offset = 0
    
    while offset < HEIGHT:
        # Place | before each str.
        if board_pos < (HEIGHT * (WIDTH - 1)):
            layout = layout + '|' + board[board_pos]
            board_pos = board_pos + HEIGHT
            
        # Place | before and after the last str in each row.
        elif board_pos >= (HEIGHT * (WIDTH - 1)) and \
             board_pos < (HEIGHT * WIDTH - 1):
                layout = layout + '|' + board[board_pos] + '|\n'
                offset = offset + 1
                board_pos = offset
            
        # Place the final | in the bottom row as well as the
        # base of - to seal off the board.
        elif board_pos == (HEIGHT * WIDTH - 1):
            layout = layout + '|' + board[board_pos] + '|\n'
            layout = layout + '-' * (WIDTH * 2 + 1) + '\n'
            layout = layout + ''
            offset = offset + 1
        
    print(layout)


def vert_win(board):
    ''' (str) -> bool

        Return whether there is a winner on the board vertically.
        A winner is a str containing the player's piece WIN_LENGTH long.

        >>> vert_win('XXXXOO    O                              ')
        True
    '''
    
    # Check if column has a winner.
    count = WIDTH
    x = 0
    
    while count > 0:
        # Run extract_run function to create str using slope as 0.
        vert = extract_run(board, x, 0, 0, 1, HEIGHT)
        i = 0
        
        # Check if any of the players has WIN_LENGTH in a row
        # in the vert str created.
        while i < len(PLAYERS):
            token = PLAYERS[i]
            if (token * WIN_LENGTH in vert):
                return True
            else:
                i = i + 1
                
        # If no winner is found, move to the next column and check again.
        y = 0
        x = x + 1
        count = count - 1

    return False


def horiz_win(board):
    ''' (str) -> bool

        Return whether there is a winner on the board horizontally.
        A winner is a str containing the player's piece WIN_LENGTH long.

        >>> horiz_win('    OX    OX    OX     X                  ')
        True
        '''
    
    # Check if row has a winner.
    count = HEIGHT
    y = 0
    
    while count > 0:
        # Run extract_run function and create str using slope as 1.
        horiz = extract_run(board, 0, y, 1, 0, WIDTH)
        i = 0
        
        # Check if any of the players has WIN_LENGTH in a row
        # in the horiz str created.
        while i < len(PLAYERS):
            token = PLAYERS[i]
            if (token * WIN_LENGTH in horiz):
                return True
            else:
                i = i + 1
                
        # If no winner is found, move to the next row and check again.
        x = 0
        y = y + 1
        count = count - 1

    return False


def diag_win(board):
    ''' (str) -> bool

        Return whether there is a winner on the board diagonally
        from top left to bottom right.
        A winner is a str containing the player's piece WIN_LENGTH long.

        >>> diag_win('                    XOOX   XOO    XO     X')
        True
        '''

    # Check if diagonal (left to right) has a winner. 
    y = HEIGHT - 1
    x = 0
    
    while y > 0:
        # Run extract_run function and create str using slope 1/1.
        diag = extract_run(board, x, y, 1, 1, HEIGHT - y)
        i = 0
        
        # Check if any of the players has WIN_LENGTH in a row
        # in the diag str created.
        while i < len(PLAYERS):
            token = PLAYERS[i]
            if (token * WIN_LENGTH in diag):
                return True
            else:
                i = i + 1
                
        # If no winner is found, move to the next row and check the
        # diagonal again to the right.
        y = y - 1

    # Start at the top left corner.
    y = 0
    x = 0

    # Find the number of maximum squares on the diagonal present to
    # check for and ensure idx stays in range.
    while x < WIDTH:
        count_len = WIDTH - x
        if count_len > HEIGHT:
            count_len = HEIGHT
            
        # Run extract_run function and create str using slope 1/1.
        diag = extract_run(board, x, y, 1, 1, count_len)
        i = 0
        
        # Check if any of the players has WIN_LENGTH in a row
        # in the diag str created.
        while i < len(PLAYERS):
            token = PLAYERS[i]
            if (token * WIN_LENGTH in diag):
                return True
            else:
                i = i + 1
                
        # If no winner is found, move to the next column and check the
        # diagonal again to the right.
        x = x + 1


def diag1_win(board):
    ''' (str) -> bool

        Return whether there is a winner on the board diagonally
        from top right to bottom left.
        A winner is a str containing the player's piece WIN_LENGTH long.

        >>> diag_win('     X    XO   XOO  XOOX                  ')
        True
        '''

    # Check if diagonal (right to left) has a winner.
    y = HEIGHT - 1
    x = WIDTH - 1

    while y > 0:
        # Run extract_run function and create str using slope -1/1.
        diag1 = extract_run(board, x, y, -1, 1, HEIGHT - y)
        i = 0
        
        # Check if any of the players has WIN_LENGTH in a row
        # in the diag1 str created.
        while i < len(PLAYERS):
            token = PLAYERS[i]
            if (token * WIN_LENGTH in diag1):
                return True
            else:
                i = i + 1
                
        # If no winner is found, move to the next row and check the
        # diagonal again to the left.
        y = y - 1

    # Start at the top right corner.
    y = 0
    x = WIDTH - 1

    # Find the number fo maximum squares on the diagonal present to
    # check for and ensure idx stays in range.
    while x >= 0:
        count_len = x + 1
        if count_len > HEIGHT:
            count_len = HEIGHT
            
        # Run extract_run function and create str using slope -1/1.
        diag1 = extract_run(board, x, y, -1, 1, count_len)
        i = 0
        
        # Check if any of the players has WIN_LENGTH in a row
        # in the diag1 str created.
        while i < len(PLAYERS):
            token = PLAYERS[i]
            if (token * WIN_LENGTH in diag1):
                return True
            else:
                i = i + 1
                
        # If no winner is found, move to the next column and check the
        # diagonal again to the left.
        x = x - 1
        

def has_won(board):
    ''' (str) -> bool

        Return True if player has won in a row, column, or diagonal
        from their corresponding functions.

        >>> has_won(board)
        True
    '''
    
    # Call on the different checks for winner functions and check
    # whether one of them is true, indicating that there is a winner.
    if (vert_win(board) or horiz_win(board) or diag_win(board) or \
        diag1_win(board)) == True:
            return True

    return False


def insert_piece(board, column, player):
    '''(str, int, str) -> str

       Return a string representing the board if player inserts a piece
       in column of board.

       board must have free space in column.

       >>> insert_piece('XXXXXX  OOOO                              ', 1, 'X')
       'XXXXXX XOOOO                              '
    '''

    # Calculate starting position for inputted x on board.
    col_pos = column * (HEIGHT - 1) + (1 * column)

    # Counter for while loop below, as well as make y start
    # at the most bottom row
    y = HEIGHT - 1

    while y >= 0:
        # Check whether the 'y' row of the selected column
        # is empty and if it is replace the ' ' with player piece.
        if board[col_pos + y] == ' ':
            board = board[0:(col_pos + y)] + player +\
                    board[(col_pos + y + 1):]
            y = y - HEIGHT
            
        # If the row is not empty, make y, 1 square above and recheck.
        elif board[col_pos + y] != ' ':
            y = y - 1
            
    return board


def next_player(cur_player):
    '''(str) -> str

       Return the next player to make their move.

       >>> next_player('X')
       'O'
    '''

    # Number of players playing
    num_players = len(PLAYERS)

    # Find out the index of cur_player in PLAYER
    i = 0
    cur_token = 0
    while i < len(PLAYERS):
        if PLAYERS[i] == cur_player:
            cur_token = i
            i = len(PLAYERS)
        elif PLAYERS[i] != cur_player:
            i = i + 1
    
    # If the last player is the cur_player, reset the idx to
    # 0 so that the order of players starts from the start.
    if cur_player == PLAYERS[(num_players) - 1]:
        player = PLAYERS[0]
        
    # If the cur_player is not the last player, move idx forward
    # by one and make that the cur_player.
    elif cur_player != PLAYERS[(num_players) - 1]:
        player = PLAYERS[cur_token + 1]

    return  player


def get_column(board, player):
    ''' (str, str) -> int

        Print player please choose a column and return the column that
        the player has chosen.
    '''
    
    # Prompt player for column inupt
    choice = input(player + " please choose a column from 1-" +\
                   str(WIDTH) + ": ")
    
    # Alternative prompt if column is full
    alt_prompt = (player + " please choose an available column: ")
    
    # Alternative prompt if invalid input
    inv_prompt = (player + " please choose an appropriate input: ")

    # Create a str with the possible choices for columns depending
    # on how many columns the game is played with.
    count = 1
    choice_range = ''
    while count <= WIDTH:
        choice_range = choice_range + str(count)
        count = count + 1

    # Define an escape for the while loop.
    while_end = 0

    # Check if column has available space for player and is
    # an appropriate column input and if not, ask for input again.
    while while_end != 1:
        if choice == '':
            choice = input(inv_prompt)
        elif choice in choice_range:
            end_range = int(choice) * HEIGHT
            st_range = end_range - HEIGHT
            if ' ' not in board[st_range:end_range]:
                choice = input(alt_prompt)
            elif ' ' in board[st_range:end_range]:
                while_end = 1
        else:
            choice = input(inv_prompt)
            
    # -1 is adjusting for user column choice vs. python idx numbering
    # ex. user sees column 1 as 1 and idx is 0 for column 1.
    return int(choice) - 1
        

##############################################################################
##############################################################################
#############                                              ###################
#############    Do not change anything below this line    ###################
#############                                              ###################
##############################################################################
##############################################################################


def board_filled(board):
    '''(str) -> bool

       Return True iff board contains no empty spaces.

       >>> board_filled('   XOX  XXXX                              ')
       False
       >>> board_filled('ABCDEFGXXXXXABCDFGHXXXXXXXXXXXXXXXXXXXXXXX')
       True
    '''

    while board != '':
        if board[0] == ' ':
            return False

        board = board[1:]

    return True


def congratulate_winner(board, player):
    '''(str, str) -> None

       Print a congratulatory message to the player.
    '''

    print("Congratulations! " + player + " wins!")


def draw_message(board):
    '''(str) -> None

       Print a message in the event of a draw. board is ignored.

       >>> draw_message('')
       Game ended in a draw.
    '''

    print("Game ended in a draw.")


### Main program ###

board = " " * WIDTH * HEIGHT
player = PLAYERS[-1]

while not has_won(board) and not board_filled(board):
    player = next_player(player)
    print_board(board)
    column = get_column(board, player)
    board = insert_piece(board, column, player)

print_board(board)

if has_won(board):
    congratulate_winner(board, player)
else:
    draw_message(board)
