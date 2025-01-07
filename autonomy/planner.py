import unified_planning
from unified_planning.shortcuts import *

up.shortcuts.get_environment().credits_stream = None # to remove credits from print

PRINT = True

#from inventory import tracker

class MinimalProblem:
    def __init__(self, domain=None):
        #self.inventory = tracker.InventoryTracker() # Additional planning thing
        
        """
        
        Planning Domain
        
        """
      
        """
        
        Instantiate and add objects
        
        """

        """
        
        Goal testing
        
        """
        
        self.problem = None
        self.plan = None
        
class Problem:
    def __init__(self, mp):
        
        self.problem = mp.problem.clone() # clone minimal problem

        # blocks_at_locations = mbsp.inventory.blocks_at_locations # again, for external inventory
        
        """
        
        Re-point to planning terms needed for goal and dynamic relations (e.g. over = mp.problem.fluent("over"))
        
        """
       
        """
        
        Add Objects
        
        """         
        
        """
        
        Make "standardized" initial values (e.g.  problem.set_initial_value(g_at(a4), True))
        
        """

        """
        
        Dynamic Logical Setting
        
        """
        
        
    def add_goal(self, call_str):
        exec(call_str)
    
    def solve(self):
        problem = self.problem
        if PRINT:
            print("?????????????Planning:?????????????")
        with OneshotPlanner(problem_kind=problem.kind) as planner:
            result = planner.solve(problem)
            if PRINT:
                print("%s returned: %s" % (planner.name, result.plan))
        if PRINT:
            print("?????????????End Planning:?????????????")    
        self.plan = result.plan
        return result.plan
