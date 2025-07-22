from flask import Flask, request, jsonify
from flask_cors import CORS
from src.models.Match import Match

app = Flask(__name__)
CORS(app)

# Global game instance
game_match = Match()
game_match.start_game()

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

@app.route('/board', methods=['GET'])
def get_board():
    """Get current board state"""
    board_state = []
    for row in range(8):
        row_data = []
        for col in range(8):
            piece = game_match.board.get_piece(row, col)
            if piece:
                row_data.append({
                    'color': piece.color,
                    'is_king': piece.is_king,
                    'position': position_to_chess(row, col)
                })
            else:
                row_data.append(None)
        board_state.append(row_data)
    
    return jsonify({
        'board': board_state,
        'current_player': game_match.get_current_player_color(),
        'game_over': game_match.is_game_over(),
        'winner': game_match.get_winner()
    })

@app.route('/move', methods=['POST'])
def make_move():
    """Make a move"""
    data = request.get_json()
    
    if not data or 'player' not in data or 'from' not in data or 'to' not in data:
        return jsonify({'error': 'Missing required fields: player, from, to'}), 400
    
    player = data['player']
    from_pos = data['from']
    to_pos = data['to']
    
    # Validate player turn
    if player != game_match.get_current_player_color():
        return jsonify({'error': f'Not {player}\'s turn'}), 400
    
    # Parse positions
    from_row, from_col = parse_position(from_pos)
    to_row, to_col = parse_position(to_pos)
    
    if from_row is None or to_row is None:
        return jsonify({'error': 'Invalid position format. Use A1-H8'}), 400
    
    # Make the move
    if game_match.make_move(from_row, from_col, to_row, to_col):
        return jsonify({
            'success': True,
            'message': f'Move made: {from_pos} -> {to_pos}',
            'current_player': game_match.get_current_player_color(),
            'game_over': game_match.is_game_over(),
            'winner': game_match.get_winner()
        })
    else:
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/info', methods=['GET'])
def get_piece_info():
    """Get information about a piece at a specific position"""
    player = request.args.get('player')
    piece_pos = request.args.get('piece')
    
    if not piece_pos:
        return jsonify({'error': 'Missing piece position parameter'}), 400
    
    row, col = parse_position(piece_pos)
    if row is None:
        return jsonify({'error': 'Invalid position format. Use A1-H8'}), 400
    
    piece = game_match.board.get_piece(row, col)
    if not piece:
        return jsonify({'error': f'No piece at position {piece_pos}'}), 404
    
    # Get possible moves
    moves = game_match.get_possible_moves_for_piece(row, col)
    move_positions = [position_to_chess(move[1][0], move[1][1]) for move in moves]
    
    return jsonify({
        'position': piece_pos,
        'color': piece.color,
        'is_king': piece.is_king,
        'possible_moves': move_positions
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game"""
    global game_match
    game_match = Match()
    game_match.start_game()
    
    return jsonify({
        'message': 'Game reset successfully',
        'current_player': game_match.get_current_player_color()
    })

@app.route('/', methods=['GET'])
def home():
    """API documentation"""
    return jsonify({
        'message': 'Checkers Game API',
        'endpoints': {
            'GET /board': 'Get current board state',
            'POST /move': 'Make a move (JSON: {player, from, to})',
            'GET /info': 'Get piece info (params: ?player=Black&piece=2A)',
            'POST /reset': 'Reset the game'
        },
        'example_move': {
            'player': 'Black',
            'from': '2A',
            'to': '3B'
        }
    })

if __name__ == '__main__':
    print("Starting Checkers API Server...")
    print("API Documentation available at: http://localhost:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)

