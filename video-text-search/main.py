import speech_recognition as sr
from moviepy.editor import *
from pocketsphinx import AudioFile

MP4_PATH = "C:/Users/david/Documents/media/video.mp4"
MP3_PATH = "C:/Users/david/Documents/media/video.mp3"
WAV_PATH = "C:/Users/david/Documents/media/video.wav"
TXTOUT_PATH = "C:/Users/david/Documents/media/video_text.txt"

def main():
    if (not os.path.exists(MP4_PATH)):
        convert()
    #google_speech_recogniser()
    #pocketsphinx_recogniser()
    tmp()
# Conversion from mp4 to mp3 and then top mp3 to wav
def convert():
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP4_PATH,output= MP3_PATH)
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP3_PATH,output= WAV_PATH)


#* Problem is that the speech recognizer of google is limited in request size => max 10 MB (1 min) and takes some time (15 sec)
def google_speech_recogniser():
    rec = sr.Recognizer()
    audio = sr.AudioFile(WAV_PATH)
    with audio as source:
        audio = rec.record(source, duration=250)
        outF = open(TXTOUT_PATH, "w")
        outF.writelines(rec.recognize_google(audio))

# TODO - build own Speech recognition system
#* Have to understand how the coordinates of the output work / can be translated to seconds or frames
def pocketsphinx_recogniser():
    AudioFile() 
    audio = AudioFile(audio_file=WAV_PATH,lm=False, keyphrase='forward', kws_threshold=1e-20)
    for phrase in audio:
        print(phrase.segments(detailed=True))

#* trying out functionnalities
def tmp():
    # Frames per Second
    fps = 100

    for phrase in AudioFile(audio_file=WAV_PATH,frate=fps):  # frate (default=100)
        print('-' * 28)
        print('| %5s |  %3s  |   %4s   |' % ('start', 'end', 'word'))
        print('-' * 28)
        for s in phrase.seg():
            print('| %4ss | %4ss | %8s |' % (s.start_frame / fps, s.end_frame / fps, s.word))
        print('-' * 28)
main()