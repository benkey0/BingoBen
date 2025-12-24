# Bingo Caller System

A Flask-based Bingo caller application with a clean, modern web interface.

## Features

- **Current Ball Display**: Shows the most recently drawn number
- **Drawn Numbers**: Displays all drawn numbers organized by bingo columns (B, I, N, G, O)
- **Draw Next Ball**: Randomly selects and displays the next number
- **Reset Game**: Clears all drawn numbers and starts fresh
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Run the Flask app:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

## Game Rules

- Numbers range from 1 to 90
- Each number can only be drawn once per game
- Numbers are organized and displayed by bingo ticket columns (9 columns):
  - **Column 1**: 1-9
  - **Column 2**: 10-19
  - **Column 3**: 20-29
  - **Column 4**: 30-39
  - **Column 5**: 40-49
  - **Column 6**: 50-59
  - **Column 7**: 60-69
  - **Column 8**: 70-79
  - **Column 9**: 80-90
- Game automatically prevents drawing when all numbers are exhausted

## Technical Details

- Built with Flask web framework
- Uses server-side sessions to maintain game state
- Responsive HTML/CSS with JavaScript for dynamic updates
- No database required - state stored in Flask sessions
