import json
import requests

YOUR_API_KEY = 'YOURS'
YOUR_AUDIO_FILE = 'resources/call1_16k_signed.wav'
REGION = 'eastus' # westus, eastasia, northeurope 
MODE = 'interactive'
LANG = 'en-GB'
FORMAT = 'simple'

def handler():
    # 1. Get an Authorization Token
    token = get_token()
    # 2. Perform Speech Recognition
    results = get_text(token, YOUR_AUDIO_FILE)
    # 3. Print Results
    print(results)

def get_token():
    # Return an Authorization Token by making a HTTP POST request to Cognitive Services with a valid API key.
    url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': YOUR_API_KEY
    }
    r = requests.post(url, headers=headers)
    token = r.content
    return(token)

def get_text(token, audio):
    # Request that the Bing Speech API convert the audio to text
    url = 'https://{0}.stt.speech.microsoft.com/speech/recognition/{1}/cognitiveservices/v1?language={2}&format={3}'.format(REGION, MODE, LANG, FORMAT)
    headers = {
        'Accept': 'application/json',
        'Ocp-Apim-Subscription-Key': YOUR_API_KEY,
        'Transfer-Encoding': 'chunked',
        'Content-type': 'audio/wav; codec=audio/pcm; samplerate=8000',
        'Authorization': 'Bearer {0}'.format(token)
    }
    print("Posting: "+ str(YOUR_AUDIO_FILE))
    r = requests.post(url, headers=headers, data=stream_audio_file(audio))
    results = json.loads(r.content)
    return results

def stream_audio_file(speech_file, chunk_size=1024):
    # Chunk audio file
    with open(speech_file, 'rb') as f:
        while 1:
            data = f.read(1024)
            if not data:
                break
            yield data

if __name__ == '__main__':
    handler()