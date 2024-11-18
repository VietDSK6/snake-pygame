import pygame
import random
from config import *
from assets import *
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