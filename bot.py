import uuid
import json
import os
import telebot
from dotenv import load_dotenv
from prepare import transcribe, preprocessing
from parse_and_analyze import parse_dialogue_and_analyze

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def hello(message):
    bot.reply_to(message, "Привет, я бот-определиттель эмоций. Отправь мне аудиофайл и я скажу, какие эмоции испытывает говорящий человек")


@bot.message_handler(content_types=["audio", 'document'])
def getfile(message):
    if message.content_type == 'document':  # wav
        file = bot.get_file(message.document.file_id)
    elif message.content_type == 'audio':  # mp3
        file = bot.get_file(message.audio.file_id)
    else:
        bot.reply_to(message, "Я не принимаю такой тип файлов")
        return

    byte_stream = bot.download_file(file.file_path)

    res = transcribe(byte_stream)
    print("transcribe", "/n", res)
    print()

    res = preprocessing(res)
    print("preprocessing", "/n", res)
    print()

    res = json.dumps(res, ensure_ascii=False, indent=4)
    print("json", "/n", res)
    print()

    res = parse_dialogue_and_analyze(res)
    print("last", "/n", res)
    print()




if __name__ == "__main__":
    bot.infinity_polling()

    # processfile("storage/call.mp3")