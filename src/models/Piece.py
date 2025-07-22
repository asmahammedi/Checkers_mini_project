# Base class for all pieces (Man and King)
class Piece:
    def __init__(self, color):
        self.color = color
        self.is_king = False

    def __repr__(self):
        return f'{self.color[0].upper()}'

    def get_possible_moves(self, board, row, col): #Polymorphism: forces child classes to override this method differently
        raise NotImplementedError

#Inheritance: Man class inherits from Piece
class Man(Piece):                  
    def __init__(self, color):
        super().__init__(color)  # Man class inherits from Piece

    def __repr__(self):
        return f'{self.color[0].upper()}'

    def get_possible_moves(self, board, row, col):
        moves = []
        # White moves up, black moves down
        direction = -1 if self.color == 'white' else 1

        # Normal diagonal moves
        for dr, dc in [(direction, -1), (direction, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] is None:
                moves.append(((row, col), (new_row, new_col)))

        # Capture moves
        for dr, dc in [(direction, -1), (direction, 1)]:
            new_row, new_col = row + dr, col + dc
            jump_row, jump_col = row + 2 * dr, col + 2 * dc

            if (0 <= new_row < 8 and 0 <= new_col < 8 and
                board[new_row][new_col] is not None and
                board[new_row][new_col].color != self.color and
                0 <= jump_row < 8 and 0 <= jump_col < 8 and
                board[jump_row][jump_col] is None):
                moves.append(((row, col), (jump_row, jump_col)))
        return moves

#Inheritance: King class inherits from Piece
class King(Piece):               
    def __init__(self, color):
        super().__init__(color)
        self.is_king = True   # King-specific property set to True

    def __repr__(self):
        return f'{self.color[0].upper()}K'

    def get_possible_moves(self, board, row, col):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]    # Kings move in all diagonal directions

        for dr, dc in directions:
            for i in range(1, 8):             # Kings can move multiple steps
                new_row, new_col = row + i * dr, col + i * dc
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                if board[new_row][new_col] is None:
                    moves.append(((row, col), (new_row, new_col)))
                else:
                    # Capture logic if opponent piece is in the way
                    if board[new_row][new_col].color != self.color:
                        jump_row, jump_col = new_row + dr, new_col + dc
                        if (0 <= jump_row < 8 and 0 <= jump_col < 8 and
                            board[jump_row][jump_col] is None):
                            moves.append(((row, col), (jump_row, jump_col)))
                    break
        return moves


