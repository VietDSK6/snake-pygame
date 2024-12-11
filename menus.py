import sys
from config import *
from assets import *
from ui import Button, InputBox

# Hàm hiển thị menu chung cho tất cả các màn hình
def show_menu(game_window, text, buttons, logo_img=None):
    while True:
        # Xóa màn hình và vẽ hình nền
        game_window.fill(COLORS['background'])
        game_window.blit(background_img, (0, 0))

        if logo_img:
            # Tính toán vị trí để căn giữa logo
            logo_rect = logo_img.get_rect(center=(FRAME_SIZE_X / 2, FRAME_SIZE_Y / 4))
            game_window.blit(logo_img, logo_rect)
        else:
            # Nếu không có logo, hiển thị văn bản thay thế
            font = pygame.font.SysFont('jetbrain', 64)
            text_surface = font.render(text, True, COLORS['text'])
            text_rect = text_surface.get_rect(center=(FRAME_SIZE_X / 2, FRAME_SIZE_Y / 4))
            game_window.blit(text_surface, text_rect)

        # Vẽ tất cả các nút trong menu
        for button in buttons:
            button.draw(game_window)

        # Cập nhật màn hình
        pygame.display.flip()

        # Xử lý các sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra xem người chơi có nhấn vào nút nào không
                for button in buttons:
                    if button.is_clicked(event.pos):
                        return button.text
            if event.type == pygame.KEYDOWN:
                # Thoát game khi nhấn ESC
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()


# Menu chọn độ khó
def difficulty_menu(game_window):
    # Thiết lập kích thước và khoảng cách giữa các nút
    button_width = 250
    button_height = 60
    button_spacing = 20
    total_height = (button_height + button_spacing) * len(DIFFICULTIES)
    start_y = (FRAME_SIZE_Y - total_height) // 1.5

    # Tạo danh sách các nút độ khó
    buttons = []
    for i, difficulty in enumerate(DIFFICULTIES.keys()):
        y = start_y + i * (button_height + button_spacing)
        # Nút "Medium" có màu khác biệt
        color = COLORS['primary'] if difficulty == "Medium" else COLORS['success']
        buttons.append(Button(
            FRAME_SIZE_X / 2 - button_width / 2,
            y,
            button_width,
            button_height,
            difficulty,
            color
        ))

    return show_menu(game_window, "SELECT DIFFICULTY", buttons)


# Menu chính của game
def main_menu(game_window):
    # Tạo hai nút: Start Game và Quit
    buttons = [
        Button(FRAME_SIZE_X / 2 - 125, FRAME_SIZE_Y / 2, 250, 60, "Start Game", COLORS['success']),
        Button(FRAME_SIZE_X / 2 - 125, FRAME_SIZE_Y / 2 + 80, 250, 60, "Quit", COLORS['accent'])
    ]
    return show_menu(game_window, "Sizzle Sizzle", buttons, logo)


# Menu hiển thị khi người chơi thua
def name_input_menu(game_window):
    """Menu for entering player name."""
    input_box = InputBox(
        FRAME_SIZE_X / 2 - 200,
        FRAME_SIZE_Y / 2,
        400, 50
    )

    while True:
        game_window.fill(COLORS['background'])
        game_window.blit(background_img, (0, 0))

        # Render title
        title_font = pygame.font.SysFont('jetbrain', 48)
        title_text = title_font.render("Enter Your Name", True, COLORS['text'])
        title_rect = title_text.get_rect(center=(FRAME_SIZE_X / 2, FRAME_SIZE_Y / 4))
        game_window.blit(title_text, title_rect)

        # Draw input box
        input_box.draw(game_window)

        # Create submit button
        submit_button = Button(
            FRAME_SIZE_X / 2 - 125,
            FRAME_SIZE_Y / 2 + 100,
            250, 60,
            "Submit",
            COLORS['success']
        )
        submit_button.draw(game_window)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If enter is pressed while input box is active
            if input_box.handle_event(event):
                # Validate name
                name = input_box.text.strip()
                if name and len(name) <= 10:
                    return name

            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.is_clicked(event.pos):
                    # Validate name
                    name = input_box.text.strip()
                    if name and len(name) <= 10:
                        return name

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

def death_menu(game_window, score):
    death_sound.play()
    pygame.mixer.music.set_volume(0.3)

    # Update high score
    difficulty = "Medium"  # You might want to pass actual difficulty
    player_name = name_input_menu(game_window)

    if player_name:
        # Update high scores
        if difficulty not in HIGH_SCORES:
            HIGH_SCORES[difficulty] = []

        HIGH_SCORES[difficulty].append({
            'name': player_name,
            'score': score
        })

        # Sort and keep top 5 scores
        HIGH_SCORES[difficulty] = sorted(
            HIGH_SCORES[difficulty],
            key=lambda x: x['score'],
            reverse=True
        )[:5]

        save_high_scores(HIGH_SCORES)

    buttons = [
        Button(FRAME_SIZE_X / 2 - 125, FRAME_SIZE_Y / 2, 250, 60, "Play Again", COLORS['success']),
        Button(FRAME_SIZE_X / 2 - 125, FRAME_SIZE_Y / 2 + 80, 250, 60, "Difficulty", COLORS['primary']),
        Button(FRAME_SIZE_X / 2 - 125, FRAME_SIZE_Y / 2 + 160, 250, 60, "Quit", COLORS['accent'])
    ]

    choice = show_menu(game_window, f"GAME OVER Score: {score}", buttons)

    if choice != "Quit":
        pygame.mixer.music.set_volume(0.5)

    return choice