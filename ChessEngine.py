#! responsible for current state and game log
class GameState:
    def __init__(self):
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
        
        self.moveFunctions = {'p': self.getTotMoves,'R': self.getXeMoves, 'N': self.getMaMoves, 'B': self.getTuongMoves, 
                              'Q': self.getHauMoves, 'K': self.getKingMoves}
        
        self.whiteToMove = True
        self.movelog = []
        
        
        
    def makeMove(self,move):
        '''
        to move object
        move: Move.move
        '''
        #! 2 dòng này để làm gì? 
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved #! đây là dòng sẽ update board
        
        self.movelog.append(move) #! so we can display history
        
        #! switch player turn! 
        self.whiteToMove = not self.whiteToMove
    
    def undoMove(self):
        '''
        this function will undo move!
        '''
        if len(self.movelog) != 0: 
            #! if there is no move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        '''
        basic algor of get valid move:
        - get all possible move
        - for each possible move: 
            - if it is_a_valid_move:
        def is_a_valid_mode():
            - make the move
            - generate all possible moves
            - if any move atack your king? 
                if king safe -> valid
                else:
                invalid
            return list(valid_move)
        '''
        return self.getAllPossibleMoves() #! not to worry about check
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])): 
                turn = self.board[r][c][0] #! check xem n la black hay white
                #print("here")
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and (not self.whiteToMove)):
                    piece = self.board[r][c][1]
                    #print("This is my piece: "+piece)
                    self.moveFunctions[piece](r,c,moves) #! goi ra cac ham tuong ung voi value trong dictionary
        return moves
    def getTotMoves(self,r,c,moves):
        if self.whiteToMove: #! white tot move
            if self.board[r-1][c] == "--": #! square tot advance
                #print("here")
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--": 
                    moves.append(Move((r,c),(r-2,c),self.board))

            #! capture
            if c-1 >= 0: #! without go to col -1
                if self.board[r-1][c-1][0] == 'b': #! enemy piece to capture to the left
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c + 1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        #self.whiteToMove = not self.whiteToMove
        else:
            #! black is move
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                    
                    
        
    def getXeMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        ally_color = 'w' if self.whiteToMove else 'b'
        for d in directions:
            for i in range(1,8):
                endrow = r + d[0]*i
                endcol = c + d[1]*i
                #! check xem no trong board khong
                if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--":
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                    elif endpiece[0] != ally_color:
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                        
        
    def getMaMoves(self,r,c,moves):
        directions = ((-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(-1,2),(1,-2),(1,2))
        ally_color = 'w' if self.whiteToMove else 'b'
        for d in directions:
            endrow = r + d[0]
            endcol = c + d[1]
            #! check xem no trong board khong
            if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                endpiece = self.board[endrow][endcol]
                if endpiece == "--":
                    moves.append(Move((r,c),(endrow,endcol),self.board))
                elif endpiece[0] != ally_color:
                    moves.append(Move((r,c),(endrow,endcol),self.board))
                   
    def getTuongMoves(self,r,c,moves):
        '''
        di logic giong het xe
        '''
        directions = ((-1,-1),(1,-1),(1,1),(-1,1))
        ally_color = 'w' if self.whiteToMove else 'b'
        for d in directions:
            for i in range(1,8):
                endrow = r + d[0]*i
                endcol = c + d[1]*i
                #! check xem no trong board khong
                if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--":
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                    elif endpiece[0] != ally_color:
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                        
    def getHauMoves(self,r,c,moves):
        self.getXeMoves(r,c,moves)
        self.getTuongMoves(r,c,moves)
    def getKingMoves(self,r,c,moves):
        directions = ((-1,-1),(1,-1),(1,1),(-1,1),(1,0),(0,1),(-1,0),(0,-1))
        ally_color = 'w' if self.whiteToMove else 'b'
        
        for i in range(8):
            endrow = r + directions[i][0]
            endcol = c + directions[i][1]
            #! check xem no trong board khong
            if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                endpiece = self.board[endrow][endcol]
                if endpiece == "--":
                    moves.append(Move((r,c),(endrow,endcol),self.board))
                elif endpiece[0] != ally_color:
                    moves.append(Move((r,c),(endrow,endcol),self.board))
                    
class Move:
    '''
    class này để biết được chúng ta đã đi những đâu
    '''
    #! khởi tạo encode bàn cờ dạng số. Nhưng khi chúng ta dùng thì gọi theo tọa độ chess thông thường
    ranksToRows = {"1": 7, "2":6, "3":5,"4":4, "5":3, "6":2, "7": 1, "8":0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()} #! encode ngược lại của ranksToRows
    ranksToCols = {"a": 0, "b":1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToRanks = {v: k for k,v in ranksToCols.items()}
    #! ----------------------------------------------------------------------------------------
    
    def __init__(self,startSq, endSq, board):
        #! cần phải đảm bảo chúng ta sẽ có valid move
        #! chúng ta cần tạo sao cho có thể undo move được! 
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        
        #! how to grap this data from our board
        #! this will help us keep track log
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*1000 + self.endRow*10 + self.endCol #! cái này để làm gì? 
        #print(self.moveID)
        #! chúng ta cần biết rõ từng tọa độ trên bản đồ -> trong chess thì một cái là số, 1 cái là chữ. Vì vậy để về 0,0
        #! thì cần phải decode nó với dict
    '''
    overridding constructor
    '''  
    def __eq__(self,other):
        '''
        không hiểu hàm này để làm gì? (vid 3)
        '''
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
        
        
        
    def getChessNotation(self):
        '''
        Cho bạn biết bạn đã đi đâu
        '''
        
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
        
    def getRankFile(self,row,col):
        '''
        Hàm này sẽ trả về tọa độ bàn cờ ở trên màn hình
        '''
        return self.colsToRanks[col] + self.rowsToRanks[row]