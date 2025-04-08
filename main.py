import json
from parse_and_analyze import parse_dialogue_and_analyze
from prepare import preprocessing, transcribe

res = transcribe('call.mp3')
res = preprocessing(res)
res = json.dumps(res, ensure_ascii=False, indent=4)
res = parse_dialogue_and_analyze(res)