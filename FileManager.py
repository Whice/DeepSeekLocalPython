import os
from pathlib import Path


class FileManager:
    def __init__(self, base_dir: str, file_name: str, content: str = '', extension: str = 'txt'):
        """
        Инициализация объекта для работы с файлами
        :param base_dir: Базовый каталог для файла
        :param file_name: Имя файла без расширения
        :param content: Содержимое файла
        :param extension: Расширение файла (по умолчанию .txt)
        """
        self.base_dir = Path(base_dir)
        self.file_name = Path(file_name).stem  # Удаляем существующее расширение если есть
        self.extension = extension.lstrip('.')
        self.content = content

        # Формируем полный путь
        self.full_path = self.base_dir / f"{self.file_name}.{self.extension}"

    def create_or_update(self) -> bool:
        """Создает или обновляет файл"""
        try:
            # Создаем директорию если необходимо
            self.base_dir.mkdir(parents=True, exist_ok=True)

            with open(self.full_path, 'w', encoding='utf-8') as file:
                file.write(self.content)
            return True
        except Exception as e:
            print(f"Ошибка при работе с файлом: {str(e)}")
            return False

    def delete(self) -> bool:
        """Удаляет файл"""
        try:
            if self.full_path.exists():
                self.full_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Ошибка при удалении файла: {str(e)}")
            return False

    def read(self) -> str:
        """Читает содержимое файла"""
        try:
            with open(self.full_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка чтения файла: {str(e)}"

    def exists(self) -> bool:
        """Проверяет существование файла"""
        return self.full_path.exists()

    def get_full_path(self) -> str:
        """Возвращает абсолютный путь к файлу"""
        return str(self.full_path.resolve())

    def update_content(self, new_content: str) -> bool:
        """Обновляет содержимое файла"""
        self.content = new_content
        return self.create_or_update()

    def change_location(self, new_base_dir: str = None, new_file_name: str = None):
        """Изменяет расположение или имя файла"""
        if new_base_dir:
            self.base_dir = Path(new_base_dir)
        if new_file_name:
            self.file_name = Path(new_file_name).stem
        self.full_path = self.base_dir / f"{self.file_name}.{self.extension}"

'''
def Example():
    # Создаем менеджер файлов
    fm = FileManager(
        base_dir=r"D:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\scripts\vscripts\bots",
        file_name="test",
        content="Первоначальное содержимое test",
        extension="lua"
    )

    # Создаем/обновляем файл
    if fm.create_or_update():
        print(f"Файл создан/обновлен: {fm.get_full_path()}")

    # Читаем содержимое
    print("Содержимое файла:", fm.read())

    # Обновляем содержимое
    fm.update_content("Новое обновленное содержимое")
    print("Обновленное содержимое:", fm.read())

    # Удаляем файл
    if fm.delete():
        print("Файл успешно удален")

Example()'''