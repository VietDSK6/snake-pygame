import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color or self.lighten_color(color)
        self.current_color = self.color
        self.is_hovered = False

    def lighten_color(self, color):
        r = min(int(color.r * 1.2), 255)
        g = min(int(color.g * 1.2), 255)
        b = min(int(color.b * 1.2), 255)
        return pygame.Color(r, g, b)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.color

        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        text_surface = FONTS['button'].render(self.text, True, COLORS['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def show_score(surface, score, difficulty, choice, color, size):
    score_surface = FONTS['score'].render(f'Score: {score} | Difficulty: {difficulty}', True, color)
    score_rect = score_surface.get_rect()

    padding = 10
    bg_rect = pygame.Rect(
        score_rect.x - padding,
        15 if choice == 1 else FRAME_SIZE_Y / 1.25,
        score_rect.width + padding * 2,
        score_rect.height + padding * 2
    )

    if choice == 1:
        score_rect.midtop = (FRAME_SIZE_X / 2, 20)
        bg_rect.midtop = (FRAME_SIZE_X / 2, 15)
    else:
        score_rect.midtop = (FRAME_SIZE_X / 2, FRAME_SIZE_Y / 1.25)
        bg_rect.midtop = (FRAME_SIZE_X / 2, FRAME_SIZE_Y / 1.25 - 5)

    s = pygame.Surface((bg_rect.width, bg_rect.height))
    s.set_alpha(128)
    s.fill(COLORS['background'])
    surface.blit(s, bg_rect)
    surface.blit(score_surface, score_rect)
