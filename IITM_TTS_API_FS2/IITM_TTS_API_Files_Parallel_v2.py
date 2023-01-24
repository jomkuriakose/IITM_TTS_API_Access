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
import argparse
import shutil
import wave
import json
import wget
import sys
import os

# lang, gender and text split into lines as global variables
text_split_final=[]
lang=''
gender=''

# Set number of lines per request while using parallel
num_lines_per_request = 60
# Set maximum number of parallel request sent to API server
max_jobs=6

# Print comment header
def code_head_print():
	code_head_str='TTS using API synthesis code\n\n'
	code_head_str+='Author: Jom Kuriakose\n'
	code_head_str+='email: jom@cse.iitm.ac.in\n'
	code_head_str+='Date: 09/11/2022\n\n'
	code_head_str+='Example: python3 IITM_TTS_API_Files_Parallel_v2.py -i input_text_file.txt -o output_folder_name -l Hindi -g male\n'
	code_head_str+='This synthesizes the text in input_text_file.txt and saves each line as .wav file in output_folder.\n\n'
	return code_head_str

# Parse arguments and print details
def parse_args():
	parser = argparse.ArgumentParser(description=code_head_print(),formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-i','--input_filename', help='Input file name', required=True)
	parser.add_argument('-o','--output_foldername', help='Output folder name', required=True)
	parser.add_argument('-l','--language', help='TTS language', required=True)
	parser.add_argument('-g','--gender', help='TTS gender\n\n', required=True)
	args = parser.parse_args()
	return args

def main():

	# Use the globally defined variables for lang, gender and text_split_final
	global text_split_final
	global gender
	global lang

	# Read variables from command line
	args=parse_args()

	textFile = args.input_filename
	audioFolder = args.output_foldername
	lang = args.language
	gender = args.gender

	# Set output file name prefix string
	filename_prefix = 'tts_fs2_output_file_'

	# Check if the output folder exits
	try:
		os.makedirs(audioFolder)
	except OSError as e:
		sys.exit('Error: Output folder already exists!!')
		
	# Read text file into lines
	fid = open(textFile,'r')
	text = fid.read().strip()
	text_split = text.split('\n')
	num_lines = len(text_split)
	fid.close()
	
	# IITM API
	if (num_lines <= num_lines_per_request):
		# Runs this section if number of lines less than 'num_lines_per_request'
		wav_list = IITM_API_request(text,gender,lang)
	else:
		n = num_lines_per_request
		# Split the text to chunks of length 'num_lines_per_request'
		text_split_final = [text_split[i * n:(i + 1) * n] for i in range((len(text_split) + n - 1) // n)]
		# Set number of jobs based on number of text chunks and max_jobs
		num_jobs = round(num_lines/n)
		if (num_jobs > max_jobs):
			num_jobs = max_jobs
		# Call IITM API parallelly and pass chunks of text
		par_wav_list = Parallel(n_jobs=num_jobs)(delayed(par_API_Req)(i) for i in range(0,len(text_split_final)))
		# Output TTS wav list will be saved in wav_list
		wav_list = []
		for i in range(0,len(par_wav_list)):
			wav_list.extend(par_wav_list[i][1])
		print(len(wav_list))

	# Write output audio
	fileList = []
	for i in range(0,len(wav_list)):
		url = wav_list[i]
		# wget the wav files from the wav_list
		filename = wget.download(url, audioFolder+'/'+filename_prefix+str(i+1)+'.wav')
		fileList.append(filename)
	return fileList

# Parallel wrapper to run the TTS api parallelly
def par_API_Req(i):
	global text_split_final
	global gender
	global lang
	return i,IITM_API_request('\n'.join(text_split_final[i]),gender,lang)

# API function that request to GPU10 server to run the FS2 TTS models and get output wav file
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
		# wav_list_str = response.json()['outspeech_filepath']
		print(response.json())
		wav_list = response.json()['outspeech_filepath']
		print(wav_list)
	else:
		sys.exit(response.json()['reason'])
	# wav_list = wav_list_str.replace('"','').strip('][').split(', ')
	return wav_list

if __name__ == "__main__":
	main()

