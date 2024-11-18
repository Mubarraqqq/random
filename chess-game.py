# My Simple Chess Capture Game

MAX_PIECES = 16

# Initialize an 8x8 board
def initialize_board():
    """Create an empty 8x8 chess board."""
    return [[" " for _ in range(8)] for _ in range(8)]

def place_piece(board, piece, position, color):
    """Place a piece on the board at the specified position."""
    x, y = get_position(position)
    
    # replace the text with the piece icon
    try:
        if color.lower() == 'white':
            symbols = {
                "rook": "♖",
                "knight": "♘",
                "bishop": "♗",
                "queen": "♕",
                "king": "♔",
                "pawn": "♙"
            }
        elif color.lower() == 'black':
            symbols = {
                "rook": "♜",
                "knight": "♞",
                "bishop": "♝",
                "queen": "♛",
                "king": "♚",
                "pawn": "♟︎"
            }
    
        board[7 - y][x] = symbols[piece.lower()]  # Flip the row to make (0,0) the bottom-left corner
    except KeyError as e:
            print(f"Error: {e} not found. Please check your spelling.\n")

def print_board(board):
    """Display the chess board in a visually appealing format."""
    print("   a   b   c   d   e   f   g   h")
    print(" +---+---+---+---+---+---+---+---+")
    for row in range(8):
        print(f"{8 - row}|", end="")  # Print row numbers on the left
        for col in range(8):
            print(f" {board[row][col]} |", end="")
        print(f" {8 - row}")  # Print row numbers on the right
        print(" +---+---+---+---+---+---+---+---+")
    print("   a   b   c   d   e   f   g   h\n")

# starting the board:
board_state = initialize_board()

def get_position(input_str):
    """Convert chess position (e.g., 'a5') to board coordinates."""
    column, row = input_str[0], input_str[1]
    x = ord(column) - ord('a')  # Convert column to a number (0-7)
    y = int(row) - 1            # Convert row to a number (0-7)
    return x, y

def is_position_valid(position):
    """Check if the position is within the chess board limits."""
    return 0 <= position[0] < 8 and 0 <= position[1] < 8

def is_path_clear(board, start, end):
    """Check if there are no pieces in the path between start and end positions for non-knight pieces."""
    x1, y1 = start
    x2, y2 = end

    dx = (x2 - x1) // max(1, abs(x2 - x1)) if x1 != x2 else 0
    dy = (y2 - y1) // max(1, abs(y2 - y1)) if y1 != y2 else 0

    # Step along the path until just before the end position
    x, y = x1 + dx, y1 + dy
    while (x, y) != (x2, y2):
        if board[7 - y][x] != " ":
            return False
        x += dx
        y += dy

    return True

def can_capture(white_piece, white_pos, black_piece, black_pos):
    """Determine if the white piece can capture a black piece based on movement rules."""
    wx, wy = get_position(white_pos)
    bx, by = get_position(black_pos)

    if white_piece == "rook":
        # Rook moves in straight lines along rows or columns
        return (wx == bx or wy == by) and is_path_clear(board_state, (wx, wy), (bx, by))

    elif white_piece == "knight":
        # Knight moves in an L-shape: 2 squares in one direction and 1 in the perpendicular direction
        return (abs(wx - bx), abs(wy - by)) in [(2, 1), (1, 2)]

    elif white_piece == "bishop":
        # Bishop moves diagonally: same difference in x and y coordinates
        return abs(wx - bx) == abs(wy - by) and is_path_clear(board_state, (wx, wy), (bx, by))

    elif white_piece == "queen":
        # Queen moves like both a rook and a bishop
        return (wx == bx or wy == by or abs(wx - bx) == abs(wy - by)) and is_path_clear(board_state, (wx, wy), (bx, by))

    elif white_piece == "king":
        # King moves one square in any direction
        return max(abs(wx - bx), abs(wy - by)) == 1

    elif white_piece == "pawn":
        # Pawns capture one square diagonally forward (assuming white pawns moving up)
        return (bx == wx + 1) and (by == wy + 1 or by == wy - 1)

    return False

def add_piece(piece, position, pieces, color):
    """Add a piece to the list if it's in a valid position."""
    
    if len(pieces) >= MAX_PIECES:
        print(f"Cannot add more than {MAX_PIECES} pieces for {color} pieces.")
        return False

    if not is_position_valid(get_position(position)):
        print(f"Invalid position for {piece} at {position}.")
        return False
    
    if piece.lower() not in ['rook', 'knight', 'pawn', 'bishop', 'king', 'queen']:
        print(f"Invalid piece: {piece}")
        return False

    pieces.append((piece, position))
    place_piece(board_state, piece, position, color)
    print_board(board_state)
    return True

def input_white_piece():
    """Prompt the user to enter the white piece with its position."""
    pieces = []
    while True:
        white_input = input("Enter the white piece and its position (e.g., 'rook a1'): ").strip().lower()
        if white_input == "done":
            if len(pieces) > 0:
                print_board(board_state)
                break
            else:
                print("You must add at least one white piece.")
                continue
        try:
            
            piece, position = white_input.split()          
            if add_piece(piece, position, pieces, color="white"):
                print(f"White {piece} added at {position}.")
                        
            # if piece not in ["rook", "knight"]:
            #     raise ValueError("Only 'rook' and 'knight' are supported as white pieces.")
            
        except ValueError as e:
            print(f"Error: {e}. Please try again.")
    return piece, position

def input_black_pieces():
    """Prompt the user to enter black pieces one by one."""
    pieces = []
    print("Enter the black pieces and their positions (e.g., 'pawn b7'). Type 'done' when finished.")
    while True:
        black_input = input("Enter black piece: ").strip().lower()
        if black_input == "done":
            if len(pieces) > 0:
                print_board(board_state)
                break
            else:
                print("You must add at least one black piece.")
                continue
        try:
            piece, position = black_input.split()
            if add_piece(piece, position, pieces, color="black"):
                print(f"Black {piece} added at {position}.")
            
        except ValueError:
            print("Invalid format. Use 'piece position' format, like 'pawn e4'.")
    return pieces

def display_capture_options(white_piece, white_pos, black_pieces):
    """Display the black pieces that can be captured by the white piece."""
    captures = []
    for black_piece, black_pos in black_pieces:
        if can_capture(white_piece, white_pos, black_piece, black_pos):
            captures.append((black_piece, black_pos))
    
    if captures:
        print(f"The white {white_piece} at {white_pos} can capture the following black pieces:")
        for piece, position in captures:
            print(f"Black {piece} at {position}")
    else:
        print(f"The white {white_piece} at {white_pos} cannot capture any black pieces.")

def start_game():
    """Start the chess game and execute the main loop."""
    print("Welcome to Chess Capture Game!")
    white_piece, white_pos = input_white_piece()
    black_pieces = input_black_pieces()
    display_capture_options(white_piece, white_pos, black_pieces)

# Run the game
if __name__ == "__main__":
    print_board(board_state)
    start_game()
    
    
