import speech_recognition as sr
from moviepy.editor import *
from pydub import AudioSegment
# from pocketsphinx import Pocketsphinx, get_model_path, get_data_path, AudioFile
from vosk import GpuThreadInit, Model, KaldiRecognizer, GpuInit
import json
import wave
import Word as custom_Word
import os
os.add_dll_directory(os.getcwd())
import vlc
import time
import tkinter as tk
from tkinter import  filedialog
from tkinter.ttk import *

PATH = ""



KEYWORD = ""
MP4_PATH = "C:/Users/david/Documents/media/video.mp4"
MP3_PATH = "C:/Users/david/Documents/media/video.mp3"
WAV_PATH = "C:/Users/david/Documents/media/video.wav"
MONO_WAV_PATH = "C:/Users/david/Documents/media/video_mono.wav"
SHORT_WAV_PATH = "C:/Users/david/Documents/media/short_video.wav"
TXTOUT_PATH = "C:/Users/david/Documents/media/video_text.txt"
JSON_PATH = "C:/Users/david/Documents/media/video_json.txt"
# TXTOUT_PATH_1 = "C:/Users/david/Documents/media/video_text_1.txt"
# JSON_PATH_1 = "C:/Users/david/Documents/media/video_json_1.txt"

def main():
    window = tk.Tk()
    window.columnconfigure(0, minsize=250)
    window.rowconfigure([0, 1], minsize=100)
    frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
    frame1.grid(row=0, column=0)
    frame2 = tk.Frame(master=window, width=100, bg="yellow")
    frame2.grid(row=1,column=0)
    entry = tk.Entry(master=frame2)
    button = tk.Button(frame1, text="Choose Video", default="in active", command=fdiag(), pady=10)
    frame3 = tk.Frame(master=window, width=100, bg="yellow")
    frame3.grid(row=1,column=1)
    button_start = tk.Button(frame1, text="Start", default="inactive", pady=10, background='green', command=vosk_rec_thorough())
    print("starting work on video :" + PATH)
    text_to_search = entry.get()
    KEYWORD = text_to_search
    button_start.pack()
    button.pack()
    entry.pack()
    
    if (not os.path.exists(MP3_PATH)):
        convert()
    if not os.path.exists(SHORT_WAV_PATH):
        cut_audio()
    window.mainloop()
    player()
def fdiag():
    PATH = filedialog.askopenfilename()
    return PATH
# Conversion from mp4 to mp3 and then top mp3 to wav, then to mono channel wav
def convert():
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP4_PATH, output=MP3_PATH)
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP3_PATH, output=WAV_PATH)
    sound = AudioSegment.from_wav(WAV_PATH)
    sound = sound.set_channels(1)
    sound.export(MONO_WAV_PATH, format="wav")

# get short part of audio
def cut_audio():
    short_audio = AudioSegment.from_wav(MONO_WAV_PATH)
    short_audio = short_audio[0:10000]
    short_audio.export(SHORT_WAV_PATH, format='wav')

# * Problem is that the speech recognizer of google is limited in request size => max 10 MB (1 min) and takes some time (15 sec)


def google_speech_recogniser():
    rec = sr.Recognizer()
    audio = sr.AudioFile(SHORT_WAV_PATH)
    with audio as source:
        audio = rec.record(source, duration=250)
        outF = open(TXTOUT_PATH, "w")
        outF.writelines(rec.recognize_google(audio))

# TODO - build own Speech recognition system

def pocketsphinx_recogniser():
    fps = 100

    audio = AudioFile(audio_file=SHORT_WAV_PATH, lm=False,
                      keyphrase='today', kws_threshold=1e-9, frate=fps)

    for phrase in audio:
        for seg in phrase.seg():
            print('| %4ss | %4ss | %8s |' %
                  (seg.start_frame / fps, seg.end_frame / fps, seg.word))

# * vosk recognizer works well


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
    for word in list_of_Words:
        print(word.to_string())
        with open(JSON_PATH, 'a+') as output:
            print(word.to_txt(), file=output)

    with open(JSON_PATH, 'w') as output:
        print(results, file=output)

   

    # write text portion of results to a file
    with open(TXTOUT_PATH, 'w') as output:
        print(json.dumps(textResults, indent=4), file=output)
    # write text portion of results to a file
    # with open(TXTOUT_PATH, 'w') as output:
    #     print(json.dumps(textResults, indent=4), file=output)



def occurences_processing():
    occurences = []
    with open(JSON_PATH) as res:    
        for line in res:
            line = line.split()
            if KEYWORD in line:
                secs=[line[1],line[2]]
                secs= [float(i) for i in secs]
                occurences.append(secs)
    return occurences
def player():
    occurences=occurences_processing()
    start = occurences[0][0]
    print(start)
    player = vlc.MediaPlayer(MP4_PATH)
    player.play()
    player.set_time(int(1000*start)-6000)
    
    time.sleep(20)

main()
