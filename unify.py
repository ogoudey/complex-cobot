"""
cobot

A -> X -> C -> Y -> P

Collaborator.loop( take audio input )

"""


from simple_cobots import cobot
from cog_arch import sound_interface

import threading

if __name__ == "__main__":

    event = threading.Event()

    co = cobot.Collaboration()
    si = sound_interface.SoundInterface()
    
    transcriber = threading.Thread(target=si.listen_for_hl, args=[si.transcription, event])
    transcriber.start()
    
    while True:
        if event.is_set():
            
            # message = ' '.join(map(str, si.transcription.composition.values())) # message is the composition as a string
            latest_composition_index = max(si.transcription.composition.keys())
            message = si.transcription.composition[latest_composition_index]
            print(">>>>>>>>>>>> Composition updated. Composition["+str(latest_composition_index)+"]: '" + message + "'")
            co.interpret(message)
            event.clear()
        else:
            # no new messages
            pass
    
    
    
    
    transcriber.join()
