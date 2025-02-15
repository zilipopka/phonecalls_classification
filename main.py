import whisper
from moviepy.editor import AudioFileClip
from langchain_gigachat.chat_models import GigaChat
from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage

load_dotenv()

model = whisper.load_model("base")  # Доступные модели: tiny, base, small, medium, large
model_giga = GigaChat(
    credentials=os.getenv('CREDENTIALS'),
    scope=os.getenv('SCOPE'),
    model=os.getenv('MODEL'),
    verify_ssl_certs=False
)

audio = AudioFileClip('call.mp3')
length = int(audio.duration)

start = audio.subclip(0, 20)
end = audio.subclip(length - 20, length)

start.write_audiofile("start.mp3")
end.write_audiofile('end.mp3')

start_result = model.transcribe("start.mp3")

end_result = model.transcribe("end.mp3")

def mood(text):
    task = f"Сейчас я отправлю тебе разговор между двумя людьми. {text}. Проанализируй его и назови эмоцию, которую испытывают его участники одним словом, например: веселье, злость, грусть. В ответ отправь только слово, описывающее эмоцию разговора"
    messages = [HumanMessage(content=task)]
    response = model_giga.invoke(messages)
    return response.content

print('Эмоция в начале разговора: ', mood(start_result))
print('Эмоция в конце разговора: ', (mood(end_result)))


