class Player:
    def __init__(self, color):
        self.color = color   #data (attribute)
        self.pieces = []     #data (attribute)

    def __repr__(self):      # Method that manipulates internal data
        return f'Player({self.color})'

    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)

    def get_pieces_count(self):
        return len(self.pieces)

    def has_pieces(self): # Method that gives access without exposing raw list
        return len(self.pieces) > 0

    def get_all_possible_moves(self, board):
        all_moves = []
        for row in range(8):
            for col in range(8):
                if board.board[row][col] is not None and board.board[row][col].color == self.color:
                    piece_moves = board.board[row][col].get_possible_moves(board.board, row, col)
                    all_moves.extend(piece_moves)
        return all_moves

