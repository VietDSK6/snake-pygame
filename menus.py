import sys
from config import *
from assets import *
from ui import Button


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
def death_menu(game_window, score):
    # Phát âm thanh thua cuộc
    death_sound.play()
    # Giảm âm lượng nhạc nền
    pygame.mixer.music.set_volume(0.3)

    # Tạo các nút cho menu thua cuộc
    buttons = [
        Button(FRAME_SIZE_X / 2 - 125, FRAME_SIZE_Y / 2, 250, 60, "Play Again", COLORS['success']),
        Button(FRAME_SIZE_X / 2 - 125, FRAME_SIZE_Y / 2 + 80, 250, 60, "Difficulty", COLORS['primary']),
        Button(FRAME_SIZE_X / 2 - 125, FRAME_SIZE_Y / 2 + 160, 250, 60, "Quit", COLORS['accent'])
    ]

    choice = show_menu(game_window, f"GAME OVER Score: {score}", buttons)

    # Khôi phục âm lượng nhạc nền nếu không thoát game
    if choice != "Quit":
        pygame.mixer.music.set_volume(0.5)

    return choice