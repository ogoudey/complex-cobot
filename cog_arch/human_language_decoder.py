import whisper

import datetime as dt
import time as t
import random
import os

import threading

from . import audio # audio slicer with configuration
from . import play

def transcribe(file_name, composition, index):
    print("Transcribing for index "+str(index)+"...")
    a = t.time()
    model = whisper.load_model("tiny.en") # maybe all threads can use the same loaded model
    print("Model loaded for index "+index+"...")
    result = model.transcribe(file_name)
    composition[index] = result["text"] # can multiple threads update a dict
    print("Finished Transcription in " + str(t.time() - a) + " seconds: " + result["text"] + "\n")
    print(composition)

def record(a):
    a.record()
    

class Transcription:
    def __init__(self):
        
        self.composition = dict()

# file to start transcribing; composition (dict); index (key) for where to put transcription (also in the name of the file)
# pass the transcription if all threads can use the sam emodel
    
    def run(self, event):
        now = dt.datetime.now()
        time_str = now.strftime("%H-%M")
        
        trial = "trials/" + time_str
        os.makedirs(trial, exist_ok=True)
        print("Made checkpoint directory " + trial)
        index = 0
        

        a = audio.Recorder()
        a.record()
        while True:
            
            this_file = "./" + trial + "/" + str(index) + ".wav"
            a.write(this_file)
            #start_time = t.time()
            # hit checkpoint
            t = threading.Thread(target=transcribe, args=[this_file, self.composition, index])
            t.start()


            
            index += 1
            #stop_time = t.time()
            #print(str(stop_time - start_time) + " second lag.")
            
            a = audio.Recorder()
            at = threading.Thread(target=record, args=[a])
            at.start()


          
            t.join()    # waits for inference (transcribe) - should come before other thread, otherwise we won't start a new recording thread
            
            as_str = ' '.join(map(str, self.composition.values()))
            #print("_______________________")
            #print(as_str)
            #print("_______________________")
            event.set()
            exit_phrase = "Stop listening to me"
            if exit_phrase.lower() in as_str.lower():
                return exit_phrase
            # create b recorder ??
            # start b recorder now ??
            # and overlap the two... with an llm??
            at.join()
    


if __name__ == "__main__":
    t = Transcription()
    t.run()
            

    
    
