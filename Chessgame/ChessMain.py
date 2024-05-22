
from time import sleep
import pygame as p
import ChessEngine, ChessAI
import Button
import sys
from multiprocessing import Process, Queue
import os as os

current_dir = os.path.dirname(__file__)
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION #! 64
MAX_FPS = 15
IMAGES = {}
DEFAULT_IMAGE_SIZE = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT)
background = p.image.load(os.path.join(current_dir, "images", "background4.jpg"))

background = p.transform.scale(background, DEFAULT_IMAGE_SIZE)
board = p.image.load(os.path.join(current_dir,"images","board.png"))
board = p.transform.scale(board, (250, 250))
p.display.set_caption('Chess')

# handle button click 
def clickButton():
    pass

def loadImages():
    
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(os.path.join(current_dir,"images", piece+".png")), (SQUARE_SIZE, SQUARE_SIZE))
        
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

def main():
    
    p.init()
    
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    
    clock = p.time.Clock()
    
    screen.fill(p.Color("white"))
    
    game_state = ChessEngine.GameState() 
    
    valid_moves = game_state.getValidMoves() 
    
    move_made = False  
    animate = False  
    loadImages()  
    running = True
    beginScreen = True
    square_selected = ()  
   
    player_clicks = []  
    difficulty = "hard" 
    
    
    font = p.font.Font('freesansbold.ttf', 20)
    
    
    while not (running == False and beginScreen == False):
        game_over = False
        ai_thinking = False
        move_undone = False
        move_finder_process = None
        move_log_font = p.font.SysFont("Arial", 16, bold = True, italic= False)
        player_one = True  
        player_two = True  
        mode = "" 
        buttonClicked = False
        target = ""
        time = 0
        while beginScreen:
            
            screen.blit(background,(0,0))
            
            # create button list 
            welcome = Button.Button("welcome", (80,-50), (600,300))
            instruction = Button.Button("instruction", (140,150), (160, 60))
            news = Button.Button("news", (140, 240), (160, 60))
            watch = Button.Button("watch", (140, 330), (160, 60))
            twoplayer = Button.Button("twoplayer", (460, 150), (160, 60))
            playcom = Button.Button("playcom", (460, 240), (160, 60))
            comcom = Button.Button("comcom", (460, 330), (160, 60))

            easy = Button.Button("easy", (460 + 160, 190), (100, 50))
            medium = Button.Button("medium", (460 +160,  240 ), (100, 50))
            hard = Button.Button("hard", (460 + 160, 290), (100, 50))

            welcome.displayButton(screen)
            buttonList = [instruction, news, watch, twoplayer, playcom, comcom]
            difficulties = [easy, medium, hard]

            for button in buttonList:
                button.displayButton(screen)       

            for button in buttonList:
                button.handleHover(screen)
            
            # check clicked for button easy, medium and hard
            if buttonClicked == True:
                
                for button  in difficulties:
                    button.displayButton(screen)
                    button.handleHover(screen)
            
            for e in p.event.get():
                if e.type == p.QUIT:
                    beginScreen = False
                if e.type == p.MOUSEBUTTONDOWN:
                    for button in buttonList:
                        if button.isMouseOnText() == True: 
                            mode = button.name
                            if mode == "news":
                                news.open("https://www.fide.com/news")
                                mode = ""
                            elif mode == "instruction":
                                news.open("https://www.youtube.com/watch?v=OCSbzArwB10")
                                mode = ""
                            elif mode == "watch":
                                news.open("https://www.chess.com/watch")
                                mode = ""
                            elif mode == "playcom":
                                buttonClicked = not buttonClicked
                            else: # if choose play mode, move to the game
                                time = p.time.get_ticks()
                                beginScreen = False
                                running = True
                                
                    for button in difficulties:
                        if buttonClicked == True and button.isMouseOnText() == True:
                            time = p.time.get_ticks()
                            beginScreen = False
                            running = True
                            difficulty = button.name
                            if button.name == "easy":
                                target = ChessAI.findBestMove
                            elif button.name == "medium":
                                target = ChessAI.findBestMove
                            elif button.name == "hard":
                                target = ChessAI.findBestMove
                            buttonClicked = not buttonClicked
                            
            p.display.flip()

        while running:
        
            # set mode 
            if mode == "twoplayer":
                #! neu an 1 thi reset game lai
                game_state = ChessEngine.GameState()
                valid_moves = game_state.getValidMoves()
                square_selected = ()
                player_clicks = []
                move_made = False
                animate = False
                game_over = False
                if ai_thinking:
                    move_finder_process.terminate()
                    ai_thinking = False
                move_undone = True
                #! this will be human vs human
                player_one = True
                player_two = True
                mode = ""
            elif mode == "playcom":
                #! reset game lai
                game_state = ChessEngine.GameState()
                valid_moves = game_state.getValidMoves()
                square_selected = ()
                player_clicks = []
                move_made = False
                animate = False
                game_over = False
                if ai_thinking:
                    move_finder_process.terminate()
                    ai_thinking = False
                move_undone = True
                
                #! human vs machine
                player_one = True
                player_two = False
                mode = ""
                
            elif mode == "comcom":
                    #! reset game lai
                game_state = ChessEngine.GameState()
                valid_moves = game_state.getValidMoves()
                square_selected = ()
                player_clicks = []
                move_made = False
                animate = False
                game_over = False
                target = ChessAI.findBestMove
                
                # move_undone = True
                player_one = False
                player_two = False
                mode = ""
            
        
            
            if (game_state.trangDiChuyen and player_one == True) or (not game_state.trangDiChuyen and player_two == True):
                human_turn = True
            else:
                human_turn = False
            
            
            for e in p.event.get():    
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                # mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    if homebutton.isMouseOnText() == True: 
                        clock = p.time.Clock()
                        beginScreen = True
                        running = False
                        break
                        
                        
                    if not game_over:
                        location = p.mouse.get_pos()  # (x, y) location of the mouse
                        col = location[0] // SQUARE_SIZE
                        row = location[1] // SQUARE_SIZE
                        if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                            square_selected = ()  # deselect
                            player_clicks = []  # clear clicks
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)  # append for both 1st and 2nd click
                        if len(player_clicks) == 2 and human_turn:  # after 2nd click
                            move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.makeMove(valid_moves[i])
                                    move_made = True
                                    animate = True
                                    square_selected = ()  # reset user clicks
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [square_selected]

                # key handler
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:  # undo when 'z' is pressed
                        game_state.undoMove()
                        move_made = True
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    if e.key == p.K_r:  # reset the game when 'r' is pressed
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True

            #! Phần di chuyển của AI
            
            if not game_over and not human_turn and not move_undone:
                
                if not ai_thinking:
                    ai_thinking = True
                    return_queue = Queue() 
                    move_finder_process = Process(target=target, args=(game_state, valid_moves, return_queue, difficulty))
                    move_finder_process.start()
                    

                if not move_finder_process.is_alive():
                    
                    ai_move = return_queue.get()
                    if ai_move is None:
                        print("RANDOM ALGOR IS CALLED!")
                        ai_move = ChessAI.findRandomMove(valid_moves)
                    game_state.makeMove(ai_move)
                    
                    move_made = True
                    animate = True
                    ai_thinking = False

            
            if move_made:
                if animate:
                    animateMove(game_state.move_log[-1], screen, game_state.board, clock)
                valid_moves = game_state.getValidMoves()
                move_made = False
                animate = False
                move_undone = False

            
            drawGameState(screen, game_state, valid_moves, square_selected)

            if not game_over:
                drawMoveLog(screen, game_state, move_log_font)

            if game_state.checkmate:
                game_over = True
                if game_state.trangDiChuyen:
                    drawEndGameText(screen, "Black wins by checkmate")
                else:
                    drawEndGameText(screen, "White wins by checkmate")

            elif game_state.stalemate:
                game_over = True
                drawEndGameText(screen, "Stalemate")
            
            

            playtime = Button.Button('playtime', (60, 150), (400, 200))
            if  time <= p.time.get_ticks() and p.time.get_ticks() <= time + 2000:
                playtime.displayButton(screen)
            
            homebutton = Button.Button('homebutton', (560, 452), (50, 50))
            helpbutton = Button.Button('help', (640, 430), (90, 90))
            twoplayermode = Button.Button('twoplayermode', (60, 150), (400, 200))
            playcommode = Button.Button('playcommode', (60, 150), (400, 200))
            twocommode = Button.Button('twocommode', (60, 150), (400, 200))

            if helpbutton.isMouseOnText() == True:
                helpnoti = Button.Button("helpnoti", (512, 240), (250, 250))
                helpnoti.displayButton(screen)
            
            if time + 2000 <= p.time.get_ticks() and p.time.get_ticks() <=  time + 5000:
                if (player_one == True) and (player_two == True):
                    twoplayermode.displayButton(screen)        
                elif (player_one == True) and (player_two == False):
                    playcommode.displayButton(screen)        
                elif (player_one == False) and (player_two == False):
                    twocommode.displayButton(screen)
            
            
            homebutton.displayButton(screen)
            homebutton.handleHover(screen)
            helpbutton.displayButton(screen)
            helpbutton.handleHover(screen)

            clock.tick(MAX_FPS)
            p.display.flip()

    

def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    vẽ bàn cờ của hiện tại 
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen):
    """
    Vẽ hình
    """
    global colors
    colors = [p.Color((118,150,86)), p.Color((238,238,210))]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    highlight hình vuông
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('pink'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.trangDiChuyen else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))


def drawPieces(screen, board):
    """
    vẽ quân cờ trên bàn cờ
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawMoveLog(screen, game_state, font):
    
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color((186,202,88)), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


def animateMove(move, screen, board, clock):
    
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_totQuaDuong_move:
                totQuaDuong_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, totQuaDuong_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()