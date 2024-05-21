"""
Storing all the information about the current state of chess game.
Determining valid moves at current state.
It will keep move log.
"""


class GameState:
    def __init__(self):
        """
        trạng thái thực của game trên board. Hàm này sẽ giúp cập nhật trạng thái chính của game
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.trangDiChuyen = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []
        self.totQuaDuong_possible = ()  # coordinates for the square where en-passant capture is possible
        self.totQuaDuong_possible_log = [self.totQuaDuong_possible]
        self.current_nhapThanh_rights = nhapthanhRights(True, True, True, True)
        self.nhapthanh_rights_log = [nhapthanhRights(self.current_nhapThanh_rights.wks, self.current_nhapThanh_rights.bks,
                                               self.current_nhapThanh_rights.wqs, self.current_nhapThanh_rights.bqs)]

    def makeMove(self, move):
        """
        
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        #! sử dụng move_log để có thể undo move lại bất cứ lúc nào
        self.move_log.append(move)  
        #! sau khi mình đi thì tới họ đi
        self.trangDiChuyen = not self.trangDiChuyen 
         #! Vì vị trí của vua ngoài đi 1 nước còn liên quan tới nhập thành, nên khi di chuyển thì phải keeptrack nó
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        #! tốt thăng cấp
        if move.is_pawn_promotion:
            
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        #! bắt tốt qua đường
        if move.is_totQuaDuong_move:
            '''
            con tốt ở điểm start_row và end_col sẽ bị xóa. 
            '''
            self.board[move.start_row][move.end_col] = "--"  # capturing the pawn

        #! luật bắt tốt qua đường
        #! nếu như tốt đối thủ lên 2 bước trong lần đầu, 
        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2:  # only on 2 square pawn advance
            self.totQuaDuong_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.totQuaDuong_possible = ()

        # nhapthanh move
        if move.is_nhapthanh_move:
            if move.end_col - move.start_col == 2:  #! đối với nhập thành 4 ô đầu tiên
                #! self.board[move.end_row][move.end_col + 1] là vị trí của con xe 
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]  # moves the rook to its new square
                self.board[move.end_row][move.end_col + 1] = '--'  # erase old rook
            else:  # queen-side nhapthanh move
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]  # moves the rook to its new square
                self.board[move.end_row][move.end_col - 2] = '--'  # erase old rook

        #! cái này để undo được move
        self.totQuaDuong_possible_log.append(self.totQuaDuong_possible)

        # update nhapThanh rights - whenever it is a rook or king move
        self.updatenhapthanhRights(move)
        self.nhapthanh_rights_log.append(nhapthanhRights(self.current_nhapThanh_rights.wks, self.current_nhapThanh_rights.bks,
                                                   self.current_nhapThanh_rights.wqs, self.current_nhapThanh_rights.bqs))

    def undoMove(self):
        """
        Undo the last move
        """
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.trangDiChuyen = not self.trangDiChuyen  # swap players
            # update the king's position if needed
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)
            # undo tốt qua đường move
            if move.is_totQuaDuong_move:
                self.board[move.end_row][move.end_col] = "--"  # leave landing square blank
                self.board[move.start_row][move.end_col] = move.piece_captured

            self.totQuaDuong_possible_log.pop()
            self.totQuaDuong_possible = self.totQuaDuong_possible_log[-1]

            # undo nhapthanh rights
            self.nhapthanh_rights_log.pop()  # get rid of the new nhapthanh rights from the move we are undoing
            self.current_nhapThanh_rights = self.nhapthanh_rights_log[
                -1]  # set the current nhapthanh rights to the last one in the list
            # undo the nhapthanh move
            if move.is_nhapthanh_move:
                if move.end_col - move.start_col == 2:  # king-side
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = '--'
                else:  # queen-side
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = '--'
            self.checkmate = False
            self.stalemate = False

    def updatenhapthanhRights(self, move):
        """
        Update the nhapthanh rights given the move
        """
        if move.piece_captured == "wR":
            if move.end_col == 0:  # left rook
                self.current_nhapThanh_rights.wqs = False
            elif move.end_col == 7:  # right rook
                self.current_nhapThanh_rights.wks = False
        elif move.piece_captured == "bR":
            if move.end_col == 0:  # left rook
                self.current_nhapThanh_rights.bqs = False
            elif move.end_col == 7:  # right rook
                self.current_nhapThanh_rights.bks = False

        if move.piece_moved == 'wK':
            self.current_nhapThanh_rights.wqs = False
            self.current_nhapThanh_rights.wks = False
        elif move.piece_moved == 'bK':
            self.current_nhapThanh_rights.bqs = False
            self.current_nhapThanh_rights.bks = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:  # left rook
                    self.current_nhapThanh_rights.wqs = False
                elif move.start_col == 7:  # right rook
                    self.current_nhapThanh_rights.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:  # left rook
                    self.current_nhapThanh_rights.bqs = False
                elif move.start_col == 7:  # right rook
                    self.current_nhapThanh_rights.bks = False

    def getValidMoves(self):
        """
        kiểm tra toàn bộ nước đi 
        """
        temp_nhapthanh_rights = nhapthanhRights(self.current_nhapThanh_rights.wks, self.current_nhapThanh_rights.bks,
                                          self.current_nhapThanh_rights.wqs, self.current_nhapThanh_rights.bqs)
        
        moves = []
        self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.trangDiChuyen:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.getAllPossibleMoves()
                # to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0]  # check information
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i,
                                        king_col + check[3] * i)  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:  # once you get to piece and check
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
                    if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block or capture
                        if not (moves[i].end_row,
                                moves[i].end_col) in valid_squares:  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(king_row, king_col, moves)
        else:  # not in check - all moves are fine
            moves = self.getAllPossibleMoves()
            if self.trangDiChuyen:
                self.getnhapthanhMoves(self.white_king_location[0], self.white_king_location[1], moves)
            else:
                self.getnhapthanhMoves(self.black_king_location[0], self.black_king_location[1], moves)

        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                # TODO stalemate on repeated moves
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.current_nhapThanh_rights = temp_nhapthanh_rights
        
        
        return moves

    def inCheck(self):
        """
        kiểm tra có bị chiếu tướng không
        """
        if self.trangDiChuyen:
            return self.squareUnderAttack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.squareUnderAttack(self.black_king_location[0], self.black_king_location[1])

    def squareUnderAttack(self, row, col):
        """
        Kiểm tra đối thủ có đang chuẩn bị ăn ô này không
        """
        self.trangDiChuyen = not self.trangDiChuyen  # switch to opponent's point of view
        opponents_moves = self.getAllPossibleMoves()
        self.trangDiChuyen = not self.trangDiChuyen
        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:  # square is under attack
                return True
        return False

    def getAllPossibleMoves(self):
        """
        All moves without considering checks.
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.trangDiChuyen) or (turn == "b" and not self.trangDiChuyen):
                    piece = self.board[row][col][1]
                    #print("this is my piece: "+str(piece))
                    self.moveFunctions[piece](row, col, moves)  # calls appropriate move function based on piece type
        #print("This is my moves in getAllPossibleMoves: ",moves)
        return moves

    def checkForPinsAndChecks(self):
        '''
        
        '''
        pins = []  # squares pinned and the direction its pinned from
        checks = []  # squares where enemy is applying a check
        in_check = False
        if self.trangDiChuyen:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()  # reset possible pins
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == ():  # first allied piece could be pinned
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:  # 2nd allied piece - no check or pin from this direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                i == 1 and enemy_type == "p" and (
                                (enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (
                                enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board
        # check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks

#! ------------------------------------------------------ nước đi của các quân cờ ------------------------------------------
    def getPawnMoves(self, row, col, moves):
        """
        lấy các nước của quân tốt, hàm này siêu khó
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.trangDiChuyen:
            move_amount = -1
            start_row = 6
            enemy_color = "b"
            king_row, king_col = self.white_king_location
        else:
            move_amount = 1
            start_row = 1
            enemy_color = "w"
            king_row, king_col = self.black_king_location

        if self.board[row + move_amount][col] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((row, col), (row + move_amount, col), self.board))
                if row == start_row and self.board[row + 2 * move_amount][col] == "--":  # 2 square pawn advance
                    moves.append(Move((row, col), (row + 2 * move_amount, col), self.board))
        if col - 1 >= 0:  # capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][col - 1][0] == enemy_color:
                    moves.append(Move((row, col), (row + move_amount, col - 1), self.board))
                if (row + move_amount, col - 1) == self.totQuaDuong_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_col + 1, col - 1)
                            outside_range = range(col + 1, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col, -1)
                            outside_range = range(col - 2, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col), (row + move_amount, col - 1), self.board, is_totQuaDuong_move=True))
        if col + 1 <= 7:  # capture to the right
            if not piece_pinned or pin_direction == (move_amount, +1):
                if self.board[row + move_amount][col + 1][0] == enemy_color:
                    moves.append(Move((row, col), (row + move_amount, col + 1), self.board))
                if (row + move_amount, col + 1) == self.totQuaDuong_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_col + 1, col)
                            outside_range = range(col + 2, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col + 1, -1)
                            outside_range = range(col - 1, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col), (row + move_amount, col + 1), self.board, is_totQuaDuong_move=True))

    def getRookMoves(self, row, col, moves):
        """
        lấy toàn bộ nước đi của xe
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][
                    1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.trangDiChuyen else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getKnightMoves(self, row, col, moves):
        """
        lấy toàn bộ nước đi của mã
        """
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                        (1, -2))  # up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.trangDiChuyen else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                        moves.append(Move((row, col), (end_row, end_col), self.board))

    def getBishopMoves(self, row, col, moves):
        """
        lấy toàn bộ nước đi của tượng
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  
        enemy_color = "b" if self.trangDiChuyen else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  #! nước đi trong giới hạn của bàn cờ
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  #! ô trống thì đi được
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                             
                        elif end_piece[0] == enemy_color:  #! nếu là địch thì ăn được
                            
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  
                            break
                else:  
                    break

    def getQueenMoves(self, row, col, moves):
        """
        nước đi của hậu là kết hợp tượng và xe
        """
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        """
        các nước đi của vua
        """
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.trangDiChuyen else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.checkForPinsAndChecks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if ally_color == "w":
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

    def getnhapthanhMoves(self, row, col, moves):
        """
        Generate all valid nhapthanh moves for the king at (row, col) and add them to the list of moves.
        """
        if self.squareUnderAttack(row, col):
            return  #! nếu như đang bị chiếu tướng thì không thể nhập thành được
        if (self.trangDiChuyen and self.current_nhapThanh_rights.wks) or (not self.trangDiChuyen and self.current_nhapThanh_rights.bks):
            self.getKingsidenhapthanhMoves(row, col, moves)
        if (self.trangDiChuyen and self.current_nhapThanh_rights.wqs) or (not self.trangDiChuyen and self.current_nhapThanh_rights.bqs):
            self.getQueensidenhapthanhMoves(row, col, moves)

    def getKingsidenhapthanhMoves(self, row, col, moves):
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, is_nhapthanh_move=True))

    def getQueensidenhapthanhMoves(self, row, col, moves):
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, is_nhapthanh_move=True))
    
    def get_all_pieces(self):
        """
        dem so quan co tren ban co
        """
        # pieces = []
        # for row in self.board:
        #     for square in row:
        #         if square != "--":  # Assuming empty squares are represented as "--"
        #             pieces.append(square)
        # return pieces  
             
        print(sum(sum(char != "--" for char in row) for row in self.board))
        return sum(sum(char != "--" for char in row) for row in self.board)

class nhapthanhRights:
    '''
    Hàm này để nhập thành về bên 4 ô
    '''
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    '''
    Vì tọa độ thực của chess là vừa chữ và số, nên chúng ta encode hết toàn bộ 
    (start_row,start_col): trả về tọa độ lần đầu tiên bấm vào con cờ
    (end_row,end_col): trả về tọa độ lần 2 bấm vào cờ
    piece_moved: trả về index của quân cờ move theo dạng bK,... (index này lấy theo những gì ghi trên board)
    piece_captured: trả về con cờ bị ăn (điều này đạt được nhờ board[self.end_row][self.end_col])
    
    
    hàm này được gọi ở main theo kiểu:  move = ChessEngine.Move(playerClicks[0],playerClicks[1],gamestate.board)
    
    
    class này để biết được chúng ta đã đi những đâu
    self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
    
    
    '''
    #! Câu hỏi: tại sao lại phải encode 1-8 là số 7 - 0? Tọa độ (row,col) sau convert là location / 64. 
    #! bàn cờ: y dưới lên: 1-8, x (trái sang phải): a - h
    #! ------------------- encode bàn cờ ra tọa độ máy hiểu --------------------------------
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    #! fix 2 cột này
    rows_to_ranks = {7: "1", 6: "2", 5: "3", 4: "4", 3:"5" , 2: "6" , 1: "7" , 0: "8"}
    
    char_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    
    cols_to_char = {0: 'a',1: 'b', 2: 'c',3: "d",4: 'e',5: "f",6: 'g',7: 'h'}

    #! --------------------------------------------------------------------

    def __init__(self, start_square, end_square, board, is_totQuaDuong_move=False, is_nhapthanh_move=False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (
                self.piece_moved == "bp" and self.end_row == 7)
        # en passant #! đoạn en passant này là sao? 
        self.is_totQuaDuong_move = is_totQuaDuong_move
        if self.is_totQuaDuong_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"
        # nhapthanh move
        #! nhập thành
        self.is_nhapthanh_move = is_nhapthanh_move

        #! biến is_capture này để làm gì? 
        self.is_capture = self.piece_captured != "--"
        
        #! biến move_id này để làm gì? 
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        """
        Overriding the equals method.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        '''
        if self.is_pawn_promotion:
            nếu 
            return self.getRankFile(self.end_row, self.end_col) + "Q"
        '''
        if self.is_pawn_promotion:
            return self.getRankFile(self.end_row, self.end_col) + "Q"
        
        #! 2 cái hàm if dưới chưa hiểu rõ!
        if self.is_nhapthanh_move:
            # print(" if self.is_nhapthanh_move is called") cái này chưa được gọi lần nào
            if self.end_col == 1:
                return "0-0-0"
            else:
                return "0-0"
        if self.is_totQuaDuong_move:
            return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
                                                                                                self.end_col) + " e.p."
        if self.piece_captured != "--":
            if self.piece_moved[1] == "p":
                return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
                                                                                                    self.end_col)
            else:
                return self.piece_moved[1] + "x" + self.getRankFile(self.end_row, self.end_col)
        else:
            if self.piece_moved[1] == "p":
                return self.getRankFile(self.end_row, self.end_col)
            else:
                return self.piece_moved[1] + self.getRankFile(self.end_row, self.end_col)

        # TODO Disambiguating moves

    def getRankFile(self, row, col):
        '''
        hàm này để trả về vị trí của quân cờ theo bàn cờ thực tế.
        Ví dụ đang ở (0,0) thì nó encode về (a8)
        '''
        return self.cols_to_char[col] + self.rows_to_ranks[row]

    def __str__(self):
        if self.is_nhapthanh_move:
            return "0-0" if self.end_col == 6 else "0-0-0"

        end_square = self.getRankFile(self.end_row, self.end_col)

        if self.piece_moved[1] == "p":
            if self.is_capture:
                return self.cols_to_char[self.start_col] + "x" + end_square
            else:
                return end_square + "Q" if self.is_pawn_promotion else end_square

        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square