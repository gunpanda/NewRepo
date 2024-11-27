import os

def save_directory_structure_to_txt(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(directory):
            # Записываем путь текущей директории
            f.write(f"Directory: {root}\n")
            # Записываем все папки в текущей директории
            if dirs:
                f.write(" Subdirectories:\n")
                for dir_name in dirs:
                    f.write(f"  - {dir_name}\n")
            # Записываем все файлы в текущей директории
            if files:
                f.write(" Files:\n")
                for file_name in files:
                    f.write(f"  - {file_name}\n")
            f.write("\n")  # Добавляем пустую строку для разделения

# Укажите путь к папке и выходной файл
directory_path = r'C:\code\sprit for games'
output_file_path = r'C:\code\sprit for games\\structure.txt'

# Вызов функции для сохранения структуры папок и файлов
save_directory_structure_to_txt(directory_path, output_file_path)

print(f"Структура папок и файлов сохранена в {output_file_path}")
