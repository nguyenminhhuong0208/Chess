#xử lý đầu vào của người chơi và hiển thị trạng thái game hiệnt tại
import pygame as p
import chess_engine

BOARD_WIDTH = BOARD_HEIGHT = 512 # kích cỡ bàn cờ
DIMENSION = 8 # chia thành 64 ô
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION # kích cỡ mỗi ô
MAX_FPS = 15 # for animation later
IMAGES = {}

def loadImages():
    # khởi tạo một thư mục của hình ảnh.
    # ảnh được gọi chính xác một lần trong main.
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        # load ảnh của quân cờ tương ứng với ký hiệu tên từ folder images và fix với size mỗi ô 
        IMAGES[piece] = p.transform.scale(p.image.load(r"C:\Users\Admin\projects\CSTTNT\Chess\chess\images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE)) 

def main():
    # xử lý nước đi của user và cập nhật bàn cờ
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = chess_engine.GameState()
    print(game_state.board)
    loadImages()  # do this only once before while loop
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen,game_state)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, game_state):
    # Responsible for all the graphics within current game state.
    drawBoard(screen) # vẽ các ô vuông trên bàn cờ
    drawPieces(screen,game_state.board) # vẽ các quân cờ trên các ô vuông 

def drawBoard(screen):
    # hiển thị các hình vuông lên bàn cờ
    # hình vuông trên cùng bên trái luôn là ô trắng
    global colors
    colors = [p.Color("gray95"), p.Color("lightblue")] # lấy màu xám và xanh từ thư viện pygame
    for row in range(DIMENSION): # DIMENSION = 8
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)] # màu cho ô vuông hiện tại, 0 = gray95, 1 = lightblue
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # hiện hình vuông có color = color, size = SQUARE_SIZE lên màn hình

def drawPieces(screen, board):
    # hiển thị các quân cờ lên bàn cờ sử dụng game_state.board hiện tại
    for row in range(DIMENSION): # DIMENSION = 8
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # hiện hình quân cờ với ví trí column * SQUARE_SIZE, row * SQUARE_SIZE và kích thước SQUARE_SIZE  

if __name__ == "__main__":
    main()