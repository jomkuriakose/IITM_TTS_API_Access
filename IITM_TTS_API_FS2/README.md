usage: IITM_TTS_V2_API.py [-h] [-r] -i INPUT_FILENAME [-o OUTPUT_WAV_FILENAME]
                          [-v OUTPUT_VTT_FILENAME] [-f OUTPUT_FOLDERNAME] -l
                          LANGUAGE -g GENDER

TTS using API synthesis code

Author: Jom Kuriakose
email: jom@cse.iitm.ac.in
Date: 29/11/2022

Example: python3 IITM_TTS_V2_API.py -r -i input_text_file.txt -f output_folder_name -o output_mp3_filename.mp3 -v output_vtt_filename.vtt -l Hindi -g male
This synthesizes the text in input_text_file.txt and saves output in output_mp3_filename.mp3, vtt at segment level in output_vtt_filename.vtt and corresponding segments in output_folder_name.

optional arguments:
  -h, --help            show this help message and exit
  -r, --remove_previous
                        Set this flag to remove the previous files (default=False)
  -i INPUT_FILENAME, --input_filename INPUT_FILENAME
                        Input file name
  -o OUTPUT_WAV_FILENAME, --output_wav_filename OUTPUT_WAV_FILENAME
                        Output wav file name
  -v OUTPUT_VTT_FILENAME, --output_vtt_filename OUTPUT_VTT_FILENAME
                        Output vtt file name
  -f OUTPUT_FOLDERNAME, --output_foldername OUTPUT_FOLDERNAME
                        Output folder name. Saves mp3 segments corresponding to the VTT file in this folder.
  -l LANGUAGE, --language LANGUAGE
                        TTS language
  -g GENDER, --gender GENDER
                        TTS gender
                        
