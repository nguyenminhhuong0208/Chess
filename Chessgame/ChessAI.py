"""
AI stuff
"""
import time 

import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}





CHECKMATE = 100
STALEMATE = 0
DEPTH = 3

#! greedy algorithm:
#! look at all move, which move is the best

def greedySearch(game_state,valid_move):
    '''
    Nhìn tất cả nước đi xem nước nào là tốt nhất
    '''
    global next_move
    turnMultiplier = 1 if game_state.trangDiChuyen else -1
    opponentMinMaxScore = CHECKMATE
    
    for playerMove in valid_move:
        game_state.makeMove(playerMove)
        opponentMoves = game_state.getValidMoves()
        if game_state.checkmate:
            opponentMaxScore = -CHECKMATE
        elif game_state.stalemate:
            opponentMaxScore = STALEMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentMoves:
                game_state.makeMove(opponentMove)
                game_state.getValidMoves()
                if game_state.checkmate:
                    score = CHECKMATE
                elif game_state.stalemate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreBoard(game_state)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                game_state.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestMove = playerMove
        game_state.undoMove()

    next_move = bestMove
'''
Giả sử mình là thằng đầu di chuyển, thì mình sẽ chọn max!
đến depth là 1, lượt của đối phương -> false trong hàm trangDiChuyen. 
Sau đó thì đen sẽ chọn score min nhất.
Đen tổng càng âm điểm thì nó càng thắng!
'''

def findMoveSCout(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves() 
        
        
        score = -findMoveSCout(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if alpha < score < beta:
            score = -findMoveSCout(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        else:
            #! nếu score không nằm trong khoảng từ alpha tới beta, tức là có thể có điểm tốt hơn ở phía sau 
            score = -findMoveSCout(game_state,next_moves,depth - 1,-alpha-1,-alpha,-turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score




def findBestMove(game_state, valid_moves, return_queue, difficulty):
    '''
    return the best move by call algor method!
    next_move: Lúc này sẽ chứa tên của quân cờ mà nó đi!
    '''
    global next_move
    
    
    next_move = None
    random.shuffle(valid_moves)
    
    if difficulty == "hard":       
        findMoveNegaMaxAlphaBeta(game_state, valid_moves,DEPTH , -CHECKMATE, CHECKMATE,1 if game_state.trangDiChuyen else -1)
    
    elif difficulty == "medium":
        findMoveSCout(game_state, valid_moves,DEPTH , -CHECKMATE, CHECKMATE,1 if game_state.trangDiChuyen else -1)
        
    elif difficulty == "easy":
        greedySearch(game_state,valid_moves)
    #print("My next move: ",next_move)
    return_queue.put(next_move)
    
def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score



def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    
    sum up the score
    
    piece[1] Là tên quân cờ, được chấm điểm dựa trên dict đã cho sẵn
    """
    if game_state.checkmate:
        if game_state.trangDiChuyen:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    
    
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                    #piece_position_score = 0
                if piece[0] == "w":
                    # print("This is my piece[1] at positive: ",piece[1])
                    # print("This is my piece_score[piece[1]] at positive: ",piece_score[piece[1]])
                    score += piece_score[piece[1]] + piece_position_score
                    # print("This is my positive score: ",score)
                    score += piece_score[piece[1]]
                if piece[0] == "b":
                    # print("This is my piece[1] at negative: ",piece[1])
                    # print("This is my piece_score[piece[1]] at negative: ",piece_score[piece[1]])
                    score -= piece_score[piece[1]] + piece_position_score
                    # print("This is my negative score: ",score)
                    # score -= piece_score[piece[1]]
    return score

#! random play
def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    
    """
    #! choice is choose random element in valid move
    return random.choice(valid_moves)

