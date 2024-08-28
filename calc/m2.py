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

def get_float_input(prompt):
    """
    Функция для получения числового ввода от пользователя с проверкой.
    
    Параметры:
    prompt (str): Сообщение для запроса ввода.
    
    Возвращает:
    float: Введенное пользователем число.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число.")

def calculate_total_area():
    """
    Функция для расчета общей площади всех стен.
    
    Возвращает:
    float: Общая площадь всех стен в квадратных метрах.
    """
    total_area = 0
    num_walls = int(get_float_input("Введите количество стен: "))
    for i in range(num_walls):
        length = get_float_input(f"Введите длину стены {i+1} в метрах: ")
        height = get_float_input(f"Введите высоту стены {i+1} в метрах: ")
        total_area += calculate_area(length, height)
    return total_area

def main():
    choice = input("Хотите ввести общую площадь стен (введите 'общая') или размеры каждой стены по очереди (введите 'по очереди')? ").strip().lower()
    
    if choice == 'общая':
        total_area = get_float_input("Введите общую площадь стен в квадратных метрах: ")
    elif choice == 'по очереди':
        total_area = calculate_total_area()
    else:
        print("Неверный выбор. Пожалуйста, введите 'общая' или 'по очереди'.")
        return
    
    print(f"Общая площадь стен: {total_area} квадратных метров")

if __name__ == "__main__":
    main()