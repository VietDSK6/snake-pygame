import pygame
import random
from config import *
from assets import *
from menus import *
from ui import Button, show_score


# Hàm lấy góc xoay cho sprite rắn dựa trên hướng di chuyển
def get_rotation_angle(direction):
    # Định nghĩa góc xoay tương ứng với mỗi hướng
    angles = {'RIGHT': 0, 'DOWN': 90, 'LEFT': 180, 'UP': -90}
    return angles.get(direction, 0)  # Trả về 0 nếu không tìm thấy hướng


# Hàm tạo vị trí ngẫu nhiên cho thức ăn
def generate_food_position(snake_segments):
    while True:
        # Tạo tọa độ ngẫu nhiên, đảm bảo thức ăn nằm trong lưới và căn chỉnh với kích thước sprite
        x = random.randrange(0, (FRAME_SIZE_X - SPRITE_SIZE), SPRITE_SIZE)
        y = random.randrange(0, (FRAME_SIZE_Y - SPRITE_SIZE), SPRITE_SIZE)
        food_pos = [x, y]

        # Đảm bảo thức ăn không xuất hiện trên thân rắn
        if food_pos not in snake_segments:
            return food_pos


# Hàm khởi tạo trạng thái ban đầu của game
def init_game():
    # Tạo vị trí ban đầu cho các đoạn thân rắn
    # Rắn bắt đầu với 3 đoạn, di chuyển sang phải
    initial_snake_segments = [
        [100, 50],  # Đầu rắn
        [100 - SPRITE_SIZE, 50],  # Đoạn thân thứ nhất
        [100 - (2 * SPRITE_SIZE), 50]  # Đoạn thân thứ hai
    ]

    # Trả về dictionary chứa trạng thái ban đầu của game
    return {
        'snake_pos': [100, 50],  # Vị trí đầu rắn
        'snake_segments': initial_snake_segments.copy(),  # Danh sách các đoạn thân
        'segment_directions': ['RIGHT', 'RIGHT', 'RIGHT'],  # Hướng của từng đoạn
        'food_pos': generate_food_position(initial_snake_segments),  # Vị trí thức ăn
        'direction': 'RIGHT',  # Hướng di chuyển hiện tại
        'change_to': 'RIGHT',  # Hướng sẽ thay đổi sang
        'score': 0  # Điểm số ban đầu
    }

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