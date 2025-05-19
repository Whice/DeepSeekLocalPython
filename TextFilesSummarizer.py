import os
from pathlib import Path


class TextFilesSummarizer:
    def __init__(self, folder_path: str, valid_extensions: list = ['.txt']):
        """
        Инициализация класса
        :param folder_path: Путь к целевой папке
        :param valid_extensions: Список разрешённых расширений (например ['.txt', '.md'])
        """
        self.folder_path = Path(folder_path)
        self.valid_extensions = [ext.lower() for ext in valid_extensions]

        if not self.folder_path.exists():
            raise ValueError(f"Папка {folder_path} не существует")

        if not self.folder_path.is_dir():
            raise ValueError(f"{folder_path} не является папкой")

    def generate_summary(self) -> str:
        """Генерирует итоговый текст с содержимым всех файлов"""
        files_content = []

        for file_path in self._get_files():
            content = self._read_file(file_path)
            files_content.append(
                f"##*FileName*##: {file_path.relative_to(self.folder_path)}\n"
                f"{content}\n\n"
            )

        if not files_content:
            return "Нет файлов с указанными расширениями в папке и подпапках"

        return "\n".join(files_content)

    def _get_files(self) -> list:
        """Рекурсивный поиск файлов во всех подпапках"""
        valid_files = []

        # Рекурсивный обход всех поддиректорий
        for file_path in self.folder_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.valid_extensions:
                valid_files.append(file_path)

        return sorted(valid_files, key=lambda x: x.relative_to(self.folder_path))

    def _read_file(self, file_path: Path) -> str:
        """Чтение содержимого файла с обработкой ошибок (без изменений)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='cp1251') as f:
                    return f.read()
            except Exception as e:
                return f"Ошибка чтения файла: {str(e)}"
        except Exception as e:
            return f"Ошибка чтения файла: {str(e)}"

    def save_summary(self, output_file: str):
        """Сохранение резюме в файл"""
        summary = self.generate_summary()
        return summary

#Пример использования:
'''summarizer = TextFilesSummarizer(
    folder_path=r"D:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\scripts\vscripts\bots",
    valid_extensions=['.txt', '.lua', ]
    )
print(summarizer.generate_summary())'''