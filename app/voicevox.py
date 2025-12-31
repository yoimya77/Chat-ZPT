import requests
import json

def VOICEVOX_ENGINE(text, speaker, audio_file):

    params = {('text', text), ('speaker', speaker)}

    query = requests.post(f'http://voicevox_engine:50021/audio_query', params = params)
    if query.status_code == 422:
        print(f"*****{query.status_code} Error!*****")
    
    synthesis = requests.post(f'http://voicevox_engine:50021/synthesis', params = params, data = json.dumps(query.json()))
    if synthesis.status_code == 200:
        with open(audio_file, 'wb') as f:
            f.write(synthesis.content)
        print(f"*****Audio file has archived.*****")
    
    else:
        print(f"*****{synthesis.status_code} Error!*****")
