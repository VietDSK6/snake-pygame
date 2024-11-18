import pygame

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
    "Hard": 12,
    "Harder": 15,
    "Impossible": 25
}
