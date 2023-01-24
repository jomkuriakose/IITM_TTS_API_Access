#!/usr/bin/python3

# TTS using ULCA API synthesis code - IITM TTS
# Author: Jom Kuriakose
# email: jom@cse.iitm.ac.in
# Date: 04/08/2022

import sys
import json
import base64
import requests

textFile = sys.argv[1]

fid = open(textFile,'r')
text = fid.read().strip()
text_split = text.split('\n')
fid.close()

fileJsonList=[]
for line in text_split:
	json_obj = {"source": line}
	fileJsonList.append(json_obj)

url = "https://asr.iitm.ac.in/tts"
payload=json.dumps({
	"input": fileJsonList,
	"config": {
		"language": {
			"sourceLanguage": "hi"
		},
		"gender": "male"
	}
})
headers = {
	'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.json())

wav_list = response.json()['audio']
filePrefix = 'tts_syn_'
for wave_idx in range(0,len(wav_list)):
	wav_file = open(filePrefix+str(wave_idx)+'.mp3','wb')
	decode_string = base64.b64decode(wav_list[wave_idx]['audioContent'])
	wav_file.write(decode_string)
	wav_file.close()


