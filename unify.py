"""
cobot

A -> X -> C -> Y -> P

Collaborator.loop( take audio input )

"""
PRINT = False

from simple_cobots import cobot
from cog_arch import sound_interface
from cog_arch import state

import sys
import threading
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument('-d', '--deaf', action='store_true')         
    parser.add_argument('-b', '--bypassLLM', action='store_true')   
       
    args = parser.parse_args()
        
    event = threading.Event()
    
    s = state.SimpleState()
    co = cobot.Collaboration(s)
    si = sound_interface.SoundInterface()
    
    if args.deaf:
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
            co.interpret(message, args.bypassLLM)
            event.clear()
        else:
            # mainloop room
            pass
    
    
    
    
    transcriber.join()
