from flask import Flask, render_template, session, redirect, url_for, jsonify
import random

app = Flask(__name__)
app.secret_key = 'bingo_secret_key_2024'  # Change this in production

# Traditional bingo calls mapping
BINGO_CALLS = {
    1: "Kelly's eye",
    2: "One little duck",
    3: "Cup of tea",
    4: "Knock at the door",
    5: "Man alive",
    6: "Half a dozen",
    7: "Lucky seven",
    8: "Garden gate",
    9: "Doctor's orders",
    10: "Cock and hen",
    11: "Legs eleven",
    12: "One dozen",
    13: "Unlucky for some",
    14: "Valentine's Day",
    15: "Young and keen",
    16: "Sweet sixteen",
    17: "Dancing queen",
    18: "Coming of age",
    19: "Goodbye teens",
    20: "One score",
    21: "Key of the door",
    22: "Two little ducks",
    23: "Thee and me",
    24: "Two dozen",
    25: "Duck and dive",
    26: "Pick and mix",
    27: "Gateway to heaven",
    28: "In a state",
    29: "Rise and shine",
    30: "Dirty Gertie",
    31: "Get up and run",
    32: "Buckle my shoe",
    33: "All the threes",
    34: "Ask for more",
    35: "Jump and jive",
    36: "Three dozen",
    37: "More than eleven",
    38: "Christmas cake",
    39: "Steps",
    40: "Life begins",
    41: "Time for fun",
    42: "Winnie the Pooh",
    43: "Down on your knees",
    44: "Droopy drawers",
    45: "Halfway there",
    46: "Up to tricks",
    47: "Four and seven",
    48: "Four dozen",
    49: "PC",
    50: "Half a century",
    51: "Tweak of the thumb",
    52: "Chicken vindaloo",
    53: "Here comes Herbie",
    54: "Clean the floor",
    55: "Snakes alive",
    56: "Was she worth it",
    57: "Heinz varieties",
    58: "Make them wait",
    59: "Brighton line",
    60: "Five dozen",
    61: "Bakers bun",
    62: "Tickety-boo",
    63: "Tickle me",
    64: "Red raw",
    65: "Old age pension",
    66: "Clickety click",
    67: "Stairway to heaven",
    68: "Saving grace",
    69: "Either way up",
    70: "Three score and ten",
    71: "Bang on the drum",
    72: "Six dozen",
    73: "Queen bee",
    74: "Candy store",
    75: "Strive and strive",
    76: "Trombones",
    77: "Sunset strip",
    78: "Heaven's gate",
    79: "One more time",
    80: "Eight and blank",
    81: "Stop and run",
    82: "Straight on through",
    83: "Time for tea",
    84: "Seven dozen",
    85: "Staying alive",
    86: "Between the sticks",
    87: "Torquay in Devon",
    88: "Two fat ladies",
    89: "Nearly there",
    90: "Top of the shop"
}

def get_bingo_call(number):
    """Return the traditional bingo call for a number"""
    return BINGO_CALLS.get(number, None)

class BingoGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.drawn_numbers = []
        self.available_numbers = list(range(1, 91))  # 1-90
        self.current_ball = None
        self.previous_ball = None

    def draw_next_ball(self):
        if not self.available_numbers:
            return None  # All numbers drawn

        # Store current ball as previous before drawing new one
        self.previous_ball = self.current_ball
        
        self.current_ball = random.choice(self.available_numbers)
        self.available_numbers.remove(self.current_ball)
        self.drawn_numbers.append(self.current_ball)
        return self.current_ball

    def get_drawn_by_column(self):
        """Return drawn numbers organized by bingo ticket columns (9 columns)"""
        columns = {
            '1': [],   # 1-9
            '2': [],   # 10-19
            '3': [],   # 20-29
            '4': [],   # 30-39
            '5': [],   # 40-49
            '6': [],   # 50-59
            '7': [],   # 60-69
            '8': [],   # 70-79
            '9': []    # 80-90
        }

        for number in sorted(self.drawn_numbers):
            if 1 <= number <= 9:
                columns['1'].append(number)
            elif 10 <= number <= 19:
                columns['2'].append(number)
            elif 20 <= number <= 29:
                columns['3'].append(number)
            elif 30 <= number <= 39:
                columns['4'].append(number)
            elif 40 <= number <= 49:
                columns['5'].append(number)
            elif 50 <= number <= 59:
                columns['6'].append(number)
            elif 60 <= number <= 69:
                columns['7'].append(number)
            elif 70 <= number <= 79:
                columns['8'].append(number)
            elif 80 <= number <= 90:
                columns['9'].append(number)

        return columns

def get_game():
    """Get or create game from session"""
    if 'game_data' not in session:
        game = BingoGame()
        session['game_data'] = {
            'drawn_numbers': game.drawn_numbers,
            'available_numbers': game.available_numbers,
            'current_ball': game.current_ball,
            'previous_ball': game.previous_ball
        }
    else:
        game = BingoGame()
        game.drawn_numbers = session['game_data']['drawn_numbers']
        game.available_numbers = session['game_data']['available_numbers']
        game.current_ball = session['game_data']['current_ball']
        game.previous_ball = session['game_data'].get('previous_ball', None)
    return game

def save_game(game):
    """Save game state to session"""
    session['game_data'] = {
        'drawn_numbers': game.drawn_numbers,
        'available_numbers': game.available_numbers,
        'current_ball': game.current_ball,
        'previous_ball': game.previous_ball
    }

@app.route('/')
def index():
    game = get_game()
    current_call = get_bingo_call(game.current_ball) if game.current_ball else None
    return render_template('caller.html',
                         current_ball=game.current_ball,
                         current_call=current_call,
                         previous_ball=game.previous_ball,
                         drawn_columns=game.get_drawn_by_column(),
                         remaining_count=len(game.available_numbers))

@app.route('/draw')
def draw_ball():
    game = get_game()
    ball = game.draw_next_ball()
    save_game(game)

    if ball is None:
        return jsonify({'error': 'All numbers have been drawn!'})

    return jsonify({
        'ball': ball,
        'call': get_bingo_call(ball),
        'previous_ball': game.previous_ball,
        'remaining': len(game.available_numbers),
        'drawn_columns': game.get_drawn_by_column()
    })

@app.route('/reset')
def reset_game():
    game = BingoGame()
    save_game(game)
    return jsonify({
        'current_ball': game.current_ball,
        'previous_ball': game.previous_ball,
        'drawn_columns': game.get_drawn_by_column(),
        'remaining': len(game.available_numbers)
    })

if __name__ == '__main__':
    app.run(debug=True)
