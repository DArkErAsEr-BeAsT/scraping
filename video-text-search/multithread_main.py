#!/usr/bin/python

from moviepy.editor import *
from pydub import AudioSegment
from multiprocessing.dummy import Pool
from vosk import GpuThreadInit, Model, KaldiRecognizer, GpuInit
import json
import wave
import Word as custom_Word
import os
import Split as split
os.add_dll_directory(os.getcwd())
import math
from multiprocessing import Process


MP4_PATH = "C:/Users/david/Documents/media/video.mp4"
MP3_PATH = "C:/Users/david/Documents/media/video.mp3"
WAV_PATH = "C:/Users/david/Documents/media/video.wav"
MONO_WAV_PATH = "C:/Users/david/Documents/media/video_mono.wav"
SHORT_WAV_PATH = "C:/Users/david/Documents/media/short_video.wav"
TXTOUT_PATH = "C:/Users/david/Documents/media/video_text.txt"
JSON_PATH = "C:/Users/david/Documents/media/video_json.txt"
TXT = "video_text.txt"
JSON = "video_json.txt"
FOLDER = "C:/Users/david/Documents/media"
VIDEO = "video_mono.wav"

def main():
    # convert()
    cut_audio()
    parallelizer()
    



def parallelizer():
    processes = []
    p = Pool(8)
    wf = wave.open("C:/Users/david/Documents/media/0_video_mono.wav", "rb")

    for i in range(0,8):
        f = FOLDER+"/"+str(i)+"_"+VIDEO
        wf = wave.open(f, "rb")
        print(f)
        p = Process(target=vosk_rec_thorough(wf))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

# Conversion from mp4 to mp3 and then top mp3 to wav, then to mono channel wav
def convert():
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP4_PATH, output=MP3_PATH)
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP3_PATH, output=WAV_PATH)
    sound = AudioSegment.from_wav(WAV_PATH)
    sound = sound.set_channels(1)
    sound.export(MONO_WAV_PATH, format="wav")

# split audio into 8 segments for parallel execution
def cut_audio():
    audio = AudioSegment.from_wav(MONO_WAV_PATH)
    duration = audio.duration_seconds/60
    splt = split.Split(FOLDER, VIDEO)
    splt.better_split((8))


def vosk_rec_thorough(wf):
    # GpuInit()
    # GpuThreadInit()
    
    results = []
    textResults = []
  

    model = Model(r"C:/Users/david/Documents/media/vosk-model-en-us-0.22")
    
    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            part_result = json.loads(recognizer.Result())
            results.append(part_result)

    part_result = json.loads(recognizer.FinalResult())
    results.append(part_result)
    list_of_Words = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition 
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            w = custom_Word.Word(obj)  # create custom Word object
            list_of_Words.append(w)  # and add it to list
    # write results to a file
    for i in range (0,8):
        for word in list_of_Words:
            #print(word.to_string())
            with open(FOLDER+"/"+str(i)+"_"+JSON, 'a+') as output:
                print(word.to_txt(), file=output)

        with open(FOLDER+"/"+str(i)+"_"+JSON, 'w') as output:
            print(results, file=output)

    

        # write text portion of results to a file
        with open(FOLDER+"/"+str(i)+"_"+TXT, 'w') as output:
            print(json.dumps(textResults, indent=4), file=output)
    # write text portion of results to a file
    # with open(TXTOUT_PATH, 'w') as output:
    #     print(json.dumps(textResults, indent=4), file=output)

main()