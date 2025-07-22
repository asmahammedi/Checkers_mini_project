from .Board import Board
from .Player import Player
from .Piece import Man, King

class Match:
    def __init__(self):
        self.board = Board()
        self.player1 = Player("white")
        self.player2 = Player("black")
        self.current_player = self.player2
        self.game_over = False
        self.winner = None

    def start_game(self):
        self.board.initialize_board()
        self.update_players_pieces()

    def update_players_pieces(self):
        self.player1.pieces = []
        self.player2.pieces = []
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece:
                    if piece.color == self.player1.color:
                        self.player1.add_piece(piece)
                    else:
                        self.player2.add_piece(piece)

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def check_game_over(self):
        if not self.player1.has_pieces():
            self.game_over = True
            self.winner = self.player2
        elif not self.player2.has_pieces():
            self.game_over = True
            self.winner = self.player1
        elif not self.current_player.get_all_possible_moves(self.board):
            self.game_over = True
            self.winner = self.player2 if self.current_player == self.player1 else self.player1

    def make_move(self, from_row, from_col, to_row, to_col):
        piece = self.board.get_piece(from_row, from_col)
        if piece is None or piece.color != self.current_player.color:
            return False

        if self.board.move_piece(from_row, from_col, to_row, to_col):
            self.update_players_pieces()
            self.check_game_over()
            if not self.game_over:
                self.switch_player()
            return True
        return False

    def get_board_state(self):
        state = []
        for r in range(8):
            row_state = []
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece:
                    row_state.append(f"{piece.color[0]}{'K' if piece.is_king else ''}")
                else:
                    row_state.append(None)
            state.append(row_state)
        return state

    def get_possible_moves_for_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.current_player.color:
            return piece.get_possible_moves(self.board.board, row, col)
        return []

    def get_current_player_color(self):
        return self.current_player.color

    def get_winner(self):
        return self.winner.color if self.winner else None

    def is_game_over(self):
        return self.game_over
