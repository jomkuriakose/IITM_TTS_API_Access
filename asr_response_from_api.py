from os import replace
import requests
import json
import base64
from glob import glob 
from tqdm import tqdm 
import sys

url = "https://meity-dev-asr.ulcacontrib.org/asr/v1/recognize/hi"

def encode_audio(audio):
    wav_bytes = base64.b64encode(open(audio, "rb").read())
    return wav_bytes.decode('utf-8')

def create_payload(audio_path):


    payload = json.dumps({
        "config": {
                "transcriptionFormat": {
                            "value": "srt"
                                },
                    "audioFormat": "wav",
                        "punctuation": False,
                            "enableInverseTextNormalization": False
                                },
            "audio": [
                    {
                            "audioContent":encode_audio(audio_path)
                                }
                        ]
            })
    return payload

headers = {
          'Content-Type': 'application/json'
          }


audio = sys.argv[1]
payload = create_payload(audio)

response = requests.request("POST", url, headers=headers, data=payload)

text = json.loads(response.text)
asr_output = text["output"][0]["source"]
print(asr_output)