from .Piece import Man, King

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()

    def initialize_board(self):
        # Place black pieces (top 3 rows, dark squares only)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:  # Dark squares
                    self.board[row][col] = Man('black')

        # Place white pieces (bottom 3 rows, dark squares only)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:  # Dark squares
                    self.board[row][col] = Man('white')

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def set_piece(self, row, col, piece):
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece

    def remove_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.board[row][col]
            self.board[row][col] = None
            return piece
        return None

    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.get_piece(from_row, from_col)
        if piece is None:
            return False

        # Check if move is valid
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False

        # Move the piece
        self.remove_piece(from_row, from_col)
        self.set_piece(to_row, to_col, piece)

        # Check for capture
        if abs(to_row - from_row) == 2:
            captured_row = (from_row + to_row) // 2
            captured_col = (from_col + to_col) // 2
            captured_piece = self.remove_piece(captured_row, captured_col)

        # Check for king promotion
        if piece.color == 'white' and to_row == 0 and not piece.is_king:
            self.board[to_row][to_col] = King(piece.color)
        elif piece.color == 'black' and to_row == 7 and not piece.is_king:
            self.board[to_row][to_col] = King(piece.color)

        return True

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        # Check bounds
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8):
            return False

        # Check if there's a piece to move
        piece = self.get_piece(from_row, from_col)
        if piece is None:
            return False

        # Check if destination is empty
        if self.get_piece(to_row, to_col) is not None:
            return False

        # Check if destination is on a dark square
        if (to_row + to_col) % 2 == 0:
            return False

        # Get possible moves for the piece
        possible_moves = piece.get_possible_moves(self.board, from_row, from_col)
        return ((from_row, from_col), (to_row, to_col)) in possible_moves

    def get_all_pieces(self, color):
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None and piece.color == color:
                    pieces.append((piece, row, col))
        return pieces

    def display(self):
        print("  A B C D E F G H")
        for row in range(8):
            print(f"{8-row} ", end="")
            for col in range(8):
                if (row + col) % 2 == 0:
                    print("□", end=" ")  # Light square
                else:
                    piece = self.board[row][col]
                    if piece is None:
                        print("■", end=" ")  # Dark empty square
                    else:
                        if piece.is_king:
                            print("♔" if piece.color == 'white' else "♚", end=" ")
                        else:
                            print("○" if piece.color == 'white' else "●", end=" ")
            print(f" {8-row}")
        print("  A B C D E F G H")

    def copy(self):
        new_board = Board()
        for row in range(8):
            for col in range(8):
                if self.board[row][col] is not None:
                    piece = self.board[row][col]
                    if piece.is_king:
                        new_board.board[row][col] = King(piece.color)
                    else:
                        new_board.board[row][col] = Man(piece.color)
                else:
                    new_board.board[row][col] = None
        return new_board

