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
        Location = UserType('Location')
        Thing = UserType('Thing')
          
        air = unified_planning.model.Fluent('air', BoolType(), l=Location)
        c_at = unified_planning.model.Fluent('c_at', BoolType(), l=Location)
        t_at = unified_planning.model.Fluent('t_at', BoolType(), l=Location, t=Thing)
        connected = unified_planning.model.Fluent('connected', BoolType(), l_from=Location, l_to=Location)
        carrying = unified_planning.model.Fluent('carrying', BoolType())
        notcarrying = unified_planning.model.Fluent('notcarrying', BoolType())
          
        move = unified_planning.model.InstantaneousAction('move', l_from=Location, l_to=Location)
        l_from = move.parameter('l_from')
        l_to = move.parameter('l_to')
        move.add_precondition(connected(l_from, l_to))
        move.add_precondition(c_at(l_from))
        move.add_effect(c_at(l_from), False)
        move.add_effect(c_at(l_to), True)
        move.add_effect(air(l_to), False)
        move.add_effect(air(l_from), True)
        
        receive = unified_planning.model.InstantaneousAction('receive', l=Location, o=Thing)
        l = receive.parameter('l')
        o = receive.parameter('o')
        receive.add_precondition(c_at(l))
        receive.add_precondition(t_at(l, o))
        receive.add_precondition(notcarrying())
        receive.add_effect(carrying(), True)
        receive.add_effect(notcarrying(), False)
        receive.add_effect(t_at(l, o), False)
      
        deliver = unified_planning.model.InstantaneousAction('deliver', l=Location, t=Thing)
        l = deliver.parameter('l')
        t = deliver.parameter('t')
        deliver.add_precondition(c_at(l))
        deliver.add_precondition(carrying())
        deliver.add_effect(notcarrying(), False)
        deliver.add_effect(carrying(), True)
        deliver.add_effect(t_at(l, t), True)
        
        """
        
        Instantiate and add objects
        
        """
        problem = unified_planning.model.Problem('minimal_problem')
        problem.add_fluent(c_at, default_initial_value=False)
        problem.add_fluent(t_at, default_initial_value=False)
        problem.add_fluent(connected, default_initial_value=False)
        problem.add_fluent(air, default_initial_value=True)
        problem.add_fluent(carrying, default_initial_value=False)
        problem.add_fluent(notcarrying, default_initial_value=True)
        
        problem.add_action(move)
        problem.add_action(receive)
        problem.add_action(deliver)

        a1 = unified_planning.model.Object('a1', Location)
        a2 = unified_planning.model.Object('a2', Location)
        a3 = unified_planning.model.Object('a3', Location)
        a4 = unified_planning.model.Object('a4', Location)
        b1 = unified_planning.model.Object('b1', Location)
        b2 = unified_planning.model.Object('b2', Location)
        b3 = unified_planning.model.Object('b3', Location)
        b4 = unified_planning.model.Object('b4', Location)
        c1 = unified_planning.model.Object('c1', Location)
        c2 = unified_planning.model.Object('c2', Location)
        c3 = unified_planning.model.Object('c3', Location)
        c4 = unified_planning.model.Object('c4', Location)
        
        problem.add_object(a1)
        problem.add_object(a2)
        problem.add_object(a3)
        problem.add_object(a4)
        problem.add_object(b1)
        problem.add_object(b2)
        problem.add_object(b3)
        problem.add_object(b4)
        problem.add_object(c1)
        problem.add_object(c2)
        problem.add_object(c3)
        problem.add_object(c4)
        
        """
        
        Goal testing
        
        """
        
        self.problem = problem
        self.plan = None
        
class Problem:
    def __init__(self, mp):
        
        self.problem = mp.problem.clone() # clone minimal problem

        # blocks_at_locations = mbsp.inventory.blocks_at_locations # again, for external inventory
        
        """
        
        Re-point to planning terms needed for goal and dynamic relations (e.g. over = mp.problem.fluent("over"))
        
        """
        
        Thing = self.problem.user_type('Thing')
        connected = self.problem.fluent('connected')
        air = self.problem.fluent("air")
        c_at = self.problem.fluent("c_at")
        t_at = self.problem.fluent("t_at")
        carrying = self.problem.fluent("carrying")
        notcarrying = self.problem.fluent("notcarrying")
        
        a1 = self.problem.object("a1")
        a2 = self.problem.object("a2")
        a3 = self.problem.object("a3")
        a4 = self.problem.object("a4")
        b1 = self.problem.object("b1")
        b2 = self.problem.object("b2")
        b3 = self.problem.object("b3")
        b4 = self.problem.object("b4")
        c1 = self.problem.object("c1")
        c2 = self.problem.object("c2")
        c3 = self.problem.object("c3")
        c4 = self.problem.object("c4")
        
        # Static relations ( doesn't need to be here... )
        self.problem.set_initial_value(connected(a1, a2), True)
        self.problem.set_initial_value(connected(a2, a3), True)
        self.problem.set_initial_value(connected(a3, a4), True)
        self.problem.set_initial_value(connected(a4, a3), True)
        self.problem.set_initial_value(connected(a3, a2), True)
        self.problem.set_initial_value(connected(a2, a1), True)
        self.problem.set_initial_value(connected(b1, b2), True)
        self.problem.set_initial_value(connected(b2, b3), True)
        self.problem.set_initial_value(connected(b3, b4), True)
        self.problem.set_initial_value(connected(b4, b3), True)
        self.problem.set_initial_value(connected(b3, b2), True)
        self.problem.set_initial_value(connected(b2, b1), True)
        self.problem.set_initial_value(connected(c1, c2), True)
        self.problem.set_initial_value(connected(c2, c3), True)
        self.problem.set_initial_value(connected(c3, c4), True)
        self.problem.set_initial_value(connected(c4, c3), True)
        self.problem.set_initial_value(connected(c3, c2), True)
        self.problem.set_initial_value(connected(c2, c1), True)
        self.problem.set_initial_value(connected(a4, b4), True)
        self.problem.set_initial_value(connected(b4, c4), True)
        self.problem.set_initial_value(connected(c4, b4), True)
        self.problem.set_initial_value(connected(b4, a4), True)
        
        """
        
        Add dynamic Objects
        
        """         
        thing = unified_planning.model.Object("thing", Thing)
        self.problem.add_object(thing)
        """
        
        Make "standardized" initial values (e.g.  problem.set_initial_value(g_at(a4), True))
        
        """
        self.problem.set_initial_value(c_at(a1), True)
        
        self.problem.set_initial_value(air(a1), False)
    
        """
        
        Dynamic Logical Setting
        
        """
        self.problem.set_initial_value(t_at(c4, thing), True)
        
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
