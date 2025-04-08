import json
from pathlib import Path
from analyze_dialogue import analyze_dialogue
import pandas as pd

df = pd.read_excel('data.xlsx')
def parse_first_dialogue_and_analyze(file_path: str):
    # Загрузка данных
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Извлекаем первый диалог
    first_dialog = data
    lines = first_dialog["lines"]

    # Формируем текст диалога в виде: Менеджер: ... Клиент: ...
    dialogue_text = "\n".join(
        f"{'Менеджер' if line['role'] == 'manager' else 'Клиент'}: {line['text']}" for line in lines
    )

    print("=== Отправляем следующий диалог в LLM ===")
    # Отправляем в LLM для анализа
    analysis_result = analyze_dialogue(dialogue_text)

    if analysis_result:
        print("=== Результат анализа ===")
        print(analysis_result.model_dump_json(indent=2))
        df.loc[len(df)] = {'date': None, 'manager_id': None, 'manager_score': response.manager_performance.score, 'manager_explanation': response.manager_performance.explanation,
                   'client_emotion': response.client_emotion.score, 'client_explanation': response.client_emotion.explanation}
        df.to_excel('data.xlsx', index=False)
        return analysis_result
    else:
        print("Анализ не удался или модель отказалась отвечать.")
        return None


# Пример вызова
response = parse_first_dialogue_and_analyze("dialog.json")
df
