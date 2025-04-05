import json
from pathlib import Path
from analyze_dialogue import analyze_dialogue


def parse_first_dialogue_and_analyze(file_path: str):
    # Загрузка данных
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Извлекаем первый диалог
    first_dialog = data["dialogs"][0]
    lines = first_dialog["lines"]

    # Формируем текст диалога в виде: Менеджер: ... Клиент: ...
    dialogue_text = "\n".join(
        f"{'Менеджер' if line['role'] == 'manager' else 'Клиент'}: {line['text']}" for line in lines
    )

    print("=== Отправляем следующий диалог в LLM ===")
    print(dialogue_text[:1000])  # усеченный вывод

    # Отправляем в LLM для анализа
    analysis_result = analyze_dialogue(dialogue_text)

    if analysis_result:
        print("=== Результат анализа ===")
        print(analysis_result.model_dump_json(indent=2))
        return analysis_result
    else:
        print("Анализ не удался или модель отказалась отвечать.")
        return None


# Пример вызова
if __name__ == "__main__":
    parse_first_dialogue_and_analyze("dialog.json")
