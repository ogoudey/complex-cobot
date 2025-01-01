"""
cobot

A -> X -> C -> Y -> P

Collaborator.loop( take audio input )

"""
PRINT = False

from simple_cobots import cobot
from cog_arch import sound_interface

import sys
import threading

if __name__ == "__main__":
    event = threading.Event()

    co = cobot.Collaboration()
    si = sound_interface.SoundInterface()
    
    if len(sys.argv) == 2:
        transcriber = threading.Thread(target=si.mock_listen_for_hl, args=[si.transcription, event]) 
    else:
        transcriber = threading.Thread(target=si.listen_for_hl, args=[si.transcription, event])
    transcriber.start()
    
    while True:
        if event.is_set():
            
            # message = ' '.join(map(str, si.transcription.composition.values())) # message is the composition as a string
            latest_composition_index = max(si.transcription.composition.keys())
            message = si.transcription.composition[latest_composition_index]
            if PRINT:
                print(">>>>>>>>>>>> Composition updated. Composition["+str(latest_composition_index)+"]: '" + message + "'")
            co.interpret(message)
            event.clear()
        else:
            # no new messages
            pass
    
    
    
    
    transcriber.join()
