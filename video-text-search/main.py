import speech_recognition as sr
from moviepy.editor import *
from pydub import AudioSegment
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path, AudioFile


MP4_PATH = "C:/Users/david/Documents/media/video.mp4"
MP3_PATH = "C:/Users/david/Documents/media/video.mp3"
WAV_PATH = "C:/Users/david/Documents/media/video.wav"
SHORT_WAV_PATH = "C:/Users/david/Documents/media/short_video.wav"
TXTOUT_PATH = "C:/Users/david/Documents/media/video_text.txt"

def main():
    if (not os.path.exists(MP4_PATH)):
        convert()
    if not os.path.exists(SHORT_WAV_PATH):
        cut_audio()
    #google_speech_recogniser()
    pocketsphinx_recogniser()
    #tmp()
# Conversion from mp4 to mp3 and then top mp3 to wav
def convert():
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP4_PATH,output= MP3_PATH)
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP3_PATH,output= WAV_PATH)

def cut_audio():
   short_audio =  AudioSegment.from_wav(WAV_PATH)
   short_audio = short_audio[0:36000]
   short_audio.export(SHORT_WAV_PATH, format='wav')

#* Problem is that the speech recognizer of google is limited in request size => max 10 MB (1 min) and takes some time (15 sec)
def google_speech_recogniser():
    rec = sr.Recognizer()
    audio = sr.AudioFile(SHORT_WAV_PATH)
    with audio as source:
        audio = rec.record(source, duration=250)
        outF = open(TXTOUT_PATH, "w")
        outF.writelines(rec.recognize_google(audio))

# TODO - build own Speech recognition system
#* Have to understand how the coordinates of the output work / can be translated to seconds or frames
def pocketsphinx_recogniser():
    fps=100
    
    audio = AudioFile(audio_file=SHORT_WAV_PATH,lm=False, keyphrase='today', kws_threshold=1e-9, frate=fps)
    
    for phrase in audio:
        for seg in phrase.seg():
            print('| %4ss | %4ss | %8s |' % (seg.start_frame / fps, seg.end_frame / fps, seg.word))

#* trying out functionnalities
def tmp():
    model_path = get_model_path()
    data_path = get_data_path()
    config = {
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    }
    
    ps = Pocketsphinx(**config)
    ps.decode(
        audio_file=os.path.join(data_path, SHORT_WAV_PATH),
        buffer_size=2048,
        no_search=False,
        full_utt=False
    )
    ps.set_keyphrase(ps, "image")
    ps.set_search(ps,"keyphrase_search")
    ps.start_utt()
main()