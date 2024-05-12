
import pygame as p
import ChessEngine
#! khoi tao man hinh
HEIGHT = WIDTH = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15

IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('./my_own_chess/images/'+piece+'.png'),(SQ_SIZE,SQ_SIZE))


#! main function
def main():
    p.init()
    screen = p.display.set_mode((HEIGHT,WIDTH))
    clock = p.time.Clock()
    screen.fill(color='white')
    gamestate = ChessEngine.GameState()
    
    validMoves = gamestate.getValidMoves() #! check n co the check king minh k
    moveMade = False #! neu nhu nguoi dung di move ma bi check thi phai regenerate
    
    
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while (running):
        for e in p.event.get():
            if e.type == p.QUIT:
                print("Quit is presed")
                running = False #! break loop neu nhan key listener la quit tu queue
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #! get (x,y)
                col = location[0]//SQ_SIZE
                #print("This is my col: "+str(col))
                row = location[1]//SQ_SIZE
                #print("This is my row: "+str(row))
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    #print("lenplayer click is 2")
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gamestate.board)
                    print(move.getChessNotation())

                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gamestate.makeMove(validMoves[i])
                            
                            moveMade = True #! người dùng đi không bị chiếu tướng 
                    #! reset user click
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            # keyhandler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    #! press Z will undo move. 
                    gamestate.undoMove()
                    moveMade = True
        if moveMade:
            #! TODO: tại sao lại phải có dòng này? 
            validMoves = gamestate.getValidMoves()
            #moveMade = False
                
        drawGameState(screen,gamestate.board)
        
        clock.tick(MAX_FPS) #! ham nay de lam gi?
        p.display.flip() #! khong co ham nay thi se khong display duoc gi ca vi no se ve lai nhung gi minh da thay doi tren screen
def drawPieces(screen,board):
    '''
    Blit (overlap) the surface on the canvas at the rect position
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                #! đây sẽ là phần draw các quân cờ
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
def drawGameState(screen,board):
    drawBoard(screen)
    drawPieces(screen,board)
def drawBoard(screen):
    '''
    this function will draw only rect in screen
    remember: topleft is always white
    '''
    colors = [p.Color('white'),p.Color('yellow')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2] #! nếu mà tổng chia hết -> 0 -> ô trắng.
            #! nếu chia dư 1 -> ô còn lại. 
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #! ve col truoc roi den row sau
if __name__ == "__main__":
    main()
