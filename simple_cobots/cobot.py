#!usr/bin/python3

import os
from time import sleep

from openai import OpenAI

from unified_planning.shortcuts import *
#from gpiozero import Servo

from autonomy import blockstacking, blockstacker

#servo = Servo(17)

client = OpenAI()

"""
All things we declare to be executable with "suggestively typed" args ==> unified_library search domain



"""
unified_library = ["sleep(seconds)", "print(text)", "self.blockstack_reverse_stack()", "self.move_block_to_pad()"] # search domain
unified_library_truncs = ["sleep", "print", "self.blockstack_reverse_stack", "self.move_block_to_pad"] # generated


PRINT = False
PRINT1 = True

class Collaboration:
    def __init__(self):
        pass
    
    def blockstack_reverse_stack(self):
        problem = blockstacking.BlockStackingProblem()
        
        p = problem.problem   
        p.add_goal(And(p.fluent("b_at")(p.object("block3"), p.object("a3")), p.fluent("b_at")(p.object("block2"), p.object("a2")), p.fluent("b_at")(p.object("block1"), p.object("a1"))))
        
        plan = problem.solve() # This planner too sp[ecific
        bstacker = blockstacker.BlockStacker()
        bstacker.execute(plan) # This executor too specific
        
    def move_block_to_pad(self):
        problem = blockstacking.BlockStackingProblem()

        p = problem.problem
        p.add_goal(And(p.fluent("b_at")(p.object("block2"), p.object("a1"))))
        
        plan = problem.solve()
        bstacker = blockstacker.BlockStacker()
        bstacker.execute(plan)        
            
    def interpret(self, message):

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
