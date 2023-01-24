#!/usr/bin/python3

# TTS using API synthesis code
# Author: Jom Kuriakose
# email: jom@cse.iitm.ac.in
# Date: 29/11/2022

# textFile = 'input.txt'
# audioFolder = 'output'
# lang = 'Hindi'
# gender = 'male'

from joblib import Parallel, delayed
import requests
import argparse
import pathlib
import shutil
import base64
import wave
import json
import wget
import sys
import os

# Print comment header
def code_head_print():
	code_head_str='TTS using API synthesis code\n\n'
	code_head_str+='Author: Jom Kuriakose\n'
	code_head_str+='email: jom@cse.iitm.ac.in\n'
	code_head_str+='Date: 29/11/2022\n\n'
	code_head_str+='Example: python3 IITM_TTS_V2_API.py -r -i input_text_file.txt -f output_folder_name -o output_mp3_filename.mp3 -v output_vtt_filename.vtt -l Hindi -g male\n'
	code_head_str+='This synthesizes the text in input_text_file.txt and saves output in output_mp3_filename.mp3, vtt at segment level in output_vtt_filename.vtt and corresponding segments in output_folder_name.\n\n'
	return code_head_str

# Parse arguments and print details
def parse_args():
	parser = argparse.ArgumentParser(description=code_head_print(),formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-r','--remove_previous', help='Set this flag to remove the previous files (default=False)', required=False, action='store_true')
	parser.add_argument('-i','--input_filename', help='Input file name', required=True)
	parser.add_argument('-o','--output_wav_filename', help='Output wav file name', required=False, default=False)
	parser.add_argument('-v','--output_vtt_filename', help='Output vtt file name', required=False, default=False)
	parser.add_argument('-f','--output_foldername', help='Output folder name. Saves mp3 segments corresponding to the VTT file in this folder.', required=False, default=False)
	parser.add_argument('-l','--language', help='TTS language', required=True)
	parser.add_argument('-g','--gender', help='TTS gender\n\n', required=True)
	args = parser.parse_args()
	return args

def main():

	# Read variables from command line
	args=parse_args()

	# Read inputs
	if args.output_foldername or args.output_wav_filename:
		textFile = args.input_filename
		filePrefix = pathlib.Path(textFile).stem
		lang = args.language
		gender = args.gender
		audioFolder = args.output_foldername
		audioFile = args.output_wav_filename
		vttFile = args.output_vtt_filename
		removeFlag = args.remove_previous
		print('Log: Reading inputs')
		print(f'--------------------\ntextFile: {textFile}\nfilePrefix: {filePrefix}\nlang: {lang}\ngender: {gender}\naudioFolder: {audioFolder}\naudioFile: {audioFile}\nvttFile: {vttFile}\nremoveFlag: {removeFlag}\n--------------------')
	else:
		sys.exit('Error: Output file/folder information not found!!\nSet -o / -f arguments')

	if not (audioFolder == False):
		print("audioFolder")
		# Check if the output folder exits
		if not os.path.isdir(audioFolder):
			os.makedirs(audioFolder)
			print(f'Log: Creating "{audioFolder}"')
		else:
			if removeFlag:
				shutil.rmtree(audioFolder, ignore_errors=False)
				print(f'Log: Deleting "{audioFolder}"')
				os.makedirs(audioFolder)
				print(f'Log: Creating "{audioFolder}"')
			else:
				sys.exit(f'Error: Output folder:"{audioFolder}" already exists!!\nSet -r flag to remove the already existing folder.')
	
	if not (audioFile == False):
		# Check if the output file exits
		if os.path.isfile(audioFile):
			if removeFlag:
				os.remove(audioFile)
				print(f'Log: Deleting "{audioFile}"')
			else:
				sys.exit(f'Error: Output file:"{audioFile}" already exists!!\nSet -r flag to remove the already existing file.')

	if not (vttFile == False):
		# Check if the output file exits
		if os.path.isfile(vttFile):
			if removeFlag:
				os.remove(vttFile)
				print(f'Log: Deleting "{vttFile}"')
			else:
				sys.exit(f'Error: VTT file:"{vttFile}" already exists!!\nSet -r flag to remove the already existing file.')

	# Read text file into lines
	fid = open(textFile,'r')
	text = fid.read().strip()
	text_split = text.split('\n')
	num_lines = len(text_split)
	fid.close()
	print(f'Log: Reading input file: {textFile}. Number of lines: {num_lines}')

	print('Log: TTS api call - init')
	api_output = IITM_API_request(text,gender,lang)
	print('Log: TTS api call - done')

	# Write TTS audios to output folder
	if not (audioFolder == False):
		segments = api_output['segments']
		for wave_idx in range(0,len(segments)):
			wav_file = open("{}/{}_{:04}.mp3".format(audioFolder,filePrefix,wave_idx+1),'wb')
			decode_string = base64.b64decode(segments[wave_idx])
			wav_file.write(decode_string)
			wav_file.close()
		print(f'Log: TTS saved to folder: "{audioFolder}"')

	# Write output audio file
	if not (audioFile == False):
		audio = api_output['audio']
		file_name = "{}.mp3".format(filePrefix)
		wav_file = open(file_name,'wb')
		decode_string = base64.b64decode(audio)
		wav_file.write(decode_string)
		wav_file.close()
		print(f'Log: TTS saved to file: "{file_name}"')

	# Write output VTT file
	if not (vttFile == False):
		vtt_info = api_output['vtt']
		file_name = "{}.vtt".format(filePrefix)
		vtt_file = open(file_name,'w')
		vtt_file.write(vtt_info)
		vtt_file.close()
		print(f'Log: VTT saved to file: "{file_name}"')

# API function that request to server to run the FS2 TTS models and get output wav file
def IITM_API_request(text,gender,lang):
	url = "https://asr.iitm.ac.in/ttsv2/tts"
	payload = json.dumps({
		"input": text,
		"gender": gender,
		"lang": lang,
		"alpha": 1.2,
		"segmentwise":"True"
	})
	headers = {
		'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	if (response.json()['status'] == 'success'):
		return response.json()
	else:
		sys.exit(response.json()['reason'])

if __name__ == "__main__":
	main()
