from . import human_language_decoder as hld

import threading

# Should have audio.py here...



class SoundInterface:
    def __init__(self):
        self.transcription = hld.Transcription()
    
    def listen_for_hl(self, hl_decoder, event):
        exhaust = hl_decoder.run(event)
        
        if exhaust:
            print("Stopping listening due to: " + exhaust + " detected in: " + "".join(map(str, hl_decoder.composition.values())))
        else:
            print("How am I here?")
     
    def mock_listen_for_hl(self, transcription, event): #not sure why we're passing this as an argument...
        
        index = 0
        while True:
            x = input("---type--->")
            self.transcription.composition[index] = x 
            event.set()  
            index += 1
            
    def activate(self):
        t = threading.Thread(target=self.listen_for_hl, args=[self.transcription])
        t.start()
        t.join() # blocks until decoder stops
        
if __name__ == "__main__":
    transcription = hld.Transcription()
    t = threading.Thread(target=listen_for_hl, args=[transcription])
    t.start()
    # bulk
    t.join()
