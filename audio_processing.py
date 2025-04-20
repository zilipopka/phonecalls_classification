import gigaam
from moviepy.editor import AudioFileClip
from typing import Dict
from pydub import AudioSegment

model_emo = gigaam.load_model('emo')


def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format='wav')
    print(f"Файл успешно преобразован в WAV: {output_file}")


def get_audio_emo(filepath) -> str:
    emotion2prob: Dict[str, int] = model_emo.get_probs(filepath)
    return sorted(list(emotion2prob.items()), key=lambda x: x[1], reverse=True)[0][0]


def get_audio_part(filename, start, end):
    audio = AudioFileClip(filename)
    start = audio.subclip(start, end)
    start.write_audiofile("start.mp3")


if __name__ == "__main__":
    input_path = "storage/start.mp3"
    output_path = "storage/start.wav"
    convert_to_wav(input_path, output_path)

    input_path = "storage/end.mp3"
    output_path = "storage/end.wav"
    convert_to_wav(input_path, output_path)