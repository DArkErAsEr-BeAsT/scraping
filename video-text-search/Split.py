from pydub import AudioSegment
import math

class Split():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '/' + filename
        
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + '/' + split_filename, format="wav")
        
    def multiple_split(self, min_per_split):
        total_mins = math.floor(self.get_duration() / 60)
        print(total_mins)
        j = 0
        for i in range(0, total_mins, min_per_split):
            split_fn = str(j) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            
            print(str(j) + ' Done')
            j = j+1
            if i == total_mins - min_per_split:
                print('All splited successfully')

    def better_split(self, min_split):
        normal_time = self.get_duration()/(8*60)
        print(normal_time)
        exception_time = self.get_duration()/60
        
        exception_time = exception_time % 8
        for i in range(0, 7):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i*normal_time, (i+1)*normal_time,split_fn )
        self.single_split((self.get_duration()/60) - exception_time, self.get_duration()/60, str(7)+"_"+self.filename)