#!/usr/bin/python3

# TTS using API synthesis code
# Author: Jom Kuriakose
# email: jom@cse.iitm.ac.in
# Date: 16/02/2021

# textFile = 'input.txt'
# audioFolder = 'output'
# lang = 'Hindi'
# gender = 'male'


from joblib import Parallel, delayed
import requests
import shutil
import wave
import json
import wget
import sys
import os

text_split_final=[]
lang=''
gender=''
num_lines_per_request = 60
max_jobs=6

def main():

	global text_split_final
	global gender
	global lang

	# Read variables
	textFile = sys.argv[1]
	audioFolder = sys.argv[2]
	lang = sys.argv[3]
	gender = sys.argv[4]
	filename_prefix = 'tts_fs2_output_file_'

	try:
		os.makedirs(audioFolder)
	except OSError as e:
		sys.exit('Error: Output already exists!!')
		
	# Read text file
	fid = open(textFile,'r')
	text = fid.read().strip()
	text_split = text.split('\n')
	num_lines = len(text_split)
	fid.close()
	
	# IITM API
	if (num_lines <= num_lines_per_request):
		wav_list = IITM_API_request(text,gender,lang)
	else:
		n = num_lines_per_request
		text_split_final = [text_split[i * n:(i + 1) * n] for i in range((len(text_split) + n - 1) // n)]
		# print(len(text_split_final))
		num_jobs = round(num_lines/n)
		if (num_jobs > max_jobs):
			num_jobs = max_jobs
		par_wav_list = Parallel(n_jobs=num_jobs)(delayed(par_API_Req)(i) for i in range(0,len(text_split_final)))
		wav_list = []
		for i in range(0,len(par_wav_list)):
			wav_list.extend(par_wav_list[i][1])
		print(len(wav_list))

	# Output audio
	fileList = []
	for i in range(0,len(wav_list)):
		url = wav_list[i]
		filename = wget.download(url, audioFolder+'/'+filename_prefix+str(i+1))
		fileList.append(filename)
	return fileList

# Parallel wrapper
def par_API_Req(i):
	global text_split_final
	global gender
	global lang
	return i,IITM_API_request('\n'.join(text_split_final[i]),gender,lang)

# API function
def IITM_API_request(text,gender,lang):
	url = "https://asr.iitm.ac.in/fs2"
	payload = json.dumps({
		"text": text,
		"gender": gender,
		"lang": lang,
		"speed": 1.2
	})
	headers = {
		'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	if (response.json()['status'] == 'success'):
		wav_list_str = response.json()['outspeech_filepath']
	else:
		sys.exit(response.json()['reason'])
	wav_list = wav_list_str.replace('"','').strip('][').split(', ')
	return wav_list

if __name__ == "__main__":
	main()

