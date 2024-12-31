from task1 import task
from teleop import game
from pyniryo2 import *

from brain import predictor, brain_data

import os
import threading
import time


event = threading.Event()


model_path = "brain/best_model.statedict"
data_path = "brain/data"

"""
class Sleeper:
    def __init__(self, model, sub_feature):
        threading.Thread.__init__(self)
        self.model = model
        self.sub_feature = sub_feature
        
    def run(self):
        index = 0
        while True:
            index += 1
            time.sleep(.6)
            prediction = [[0.0,index]]
            prediction = self.model.predict(self.sub_feature[index])
            if prediction[0][1] > 0.5:
                #print("Prediction HIGH")
                event.set()
                continue
            else:
                pass
                #print("Not setting (output: " + str(prediction) + ")")
"""        

def thread(model, sub_feature):
    index = 0
    while True:
        index += 1
        time.sleep(.1) # change for testing purposes
        prediction = [[0.0,index]]
        prediction = model.predict(sub_feature[index])
        if prediction[0][1] > 0.5:
            event.set()
            print("From thread: ", event.is_set())
            continue
        else:
            print("From thread: ", event.is_set())
            event.clear()
            pass
            
            #print("Not setting (output: " + str(prediction) + ")")
    
        

if __name__ == "__main__":
    event.clear()
    print("(Re)instantiating Ned...")
    ned = NiryoRobot("169.254.200.201") # Assuming ethernet!
    ned.arm.calibrate_auto()
    ned.arm.set_arm_max_velocity(100) # change % for testing
    print("Loading model...")
    model = predictor.Predictor(model_path)
    print("Loading subject data...")
    sub_feature, __ = brain_data.read_subject_csv_binary(os.path.join(data_path, "sub_1.csv"), num_chunk_this_window_size=1488)
    print("Beginning!")
    th = threading.Thread(target=thread, args=[model, sub_feature])
    th.start()
    #sleeper = Sleeper(model, sub_feature)
    #sleeper.run() # comment out to prohibit switch
    while True:
        print("Teleoperation...")        
        g = game.Game(ned)
        switch = g.loop()
        while not event.is_set():
            switch = g.loop()

        print("Switching to autopilot...")
        ned.sound.play("beep.mp3")
        t = task.Task(ned, event) # initializes NiryoRobot
        t.start() # makes plan and executes it
        ned.sound.play("reboot.wav")
        event.clear()

    th.join()
    
