from pydub import AudioSegment

def convert_to_wav(input_file: str, output_file: str):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format='wav')
    print(f"Файл успешно преобразован в WAV: {output_file}")


if __name__ == "__main__":
    input_path = "storage/start.mp3"
    output_path = "storage/start.wav"
    convert_to_wav(input_path, output_path)

    input_path = "storage/end.mp3"
    output_path = "storage/end.wav"
    convert_to_wav(input_path, output_path)