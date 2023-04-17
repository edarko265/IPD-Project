from opencv import detect_move
import sys
import time
import nedcoding

robot=nedcoding.robot
# Tic Tac Toe board
board = [' ',' ', ' ',' ',' ',' ',' ',' ',' ']

# Function to print the Tic Tac Toe board
def print_board():
    print(board[0] + '|' + board[1] + '|' + board[2])
    print('-+-+-')
    print(board[3] + '|' + board[4] + '|' + board[5])
    print('-+-+-')
    print(board[6] + '|' + board[7] + '|' + board[8])

# Function to check for empty cells
def empty_cells():
    cells = []
    for i in range(9):
        if board[i] == ' ':
            cells.append(i)
    return cells

# Function to check if the game is over
def game_over():
    # Check for horizontal wins
    for i in range(0, 9, 3):
        if board[i] == board[i+1] and board[i] == board[i+2] and board[i] != ' ':
            return board[i]
    # Check for vertical wins
    for i in range(3):
        if board[i] == board[i+3] and board[i] == board[i+6] and board[i] != ' ':
            return board[i]
    # Check for diagonal wins
    if board[0] == board[4] and board[0] == board[8] and board[0] != ' ':
        return board[0]
    elif board[2] == board[4] and board[2] == board[6] and board[2] != ' ':
        return board[2]
    # Check for tie game
    elif ' ' in board:    
        return None
    # Game is not over
    else:
        return 'Tie'

# Function for the minimax algorithm
def minimax(depth, player):
    # Check if the game is over
    result = game_over()
    if result != None:
        if result == 'O':
            return 1
        elif result == 'X':
            return -1
        else:
            return 0
    # If it's the AI's turn
    if player == 'O':
        best_score = -1000
        for cell in empty_cells():
            board[cell] = player
            score = minimax(depth+1, 'X')
            board[cell] = ' '
            best_score = max(score, best_score)
        return best_score
    # If it's the opponent's turn
    else:
        best_score = 1000
        for cell in empty_cells():
            board[cell] = player
            score = minimax(depth+1, 'O')
            board[cell] = ' '
            best_score = min(score, best_score)
        return best_score

# Function for the AI's move
def ai_move():
    best_score = -1000
    best_cell = None
    for cell in empty_cells():
        board[cell] = 'O'
        score = minimax(0, 'X')
        board[cell] = ' '
        if score > best_score:
            best_score = score
            best_cell = cell
    board[best_cell] = 'O'
    nedcoding.move_to_pick_up_pose(robot)
    nedcoding.move_to(best_cell,robot)
    
   
# Main game loop
run_count=0
while True:
    nedcoding.move_to_observation_pose(robot)   
    result = game_over()
    if result != None:
        if result == 'O':
            run_count = 100
            print_board()          
            print(result + ' wins!')
            nedcoding.play_sound(run_count, robot)
            nedcoding.trajectory(robot)
            time.sleep(2)
            sys.exit()
        else:
            run_count=10
            print_board()
            print('Tie game')
            nedcoding.play_sound(run_count, robot)
            nedcoding.trajectory(robot)
            time.sleep(2)
            sys.exit()    
    else:
        nedcoding.ring_light(run_count, robot)
        nedcoding.play_sound(run_count, robot)
        board[detect_move()] = 'X'
        if ' ' in board:          
            ai_move()
            run_count+=1
            

    print_board()
    print("Make your move")
    
   
        
