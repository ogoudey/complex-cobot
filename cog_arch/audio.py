
""" # commented out for -d flag
import pyaudio
import wave
"""
import datetime as dt


class Recorder:
    def __init__(self):
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.fs = 44100
        self.window = 10
        self.sample_size = None # set later
        
        
        self.frames = []
    
    def record(self):
        self.frames = []
        p = pyaudio.PyAudio()
        self.sample_size = p.get_sample_size(self.sample_format)
        print("Recording for " + str(self.window) + " seconds...")
        stream = p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.fs,
                        frames_per_buffer=self.chunk,
                        input=True)
        for i in range(0, int(self.fs / self.chunk * self.window)):
            data = stream.read(self.chunk)
            self.frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        print('Finished recording')

    def write(self, file_name):
        
        
        wf = wave.open(file_name, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sample_size)
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
if __name__ == "__main__":
    r = Recorder()
    r.record()
    r.write("hi-im-steve.wav")

