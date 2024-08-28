def calculate_area(length, height):
    """
    Функция для расчета площади стены.

    Параметры:
    length (float): Длина стены в метрах.
    height (float): Высота стены в метрах.

    Возвращает:
    float: Площадь стены в квадратных метрах.
    """
    return length * height

def calculate_total_area():
    """
    Функция для расчета общей площади всех стен.

    Возвращает:
    float: Общая площадь всех стен в квадратных метрах.
    """
    total_area = 0
    num_walls = int(input("Введите количество стен: "))
    for i in range(num_walls):
        length = float(input(f"Введите длину стены {i+1} в метрах: "))
        height = float(input(f"Введите высоту стены {i+1} в метрах: "))
        total_area += calculate_area(length, height)
    return total_area

def main():
    total_area = calculate_total_area()
    print(f"Общая площадь стен: {total_area} квадратных метров")

if __name__ == "__main__":
    main()
