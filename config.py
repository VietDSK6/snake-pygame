import pygame
import json
import os

# Thong so cua cua so
FRAME_SIZE_X = 1280
FRAME_SIZE_Y = 720
SPRITE_SIZE = 50

pygame.init()
pygame.mixer.init()

# Cac mau sac su dung trong game
COLORS = {
    'background': pygame.Color(16, 24, 32),
    'primary': pygame.Color(92, 131, 196),
    'secondary': pygame.Color(235, 248, 255),
    'accent': pygame.Color(255, 107, 107),
    'success': pygame.Color(75, 181, 67),
    'warning': pygame.Color(255, 186, 8),
    'text': pygame.Color(235, 248, 255)
}

# Font chu
FONTS = {
    'title': pygame.font.Font('assets/fonts/Roboto-Bold.ttf', 72),
    'header': pygame.font.Font('assets/fonts/Roboto-Bold.ttf', 48),
    'button': pygame.font.Font('assets/fonts/Roboto-Medium.ttf', 32),
    'score': pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 24)
}

# Do kho cua game
DIFFICULTIES = {
    "Easy": 7,
    "Medium": 10,
    "Hard": 15,
    "Harder": 20,
    "Impossible": 30
}

HIGH_SCORES_FILE = 'highscores.json'

def load_high_scores():
    """Load high scores from file or return default if not exists."""
    if not os.path.exists(HIGH_SCORES_FILE):
        return {}
    try:
        with open(HIGH_SCORES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_high_scores(high_scores):
    """Save high scores to file."""
    try:
        with open(HIGH_SCORES_FILE, 'w') as f:
            json.dump(high_scores, f)
    except IOError:
        print("Could not save high scores")

# Load high scores when config is imported
HIGH_SCORES = load_high_scores()
