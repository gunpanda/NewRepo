import cv2
import numpy as np
from mss import mss

# Установим область захвата экрана
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
sct = mss()

# Инициализация для вычитания фона
background_subtractor = cv2.createBackgroundSubtractorMOG2()

while True:
    # Захватываем скриншот
    screenshot = np.array(sct.grab(monitor))
    frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    # Применяем вычитание фона
    fg_mask = background_subtractor.apply(frame)

    # Убираем шумы с помощью морфологических операций
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

    # Поиск контуров движения
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Минимальный размер объекта
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Красный прямоугольник

    # Отображение
    cv2.imshow("Screen", frame)
    cv2.imshow("Foreground Mask", fg_mask)

    # Выход по нажатию ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
