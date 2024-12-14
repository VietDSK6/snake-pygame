# Import các module cần thiết
from game import *  # Import hằng số game, sprites và hàm tiện ích
from menus import *  # Import các thành phần và hàm của hệ thống menu

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
        if choice[0] == "Quit":
            pygame.mixer.music.stop()  # Dừng nhạc trước khi thoát
            break

        # Xử lý chuyển đổi trạng thái game
        while choice[0] == "Start Game" or choice[0] == "Play Again" or choice[0] == "Change Difficulty":
            # Hiển thị menu độ khó nếu bắt đầu game mới hoặc thay đổi độ khó
            if choice[0] == "Start Game" or choice[0] == "Change Difficulty":
                difficulty = difficulty_menu(game_window)

            # Bắt đầu vòng lặp game với độ khó đã chọn
            choice = game_loop(game_window, difficulty, choice[1])
            if choice == "Quit":
                pygame.mixer.music.stop()  # Dừng nhạc trước khi thoát
                pygame.quit()
                sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()