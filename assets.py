import pygame
from config import FRAME_SIZE_X, FRAME_SIZE_Y, SPRITE_SIZE, SNAKE_COLORS

def load_image(name, size1, size2):
    image = pygame.image.load(name)
    return pygame.transform.scale(image, (size1, size2))

# Tai tai nguyen cua game
green_snake_head = load_image('assets/images/green/snake-head.png', SPRITE_SIZE, SPRITE_SIZE)
green_snake_body = load_image('assets/images/green/snake-body.png', SPRITE_SIZE, SPRITE_SIZE)
green_snake_tail = load_image('assets/images/green/snake-tail.png', SPRITE_SIZE, SPRITE_SIZE)

red_snake_head = load_image('assets/images/red/snake-head.png', SPRITE_SIZE, SPRITE_SIZE)
red_snake_body = load_image('assets/images/red/snake-body.png', SPRITE_SIZE, SPRITE_SIZE)
red_snake_tail = load_image('assets/images/red/snake-tail.png', SPRITE_SIZE, SPRITE_SIZE)

blue_snake_head = load_image('assets/images/blue/snake-head.png', SPRITE_SIZE, SPRITE_SIZE)
blue_snake_body = load_image('assets/images/blue/snake-body.png', SPRITE_SIZE, SPRITE_SIZE)
blue_snake_tail = load_image('assets/images/blue/snake-tail.png', SPRITE_SIZE, SPRITE_SIZE)

SNAKE_COLORS['Green'] = {
    'head': green_snake_head,
    'body': green_snake_body,
    'tail': green_snake_tail
}

SNAKE_COLORS['Red'] = {
    'head': red_snake_head,
    'body': red_snake_body,
    'tail': red_snake_tail
}

SNAKE_COLORS['Blue'] = {
    'head': blue_snake_head,
    'body': blue_snake_body,
    'tail': blue_snake_tail
}
food_img = load_image('assets/images/food.png', SPRITE_SIZE, SPRITE_SIZE)
background_img = load_image('assets/images/grass-background.png', FRAME_SIZE_X, FRAME_SIZE_Y)
logo = load_image('assets/images/logo.png', 1000, 400)
# Tai am thanh

eating_sound = pygame.mixer.Sound('assets/sounds/eat.wav')
death_sound = pygame.mixer.Sound('assets/sounds/die.wav')
pygame.mixer.music.load('assets/sounds/background.mp3')
