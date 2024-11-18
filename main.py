# Import các module và dependency cần thiết
from game import *  # Import hằng số game, sprites và hàm tiện ích
from menus import *  # Import các thành phần và hàm của hệ thống menu


def game_loop(game_window, difficulty_name):

    # Khởi tạo cài đặt game dựa trên độ khó đã chọn
    difficulty = DIFFICULTIES[difficulty_name]
    game_state = init_game()
    fps_controller = pygame.time.Clock()

    while True:
        # Vòng lặp xử lý sự kiện
        for event in pygame.event.get():
            # Xử lý sự kiện đóng cửa sổ
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Xử lý sự kiện đầu vào bàn phím
            elif event.type == pygame.KEYDOWN:
                # Đặt hướng di chuyển dựa trên phím được nhấn (WASD hoặc phím mũi tên)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    game_state['change_to'] = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    game_state['change_to'] = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    game_state['change_to'] = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    game_state['change_to'] = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    return "Quit"

        # Cập nhật hướng rắn dựa trên đầu vào
        # Ngăn rắn quay đầu 180 độ
        if game_state['change_to'] == 'UP' and game_state['direction'] != 'DOWN':
            game_state['direction'] = 'UP'
        if game_state['change_to'] == 'DOWN' and game_state['direction'] != 'UP':
            game_state['direction'] = 'DOWN'
        if game_state['change_to'] == 'LEFT' and game_state['direction'] != 'RIGHT':
            game_state['direction'] = 'LEFT'
        if game_state['change_to'] == 'RIGHT' and game_state['direction'] != 'LEFT':
            game_state['direction'] = 'RIGHT'

        # Tính toán vị trí đầu mới dựa trên hướng hiện tại
        new_head_pos = list(game_state['snake_pos'])
        if game_state['direction'] == 'UP':
            new_head_pos[1] -= SPRITE_SIZE
        if game_state['direction'] == 'DOWN':
            new_head_pos[1] += SPRITE_SIZE
        if game_state['direction'] == 'LEFT':
            new_head_pos[0] -= SPRITE_SIZE
        if game_state['direction'] == 'RIGHT':
            new_head_pos[0] += SPRITE_SIZE

        # Cập nhật vị trí và các phần của rắn
        game_state['snake_pos'] = new_head_pos
        game_state['snake_segments'].insert(0, list(new_head_pos))
        game_state['segment_directions'].insert(0, game_state['direction'])

        # Tạo hình chữ nhật va chạm cho đầu rắn và thức ăn
        head_rect = pygame.Rect(game_state['snake_pos'][0], game_state['snake_pos'][1], SPRITE_SIZE, SPRITE_SIZE)
        food_rect = pygame.Rect(game_state['food_pos'][0], game_state['food_pos'][1], SPRITE_SIZE, SPRITE_SIZE)

        # Xử lý va chạm thức ăn và tăng trưởng của rắn
        if head_rect.colliderect(food_rect):
            eating_sound.play()  # Phát âm thanh ăn
            game_state['score'] += 1  # Tăng điểm
            # Tạo vị trí thức ăn mới
            game_state['food_pos'] = generate_food_position(game_state['snake_segments'])
        else:
            # Xóa phần đuôi nếu không ăn thức ăn
            game_state['snake_segments'].pop()
            game_state['segment_directions'].pop()

        # Bắt đầu vẽ các phần tử game
        # Xóa màn hình và vẽ nền
        game_window.fill(COLORS['background'])
        game_window.blit(background_img, (0, 0))

        # Vẽ các phần của rắn với hướng xoay thích hợp
        for i, pos in enumerate(game_state['snake_segments']):
            if i == 0:  # Vẽ đầu
                rotated_head = pygame.transform.rotate(snake_head,
                                                       get_rotation_angle(game_state['segment_directions'][i]))
                game_window.blit(rotated_head, tuple(pos))
            elif i == len(game_state['snake_segments']) - 1:  # Vẽ đuôi
                rotated_tail = pygame.transform.rotate(snake_tail,
                                                       get_rotation_angle(game_state['segment_directions'][i]))
                game_window.blit(rotated_tail, tuple(pos))
            else:  # Vẽ thân
                rotated_body = pygame.transform.rotate(snake_body,
                                                       get_rotation_angle(game_state['segment_directions'][i]))
                game_window.blit(rotated_body, tuple(pos))

        # Vẽ sprite thức ăn
        game_window.blit(food_img, tuple(game_state['food_pos']))

        # Kiểm tra va chạm tường (điều kiện game over)
        if (game_state['snake_pos'][0] < 0 or game_state['snake_pos'][0] > FRAME_SIZE_X - SPRITE_SIZE or
                game_state['snake_pos'][1] < 0 or game_state['snake_pos'][1] > FRAME_SIZE_Y - SPRITE_SIZE):
            return death_menu(game_window, game_state['score'], difficulty_name)

        # Kiểm tra tự va chạm (điều kiện game over)
        for block in game_state['snake_segments'][1:]:
            if block[0] == game_state['snake_pos'][0] and block[1] == game_state['snake_pos'][1]:
                return death_menu(game_window, game_state['score'], difficulty_name)

        # Cập nhật hiển thị điểm và làm mới màn hình
        show_score(game_window, game_state['score'], difficulty_name, 1, COLORS['text'], 24)
        pygame.display.update()
        fps_controller.tick(difficulty)  # Điều khiển tốc độ game dựa trên độ khó


def main():
    """
    Hàm chính khởi tạo game và xử lý vòng lặp game chính.
    Thiết lập hiển thị, âm thanh và quản lý chuyển đổi giữa các menu và gameplay.
    """
    # Khởi tạo cửa sổ game với cài đặt xác định
    game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))
    pygame.display.set_caption('Sizzle Sizzle')
    pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y),
                            pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)

    # Khởi tạo và bắt đầu nhạc nền
    pygame.mixer.music.set_volume(0.5)  # Đặt âm lượng 50%
    pygame.mixer.music.play(-1)  # Phát trong vòng lặp vô hạn

    difficulty = "Medium"  # Đặt độ khó mặc định

    # Vòng lặp chương trình chính
    while True:
        # Hiển thị menu chính và nhận lựa chọn người chơi
        choice = main_menu(game_window)
        if choice == "Quit":
            pygame.mixer.music.stop()  # Dừng nhạc trước khi thoát
            break

        # Xử lý chuyển đổi trạng thái game
        while choice == "Start Game" or choice == "Play Again" or choice == "Change Difficulty":
            # Hiển thị menu độ khó nếu bắt đầu game mới hoặc thay đổi độ khó
            if choice == "Start Game" or choice == "Change Difficulty":
                difficulty = difficulty_menu(game_window)

            # Bắt đầu vòng lặp game với độ khó đã chọn
            choice = game_loop(game_window, difficulty)
            if choice == "Quit":
                pygame.mixer.music.stop()  # Dừng nhạc trước khi thoát
                pygame.quit()
                sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()