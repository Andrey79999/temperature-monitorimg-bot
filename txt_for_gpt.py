import os

# Функция для проверки, является ли файл текстовым
def is_text_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            file.read()
        return True
    except:
        return False

# Путь к корневой директории проекта
project_dir = os.getcwd()
project_dir = '.'

# Путь и имя итогового файла
output_file = 'project_summary.txt'
print(project_dir)
# Открываем итоговый файл для записи
with open(output_file, 'w', encoding='utf-8') as output:
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file in ['project_summary.txt', 'README.md', '__init__.py', '.env', 'auto_container_picup_WOT.log', 'logging_config.py', 'logging.yaml', '.gitkeep', 'txt_for_gpt.py', '.gitignore']:
                continue
            if '.git' in root or '.venv' in root or '.idea' in root or 'postgres_data' in root:
                continue
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                output.write(f"===== {file_path} =====\n")  # Добавляем заголовок с именем файла
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    output.write(content + '\n')  # Записываем содержимое файла
                output.write('\n' + '=' * 80 + '\n')  # Разделитель между файлами

print(f"Содержимое всех файлов проекта записано в {output_file}")
