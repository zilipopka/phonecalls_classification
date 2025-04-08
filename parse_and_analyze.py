from os.path import isfile
import json
from pathlib import Path
from analyze_dialogue import analyze_dialogue
import pandas as pd
import os

try:
  df = pd.read_excel('data.xlsx')
except:
  df = pd.DataFrame(columns=['date', 'manager_id', 'manager_score', 'manager_explanation', 'client_emotion', 'client_explanation'])
def parse_dialogue_and_analyze(json_string):
    # Загрузка данных
    data = json.loads(json_string)

    # Извлекаем первый диалог
    first_dialog = data
    lines = first_dialog

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
        print('СЕЙЧАС ВСЕ БУДЕТ')
        print(df)
        print('НУ ВРОДЕ БЫЛО')
        return analysis_result
    else:
        print("Анализ не удался или модель отказалась отвечать.")
        return None


# Пример вызова
response = analyze_dialogue('dialog.json')
print(response)
