import os
from time import sleep

from openai import OpenAI

from unified_planning.shortcuts import *

from autonomy import planner, executor


client = OpenAI()

PRINT = True
PRINT1 = True

class Collaboration:
    def __init__(self):
        self.unified_library = ["sleep(seconds)", "print(text)"] # generic search domain
        self.unified_library_truncs = ["sleep", "print"] # generic derivative
    
    # Change this to test specific funtions from the search domain
    def default_uninterpreted_function(self):
        return "self.print('Hello world')"
                
    def interpret(self, message, bypassLLM=False):
        if not bypassLLM:
            prompt = 'Here is a user message: "' + message + '"\nRespond with corresponding and necessary function calls from this set: \n' + str(self.unified_library) + "."
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
            text = self.default_uniterpreted_funtion()
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
                        if w_trunc in self.unified_library_truncs:
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
            
            
            
            
            

class CarCollaboration(Collaboration):
    def __init__(self, state):
        super().__init__()
        self.minimal_problem = planner.MinimalCarProblem()
        self.state = state
        
        self.unified_library += ["self.receive_thing()", "self.move()", "self.deliver_thing()"] # search domain
        self.unified_library_truncs += ["self.receive_thing", "self.move", "self.deliver_thing"] # derivative
        
        self.executor = executor.CarExecutor(self.state)
        
    """

    Complex actions

    """
    def move(self):
        prob = planner.CarProblem(self.minimal_problem, self.state)
        prob.problem.add_goal(prob.problem.fluent('c_at')(prob.problem.object("c4")))
        
        plan = prob.solve()

        self.executor.execute(plan)
        
    def deliver_thing(self):
        prob = planner.CarProblem(self.minimal_problem, self.state)
        prob.problem.add_goal(prob.problem.fluent('t_at')(prob.problem.object("c1"), prob.problem.object('thing')))
    
        plan = prob.solve()

        self.executor.execute(plan)
        
    def receive_thing(self):
        prob = planner.CarProblem(self.minimal_problem, self.state)
        prob.problem.add_goal(And(prob.problem.fluent('c_at')(prob.problem.object("c4")), prob.problem.fluent('carrying')))
    
        plan = prob.solve()
        
        self.executor.execute(plan)
        
class ArmCollaboration(Collaboration):   
    def __init__(self):
        super().__init__()
        self.minimal_problem = planner.MinimalBlockStackingProblem()

        self.unified_library += ["self.blockstack_restack()", "self.move_block_to_pad()"] # search domain
        self.unified_library_truncs += ["self.blockstack_restack", "self.move_block_to_pad"] # derivative
        
        self.bstacker = executor.NedExecutor()
    
    def blockstack_restack(self):
        problem = planner.BlockStackingProblem(self.minimal_problem)

        p = problem.problem   
        p.add_goal(And(p.fluent("b_at")(p.object("block3"), p.object("a3")), p.fluent("b_at")(p.object("block2"), p.object("a2")), p.fluent("b_at")(p.object("block1"), p.object("a1"))))

        plan = problem.solve() # This planner too sp[ecific
        bstacker = executor.BlockStacker()
        self.bstacker.execute(plan) # This executor too specific

    def move_block_to_pad(self):
        problem = planner.BlockStackingProblem(self.minimal_problem)

        p = problem.problem
        p.add_goal(And(p.fluent("b_at")(p.object("block2"), p.object("a1"))))

        plan = problem.solve()

        self.bstacker.execute(plan)        
