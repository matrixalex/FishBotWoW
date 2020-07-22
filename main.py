import time
import pyautogui
from PIL import ImageGrab
import cv2
import numpy as np

fish_count = 0
max_fish_count = 300  # Ограничивающая переменная
threshold = 0.5  # Переменная, используемая для поиска поплавка на скриншоте игры
action_diff = 6  # Разность
x_correction = 15  # Коррекция по x для наведения на поплавок
y_correction = 25  # Коррекцияя по y для наведения на поплавок
fish_ability_x = 750  # Координаты навыка рыбалки по x на панели WoW (задать руками методом тыка)
fish_ability_y = 785  # Координаты навыка рыбалки по y на панели WoW (задать руками методом тыка)
window_rectangle = (0, 0, 1100, 800)  # Координаты прямоугольника окна, с него делается скриншот
focused = False
bobber_template_path = 'src/bobber1.jpg'  # Путь до файла шаблона поплавка
bobber_template = cv2.imread(bobber_template_path, 0)
w, h = bobber_template.shape[::-1]
# print(w, h)

for _ in range(max_fish_count):
    print('Fishing ' + str(fish_count))
    screen = ImageGrab.grab(bbox=window_rectangle)
    screen.save('screen.jpg')
    img = cv2.cvtColor(cv2.imread('screen.jpg'), cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img, bobber_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    max_find = np.max(res)
    # print(loc)
    # print('max', np.max(res))
    # print(res)

    if max_find > threshold:
        x, y = None, None
        zip_loc = zip(*loc[::-1])
        # print(zip_loc)
        for z_p in zip_loc:
            print(int(z_p[0]), int(z_p[1]))
            x, y = int(z_p[0]), int(z_p[1])
            break
        if x and y:
            action = False
            diff = 0
            current_mean = None
            # print('sreening bobber')
            time_count = 0
            while not action and time_count < 13:
                bobber_screen = ImageGrab.grab(bbox=(x, y, x + w, y + h))
                # bobber_screen.save('bobber.jpg')
                mean = np.mean(bobber_screen)
                if not current_mean:
                    current_mean = mean
                diff = abs(current_mean - mean)
                # Здесь отслеживаем показания которые принтуются в консоль, чтобы установить переменной
                # action_diff нужное вам значение
                print(diff)
                if diff > action_diff:
                    action = True
                time_count += 0.2
                # print(time_count)
                time.sleep(0.2)
            # print('diff', diff)
            if diff > action_diff:
                if not focused:
                    time.sleep(0.1)
                    pyautogui.moveTo(x - x_correction, y - y_correction)
                    pyautogui.mouseDown()
                    focused = True
                time.sleep(0.1)
                pyautogui.mouseUp()
                pyautogui.moveTo(x + x_correction, y + y_correction)
                time.sleep(0.3)
                pyautogui.mouseDown()
                time.sleep(0.3)
                pyautogui.mouseUp()
                time.sleep(0.2)
            current_mean = None
            x = None
            y = None
    # print('moving to fish_ability')
    pyautogui.moveTo(fish_ability_x, fish_ability_y)
    time.sleep(0.2)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()
    time.sleep(1)
    fish_count += 1
