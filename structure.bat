@echo off

:: Создание основной директории проекта
mkdir tetris_game\assets
mkdir tetris_game\src

:: Создание пустых файлов в директории /assets
echo {} > tetris_game\assets\colors.json

:: Создание файлов в директории /src
type nul > tetris_game\src\__init__.py
type nul > tetris_game\src\main.py
type nul > tetris_game\src\game.py
type nul > tetris_game\src\tetris.py
type nul > tetris_game\src\utils.py
type nul > tetris_game\src\config.py

:: Создание файла для зависимостей
type nul > tetris_game\requirements.txt

:: Сообщение о завершении
echo Структура проекта Тетрис успешно создана!
