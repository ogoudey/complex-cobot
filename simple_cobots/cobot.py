import os
from time import sleep
import random # for block selection - no good.

from openai import OpenAI

#from unified_planning.shortcuts import * # dont need

# generic classes
from autonomy import planner, executor

# blockstacking with Ned2
from autonomy import blockstacking, blockstacker



client = OpenAI()

"""

All things we declare to be executable with "suggestively typed" args. The unified_library search domain. E.g.:

unified_library = ["sleep(seconds)", "print(text)", "self.move_block_to_pad()"] # search domain
unified_library_truncs = ["sleep", "print",  "self.move_block_to_pad"] # generated

"""
unified_library = ["sleep(seconds)", "print(text)", "self.move_block_to_pad()"] # search domain
unified_library_truncs = ["sleep", "print",  "self.move_block_to_pad"] # generated


PRINT = True
PRINT1 = True

class Collaboration:
    def __init__(self):
        self.minimal_problem = planner.MinimalProblem()
    
    """
    
    Complex actions
    
    """
    
            
    def interpret(self, message, bypassLLM=False):
        if not bypassLLM:
            prompt = 'Here is a user message: "' + message + '"\nRespond with corresponding and necessary function calls from this set: \n' + str(unified_library) + "."
            if PRINT:
                print("$$$$$$$$$$$Prompting:$$$$$$$$$$$$$$")
                print('Prompting with:\n\n' + prompt +"\n")
            completion = client.chat.completions.create(
              model="gpt-4o",
              messages=[
                {"role": "system", "content": "You execute precise function calls for a user."},
                {"role": "user", "content": prompt}
              ]
            )
            if PRINT:
                print("$$$$$$$$$$$End Prompting$$$$$$$$$$$$$$")
            text = completion.choices[0].message.content
            if PRINT:
                print("\n~~~~~~~~~~~~~~~~~Response:~~~~~~~~~~~~~~~~~")
                print(text)
                print("~~~~~~~~~~~~~~~~~End Response:~~~~~~~~~~~~~~~~~\n")
        else: # Bypass LLM
            text = "self.minimal_problem"
        # Actualizing
        
        # words = text.replace(",","").replace("\n", " ").split(' ') Method 1
        if PRINT1:
            print(".................Interpretation...............")
        words = text.split("\n")
        executions = []
        for w in words:
                if PRINT1:
                    print("Word: " + w, end="")
                index = w.find("(")
                if index != -1:
                        w_trunc = w[:index]
                        if w_trunc in unified_library_truncs:
                            if PRINT1:
                                print(" = Hit!")
                            executions.append(w)
                        else:
                            if PRINT1:
                                print(" = Miss!")
                            pass # just another word
                else:
                    if PRINT1:
                        print(" = Does not contain a function!")
        if PRINT1:
            print(".............End Interpretation.............")
        #print("(Executions:)\n" + str(executions))
        if PRINT:
            print("++++++++++Executing:+++++++++++")
        for x in executions:
            try:
                if PRINT:
                    print("Executing " + x)
                exec(x)
                if PRINT:
                    print("         |_____executed " + x + "__")
            except Exception as e:
                if PRINT:
                    print(e) 
                    print("^^^ Ignoring error potential execution " + x + "...)")
        if PRINT:
            print("++++++++++End Executing+++++++++++")
