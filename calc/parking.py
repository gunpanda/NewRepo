def calculate_materials(area_or_length, width=None, gravel_thickness_cm=None, sand_thickness_cm=None):
    """
    Рассчитывает объем щебня и песка для оформления площадки.

    Параметры:
    area_or_length (float): Площадь площадки (в квадратных метрах) или длина площадки (в метрах).
    width (float): Ширина площадки (в метрах), используется только при вводе длины.
    gravel_thickness_cm (float): Толщина слоя щебня (в сантиметрах).
    sand_thickness_cm (float): Толщина слоя песка (в сантиметрах).

    Возвращает:
    tuple: (объем щебня в кубометрах, масса щебня в тоннах, объем песка в кубометрах, масса песка в тоннах)
    """
    area = area_or_length if width is None else area_or_length * width
    gravel_volume = area * gravel_thickness_cm / 100  # переводим сантиметры в метры
    sand_volume = area * sand_thickness_cm / 100  # переводим сантиметры в метры

    # Предполагаем плотность щебня и песка (можно заменить на более точные значения)
    gravel_density = 1.5  # г/см³
    sand_density = 1.3  # г/см³

    gravel_mass = gravel_volume * gravel_density * 1000  # переводим в килограммы
    sand_mass = sand_volume * sand_density * 1000  # переводим в килограммы

    return gravel_volume, gravel_mass, sand_volume, sand_mass

# Пример использования
choice = input("Введите 'площадь' или 'длина': ").strip().lower()

if choice == 'площадь':
    area_input = float(input("Введите площадь площадки (в квадратных метрах): "))
    gravel_thickness_input = float(input("Введите толщину слоя щебня (в сантиметрах): "))
    sand_thickness_input = float(input("Введите толщину слоя песка (в сантиметрах): "))
    gravel_volume, gravel_mass, sand_volume, sand_mass = calculate_materials(area_input, gravel_thickness_cm=gravel_thickness_input, sand_thickness_cm=sand_thickness_input)
else:
    length_input = float(input("Введите длину площадки (в метрах): "))
    width_input = float(input("Введите ширину площадки (в метрах): "))
    gravel_thickness_input = float(input("Введите толщину слоя щебня (в сантиметрах): "))
    sand_thickness_input = float(input("Введите толщину слоя песка (в сантиметрах): "))
    gravel_volume, gravel_mass, sand_volume, sand_mass = calculate_materials(length_input, width=width_input, gravel_thickness_cm=gravel_thickness_input, sand_thickness_cm=sand_thickness_input)

print(f"Объем щебня: {gravel_volume:.2f} м³, Масса щебня: {gravel_mass:.2f} тонн")
print(f"Объем песка: {sand_volume:.2f} м³, Масса песка: {sand_mass:.2f} тонн")
