import pygame
from config import FRAME_SIZE_X, FRAME_SIZE_Y, SPRITE_SIZE

def load_image(name, size1, size2):
    image = pygame.image.load(name)
    return pygame.transform.scale(image, (size1, size2))

# Tai tai nguyen cua game
snake_head = load_image('assets/images/snake-head.png', SPRITE_SIZE, SPRITE_SIZE)
snake_body = load_image('assets/images/snake-body.png', SPRITE_SIZE, SPRITE_SIZE)
snake_tail = load_image('assets/images/snake-tail.png', SPRITE_SIZE, SPRITE_SIZE)
food_img = load_image('assets/images/food.png', SPRITE_SIZE, SPRITE_SIZE)
background_img = load_image('assets/images/grass-background.png', FRAME_SIZE_X, FRAME_SIZE_Y)
logo = load_image('assets/images/logo.png', 1000, 400)
# Tai am thanh
eating_sound = pygame.mixer.Sound('assets/sounds/eat.wav')
death_sound = pygame.mixer.Sound('assets/sounds/die.wav')
pygame.mixer.music.load('assets/sounds/background.mp3')
