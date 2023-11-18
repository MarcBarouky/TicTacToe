#Jamal Lahad 212138
#Marc Barouky 210426
#Lynn Mardini 210746

import sys
import numpy as np
import pygame
import copy
import random

# Window Properties
Window_Width = 600
Window_Height = 600
Window_Text_Height=120
Background_Color = ("#113537")

# Grid Properties
Nb_Rows = 3
Nb_Columns = 3
Box_Size = Window_Width // Nb_Columns 

Line_Color = ("#FFEAD0")
Margin = 50
Grid_Line = 12

# Cross Properties
Cross_Color = ("#778DA9")
Cross_Line = 17

# Circle Properties
Circle_Size = Box_Size // 4
Circle_Color = ("#BA2D0B")
Circle_Line = 15

# Font Properties
Font_Color = ("#FFEAD0")
Font_Size = int(Window_Width*15/600)
Big_Font_Size = Font_Size+30
Font = "Silom"

#=====================================================================#

# Pygame initialisation
pygame.init()
game_window = pygame.display.set_mode((Window_Width,Window_Height+Window_Text_Height))

#Text initialization
smallfont = pygame.font.SysFont(Font, Font_Size) 
bigfont = pygame.font.SysFont(Font, Big_Font_Size) 

welcome_text1 = bigfont.render("WELCOME", True , Font_Color)
welcome_text2 = bigfont.render("TO TIC TAC TOE" , True , Font_Color)
start_text = smallfont.render('PRESS A KEY TO CHOOSE YOUR OPPONENT' , True , Font_Color)
diff1_text = smallfont.render('1: Random (Easy)|' , True , Font_Color)
diff2_text = smallfont.render('2: DLS (Medium)|' , True , Font_Color)
diff3_text = smallfont.render('3: Alpha-Beta (Hard)|' , True , Font_Color)
diff4_text = smallfont.render('4: Minimax (Hard)' , True , Font_Color)

restart_text = smallfont.render('Press r key to restart' , True , Font_Color)

pygame.display.set_caption("Tic Tac Toe")
class WelcomePage:
    def __init__(self):
        game_window.fill(Background_Color)

        welcome_text1_rect = welcome_text1.get_rect()
        welcome_text1_rect.center=(Window_Width/2, Window_Height/2) 
        game_window.blit(welcome_text1, (welcome_text1_rect))

        welcome_text2_rect = welcome_text2.get_rect()
        welcome_text2_rect.center=(Window_Width/2, Window_Height/2+Big_Font_Size) 
        game_window.blit(welcome_text2, (welcome_text2_rect))

        start_text_rect = start_text.get_rect()
        start_text_rect.center=(Window_Width/2, Window_Height+Window_Text_Height/4) 
        game_window.blit(start_text, (start_text_rect))

        diff1_text_rect = diff1_text.get_rect()
        diff1_text_rect.center=(Window_Width/4-75, Window_Height+2*Window_Text_Height/4 + 10) 
        game_window.blit(diff1_text, (diff1_text_rect))

        diff2_text_rect = diff2_text.get_rect()
        diff2_text_rect.center=(2*Window_Width/4-85, Window_Height+2*Window_Text_Height/4 + 10) 
        game_window.blit(diff2_text, (diff2_text_rect))

        diff3_text_rect = diff3_text.get_rect()
        diff3_text_rect.center=(3*Window_Width/4-82, Window_Height+2*Window_Text_Height/4 + 10) 
        game_window.blit(diff3_text, (diff3_text_rect))

        diff4_text_rect = diff4_text.get_rect()
        diff4_text_rect.center=(Window_Width-75, Window_Height+2*Window_Text_Height/4 + 10) 
        game_window.blit(diff4_text, (diff4_text_rect))

# Game Definition
class Game :
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 #For human to start and 2 for AI to start
        self.running = True 

    def Make_Move(self, row, col):
        self.board.Fill_Box(row, col, self.player)
        self.Draw_Move(row, col)
        self.Next_Turn()

    def Show_Lines(self) :
        game_window.fill( Background_Color)
        # Vertical
        pygame.draw.line(game_window, Line_Color, (Box_Size, 0), (Box_Size, Window_Height), Grid_Line)
        pygame.draw.line(game_window, Line_Color, (Window_Width - Box_Size, 0), (Window_Width - Box_Size, Window_Height), Grid_Line)
        # Horizontal
        pygame.draw.line(game_window, Line_Color, (0, Box_Size), (Window_Width, Box_Size), Grid_Line)
        pygame.draw.line(game_window, Line_Color, (0, Window_Height - Box_Size), (Window_Width, Window_Height - Box_Size), Grid_Line)

    # Show restart option
    def Show_Restart(self):
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.center=(Window_Width/2, Window_Height+Window_Text_Height/2) 
        game_window.blit(restart_text, (restart_text_rect))

    # Mark the chosen_move
    def Draw_Move(self, row, col) :
        if self.player == 1 :
            # Drawing X
            x_down_0 = (col * Box_Size + Margin, row * Box_Size + Margin)
            x_down_1 = (col * Box_Size + Box_Size - Margin, row * Box_Size + Box_Size - Margin)
            pygame.draw.line(game_window, Cross_Color, x_down_0, x_down_1, Cross_Line)
            x_up_0 = (col * Box_Size+ Margin, row * Box_Size + Box_Size - Margin)
            x_up_1 = (col * Box_Size + Box_Size - Margin, row * Box_Size +  Margin)
            pygame.draw.line(game_window, Cross_Color, x_up_0, x_up_1, Cross_Line)

        elif self.player == 2 :
            # Drawing O
            center = (col * Box_Size + Box_Size //2, row* Box_Size + Box_Size // 2)
            pygame.draw.circle(game_window, Circle_Color, center, Circle_Size, Circle_Line)

    def Next_Turn(self) :
        self.player = (self.player%2) + 1

    def Game_Over(self):
        #the game is over if we reached a final state or if the board is full
        return self.board.Final_State(show=True) != 0 or self.board.Board_Full()
    
    # Reinitialize the game to default
    def restart(self):
        self.__init__() 

# Board Definition
class Board:
    def __init__(self):
        self.boxes = np.zeros((Nb_Rows, Nb_Columns))
        self.marked_boxes = 0

    def Final_State(self, show=False):
        # 0 => not final state
        # 1 => player 1 wins
        # 2 => player 2 wins
        
        # Win vertically 
        for col in range(Nb_Columns):
            if self.boxes[0][col] == self.boxes[1][col] == self.boxes[2][col] != 0:
                if show:
                    color = Circle_Color if self.boxes[0][col] == 2 else Cross_Color
                    x = (col * Box_Size + Box_Size //2, 20)
                    y = (col * Box_Size + Box_Size //2, Window_Height - 20)
                    pygame.draw.line(game_window, color, x, y, Grid_Line)
                return self.boxes[0][col]
            
        # Win horizontally
        for row in range(Nb_Rows):
            if self.boxes[row][0] == self.boxes[row][1] == self.boxes[row][2] != 0:
                if show:
                    color = Circle_Color if self.boxes[row][0] == 2 else Cross_Color
                    x = (20, row * Box_Size + Box_Size //2 )
                    y = (Window_Width -20,row * Box_Size + Box_Size //2)
                    pygame.draw.line(game_window, color, x, y, Grid_Line)
                return self.boxes[row][0]
            
        # Win diagonally
        if self.boxes[0][0] == self.boxes[1][1] == self.boxes[2][2] != 0:
            if show:
                color = Circle_Color if self.boxes[1][1] == 2 else Cross_Color
                x = (20, 20)
                y = (Window_Width -20,Window_Height - 20)
                pygame.draw.line(game_window, color, x, y, Cross_Line)
            return self.boxes[1][1]
    
        if self.boxes[2][0] == self.boxes[1][1] == self.boxes[0][2] != 0:
            if show:
                color = Circle_Color if self.boxes[1][1] == 2 else Cross_Color
                x = (20, Window_Height - 20 )
                y = (Window_Width -20, 20)
                pygame.draw.line(game_window, color, x, y, Cross_Line)
            return self.boxes[1][1]

        # No Win
        return 0
    
    # Used to keep track of the number of marked boxes
    def Fill_Box(self, row, column, player):
        self.boxes[row][column] = player
        self.marked_boxes += 1

    # Used to check if a box is empty
    def Empty_Box(self, row, col):
        return self.boxes[row][col] == 0
        
    # Used to keep track of the empty boxes
    def Get_Empty_Boxes(self):
        empty_boxes = []
        for row in range(Nb_Rows):
            for col in range(Nb_Columns):
                if self.Empty_Box(row, col):
                    empty_boxes.append((row, col))

        return empty_boxes
    
    def Board_Full(self):
        #check if all the boxes have been marked
        return (self.marked_boxes == 9)

# Agent Definition
class AI:
    
    def __init__(self, opponent = 1, player = 2):
        self.opponent = opponent
        self.player = player

    def Choose_Random(self, Board):
        empty_boxes = Board.Get_Empty_Boxes()
        index = random.randrange(0, len(empty_boxes))

        return empty_boxes[index]

    # Minimax - Dispatch Function
    def minimax (self, Board, maximizing) :
        case = Board.Final_State()

        if case == 1: # Winner = player 1
            return 1, None
        
        if case == 2: # Winner = player 2
            return -1, None
        
        elif Board.Board_Full(): # No Winner = draw
            return 0, None
        
        if (maximizing == True) :
            return self.max(Board) # calls maximising
        else :
            return self.min(Board) # calls minimizing

    # Minimax - Maximizing function
    def max(self, Board) :
        max_eval = -2
        best_move = None
        empty_boxes = Board.Get_Empty_Boxes ()

        for (row, col) in empty_boxes :
            tempBoard = copy.deepcopy(Board)
            tempBoard.Fill_Box(row,col,1)
            eval = self.minimax(tempBoard, False)[0]
            if eval > max_eval :
                max_eval = eval
                best_move = (row,col)

        return max_eval, best_move
    
    # Minimax - Minimizing function
    def min(self, Board) :
        min_eval = 2
        best_move = None
        empty_boxes = Board.Get_Empty_Boxes()

        for (row, col) in empty_boxes:
            temp_board = copy.deepcopy(Board)
            temp_board.Fill_Box(row, col, self.player)
            eval = self.minimax(temp_board, True)[0]
            if eval < min_eval:
                min_eval = eval
                best_move = (row, col)
        return min_eval, best_move
    
    # Alpha Beta Pruning - Dispatch function
    def miniMaxAlphaBeta(self, Board, maximizing, alpha, beta):
        case = Board.Final_State()

        if case == 1:
            return 1, None

        if case == 2:
            return -1, None
        
        elif Board.Board_Full():
            return 0, None

        if maximizing:
            return self.maxAlphaBeta(Board, alpha, beta)
        else:
            return self.minAlphaBeta(Board, alpha, beta)

    # Alpha Beta Pruning - Max function
    def maxAlphaBeta(self, Board, alpha, beta):
        max_eval = -2
        best_move = None
        empty_boxes = Board.Get_Empty_Boxes()

        for (row, col) in empty_boxes:
            tempBoard = copy.deepcopy(Board)
            tempBoard.Fill_Box(row, col, 1)
            eval = self.miniMaxAlphaBeta(tempBoard, False, alpha, beta)[0]
            if eval > max_eval:
                max_eval = eval
                best_move = (row, col)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval, best_move

    # Alpha Beta Pruning - Min function
    def minAlphaBeta(self, Board, alpha, beta):
        min_eval = 2
        best_move = None
        empty_boxes = Board.Get_Empty_Boxes()

        for (row, col) in empty_boxes:
            tempBoard = copy.deepcopy(Board)
            tempBoard.Fill_Box(row, col, self.player)
            eval = self.miniMaxAlphaBeta(tempBoard, True, alpha, beta)[0]
            if eval < min_eval:
                min_eval = eval
                best_move = (row, col)
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval, best_move
    
    # Depth Limited Search - Dispatch function
    def DLS(self, board, depth, maximizing, max_depth=float(3)):
        # the smaller max_depth the easier it is to win
        case = board.Final_State()

        if case == 1:
            return 1, None

        if case == 2:
            return -1, None

        elif board.Board_Full():
            return 0, None

        # Maximum depth reached
        if depth == max_depth:
            return 0, None
        
        if (maximizing == True) :
            return self.maxDLS(board, depth, max_depth)
        else :
            return self.minDLS(board, depth, max_depth)

    # Depth Limited Search - Max function
    def maxDLS (self, board, depth, max_depth):
        max_eval = -2
        best_move = None
        empty_boxes = board.Get_Empty_Boxes()

        for (row, col) in empty_boxes:
            temp_board = copy.deepcopy(board)
            temp_board.Fill_Box(row, col, 1)
            eval = self.DLS(temp_board, depth + 1, False, max_depth)[0]
            if eval > max_eval:
                max_eval = eval
                best_move = (row, col)

        return max_eval, best_move

    # Depth Limited Search - Min function
    def minDLS (self, board, depth, max_depth) :
        min_eval = 2
        best_move = None
        empty_boxes = board.Get_Empty_Boxes()

        for (row, col) in empty_boxes:
            temp_board = copy.deepcopy(board)
            temp_board.Fill_Box(row, col, self.player)
            eval = self.DLS(temp_board, depth + 1, True, max_depth)[0]
            if eval < min_eval:
                min_eval = eval
                best_move = (row, col)
        return min_eval, best_move
        
    def Evaluation_Function(self, Main_Board):
        if self.opponent == 0 :
            eval = 'random value'
            chosen_move = self.Choose_Random(Main_Board)

        elif self.opponent == 1:
            max_depth = 4 # change this to change depth level
            print(f"Minimax with depth limited to {max_depth}\n")
            eval, chosen_move = self.DLS(Main_Board, 0, False, max_depth)

        elif self.opponent == 2:
            print("Minimax with Alpha-Beta Pruning\n")
            eval, chosen_move = self.miniMaxAlphaBeta(Main_Board, False, -2, 2)

        elif self.opponent == 3 :
            print("Minimax\n")
            eval, chosen_move = self.minimax(Main_Board, False)

        print(f'AI chose {chosen_move} with an eval of {eval}')
        return chosen_move 

# WelcomePage Definition (to choose agent)

game_window.fill(Background_Color)

def main():
    game = Game()
    welcome = WelcomePage()
    board = game.board
    ai = game.ai
    
    chosen_opponent = False

    while True :
        for event in pygame.event.get():

            # Click X button - Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Press r - Restart
                if event.key == pygame.K_r:
                    welcome = WelcomePage()
                    game.restart()
                    board = game.board
                    ai = game.ai
                    chosen_opponent=False
                    # board = game.board
                    # ai = game.ai

                # Press 1 - Random AI
                if event.key == pygame.K_1:
                    game.Show_Lines()
                    game.Show_Restart()
                    chosen_opponent = True
                    ai.opponent=0

                # Press 2 - Minimax AI
                if event.key == pygame.K_2:
                    game.Show_Lines()
                    game.Show_Restart()
                    chosen_opponent = True
                    ai.opponent=1

                # Press 3 - Alpha Beta Pruning Minimax AI
                if event.key == pygame.K_3:
                    game.Show_Lines()
                    game.Show_Restart()
                    chosen_opponent = True
                    ai.opponent=2
                
                # Press 4 - DLS Minimax AI
                if event.key == pygame.K_4:
                    game.Show_Lines()
                    game.Show_Restart()
                    chosen_opponent = True
                    ai.opponent=3

            # After the human chooses the agent:
            if chosen_opponent:

                # Human clicks inside a box
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // Box_Size
                    col = pos[0] // Box_Size

                    if board.Empty_Box(row, col) and game.running:
                        game.Make_Move(row, col)

                        if game.Game_Over():
                            game.running = False

                # It is now AI's turn since we incremented game. player by 1 in the game.Make_Move() function
                if game.player == ai.player and game.running: 
                    pygame.display.update()

                    row, col = ai.Evaluation_Function(board)

                    board.Empty_Box(row, col)
                    board.Fill_Box(row, col, game.player)
                    game.Draw_Move(row, col)
                    game.Next_Turn()

                    if game.Game_Over():
                        game.running = False

            pygame.display.update()

main()
