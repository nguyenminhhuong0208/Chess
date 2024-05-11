# chứa thông tin về trạng thái hiện tại của game
# quyết định nước đi tiếp theo
# lưu nhật ký lượt chơi

class GameState:
    def __init__(self):
        # bàn cờ kích thước 8x8, mỗi ký hiệu đại diện cho 1 quân cờ
        # 'b' - quân đen, 'w' - quân trắng
        # 'K' - vua 'Q' - hậu,  'B' - tượng, 'N' - mã, 'R' - xe, 'p' - tốt
        # 'bQ' - hậu đen
        # '--' ô trống
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []