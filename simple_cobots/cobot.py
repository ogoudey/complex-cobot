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
        print("$$$$$$$$$$$Prompting:$$$$$$$$$$$$$$")
        print('Prompting with:\n\n' + prompt +"\n")
        completion = client.chat.completions.create(
          model="gpt-4o",
          messages=[
            {"role": "system", "content": "You execute precise function calls for a user."},
            {"role": "user", "content": prompt}
          ]
        )
        print("$$$$$$$$$$$End Prompting$$$$$$$$$$$$$$")
        text = completion.choices[0].message.content
        print("\n~~~~~~~~~~~~~~~~~Response:~~~~~~~~~~~~~~~~~")
        print(text)
        print("~~~~~~~~~~~~~~~~~End Response:~~~~~~~~~~~~~~~~~\n")
        # Actualizing
        
        # words = text.replace(",","").replace("\n", " ").split(' ') Method 1
        words = text.split("\n")
        executions = []
        for w in words:
                print("Word: " + w, end="")
                index = w.find("(")
                if index != -1:
                        w_trunc = w[:index]
                        if w_trunc in unified_library_truncs:
                                print(" = hit!")
                                executions.append(w)
                        else:
                                print(" = miss!")
                                pass # just another word
                else:
                        print(" = not a function!")
        print("\n")
        #print("(Executions:)\n" + str(executions))
        print("++++++++++Executing:+++++++++++")
        for x in executions:
                try:
                        print("Executing " + x)
                        exec(x)
                        print("         |_____executed " + x + "__")
                except Exception as e:
                        
                        print(e)
                        print("^^^ Ignoring error potential execution " + x + "...)")
        print("++++++++++End Executing+++++++++++")
