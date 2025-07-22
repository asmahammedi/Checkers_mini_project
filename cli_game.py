import sys
from src.models.Match import Match

def parse_position(pos_str):
    """Convert chess notation (e.g., 'A1') to row, col coordinates"""
    if len(pos_str) != 2:
        return None, None
    col_char = pos_str[0].upper()
    row_char = pos_str[1]
    
    if col_char not in 'ABCDEFGH' or row_char not in '12345678':
        return None, None
    
    col = ord(col_char) - ord('A')
    row = 8 - int(row_char)  # Convert to 0-based index from top
    
    return row, col

def position_to_chess(row, col):
    """Convert row, col coordinates to chess notation"""
    col_char = chr(ord('A') + col)
    row_char = str(8 - row)
    return col_char + row_char

def display_help():
    print("\n=== COMMANDS ===")
    print("1 - Move a piece")
    print("2 - Show piece details")
    print("3 - Show current board")
    print("4 - Leave the game")
    print("Help - Display this help")
    print("\nMove format: A1-H8 (ex: A1, B2, etc.)")
    print("===============================\n")

def main():
    print("=== CHECKERS ===")
    print("Welcome To Checkers!")
    display_help()
    
    match = Match()
    match.start_game()
    
    while not match.is_game_over():
        print(f"\nPlayer's turn: {match.get_current_player_color()}")
        match.board.display()
        
        print("\nWhat would you like to do?")
        choice = input("Your Choice: ").strip()
        
        if choice == "1":
            print("Piece Movement")
            from_pos = input("Start position (ex: A1): ").strip()
            to_pos = input("End position (ex: B2): ").strip()
            
            from_row, from_col = parse_position(from_pos)
            to_row, to_col = parse_position(to_pos)
            
            if from_row is None or to_row is None:
                print("Invalid Position! Use format A1-H8")
                continue
            
            if match.make_move(from_row, from_col, to_row, to_col):
                print(f"movement done: {from_pos} -> {to_pos}")
            else:
                print("Invalid Movement!")
                
        elif choice == "2":
            pos = input("Piece position (ex: A1): ").strip()
            row, col = parse_position(pos)
            
            if row is None:
                print("Invalid Movement!")
                continue
                
            piece = match.board.get_piece(row, col)
            if piece:
                print(f"Piece in {pos}: {piece.color} {'(King)' if piece.is_king else '(Man)'}")
                moves = match.get_possible_moves_for_piece(row, col)
                if moves:
                    print("Possible Movements:")
                    for move in moves:
                        _, (t_row, t_col) = move
                        print(f"  -> {position_to_chess(t_row, t_col)}")
                else:
                    print("No movements available for this piece.")
            else:
                print(f"No piece in {pos}")
                
        elif choice == "3":
            print("\nCurrent board:")
            match.board.display()
            
        elif choice == "4":
            print("Ciao!")
            sys.exit()
            
        elif choice.lower() == "Help":
            display_help()
            
        else:
            print("Invalid choice! Select Help for help.")
    
    print(f"\n=== END OF GAME ===")
    print(f"Winner: {match.get_winner()}")
    match.board.display()

if __name__ == "__main__":
    main()

