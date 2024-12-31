#import sound_interface
from unified_planning.shortcuts import *


def domain():
    problem = Problem("ObeyHuman")
    
    listened = problem.add_fluent("listened", BoolType(), default_initial_value=False)
    obeyed = problem.add_fluent("obeyed", BoolType(), default_initial_value=False)
    
    
    listen = DurativeAction("listen")
    listen.set_fixed_duration(10)
    listen.add_effect(StartTiming(), listened, False)
    listen.add_effect(EndTiming(), listened, True)
    problem.add_action(listen)
    
    obey = DurativeAction("obey")
    obey.add_condition(StartTiming(), listened)
    obey.set_fixed_duration(10)
    obey.add_effect(StartTiming(), obeyed, False)
    obey.add_effect(EndTiming(), obeyed, True)
    problem.add_action(obey)
    
    problem.add_goal(obeyed())
    
    return problem

if __name__ == "__main__":
    # a = sound_interface.
    problem = domain()
    with OneshotPlanner(problem_kind=problem.kind) as planner:
        result = planner.solve(problem).plan
    # switch for planner type
    # here just Tamer output
    for timed_action in result.timed_actions:
        print("Doing " + str(timed_action[1]) + " now!")
        

    
