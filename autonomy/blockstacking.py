import unified_planning
from unified_planning.shortcuts import *

up.shortcuts.get_environment().credits_stream = None

PRINT = True

from inventory import tracker

class MinimalBlockStackingProblem:
    def __init__(self, domain=None):
        self.inventory = tracker.InventoryTracker()
        
        # create domain
        
        
        Location = UserType('Location')
        Block = UserType('Block')
        self.usertypes = [Block, Location]
        
        
        
        hoverable = unified_planning.model.Fluent('hoverable', BoolType(), l=Location)
        
        air = unified_planning.model.Fluent('air', BoolType(), l=Location)

        g_at = unified_planning.model.Fluent('g_at', BoolType(), l=Location)
        b_at = unified_planning.model.Fluent('b_at', BoolType(), b=Block, l=Location)

        connected = unified_planning.model.Fluent('connected', BoolType(), l_from=Location, l_to=Location)
        over = unified_planning.model.Fluent('over', BoolType(), l_over=Location, l_under=Location)
        closed = unified_planning.model.Fluent('closed', BoolType())
        grasped = unified_planning.model.Fluent('grasped', BoolType(), b=Block)
        ungrasped = unified_planning.model.Fluent('ungrasped', BoolType())
        is_on_floor = unified_planning.model.Fluent('is_on_floor', BoolType(), l=Location)

        
        move = unified_planning.model.InstantaneousAction('move', l_from=Location, l_to=Location)
        l_from = move.parameter('l_from')
        l_to = move.parameter('l_to')
        move.add_precondition(connected(l_from, l_to))
        move.add_precondition(g_at(l_from))
        move.add_precondition(ungrasped()) # conceptual, necessary
        move.add_precondition(hoverable(l_to))
        move.add_effect(g_at(l_from), False)
        move.add_effect(g_at(l_to), True)
        
        carry = unified_planning.model.InstantaneousAction('carry', b=Block, l_from=Location, l_to=Location)
        b = carry.parameter('b')
        l_from = carry.parameter('l_from')
        l_to = carry.parameter('l_to')
        carry.add_precondition(connected(l_from, l_to))
        carry.add_precondition(g_at(l_from))
        carry.add_precondition(b_at(b, l_from))
        carry.add_precondition(grasped(b))
        carry.add_precondition(air(l_to))
        carry.add_effect(g_at(l_from), False)
        carry.add_effect(g_at(l_to), True)
        carry.add_effect(b_at(b, l_from), False)
        carry.add_effect(b_at(b, l_to), True)
    
        
        close = unified_planning.model.InstantaneousAction('close', l=Location)
        l = close.parameter('l')
        close.add_effect(closed(), True)
        
        grasp = unified_planning.model.InstantaneousAction('grasp', b=Block, l_over=Location, l_under=Location)
        b = grasp.parameter('b')
        l_over = grasp.parameter('l_over')
        l_under = grasp.parameter('l_under')
        grasp.add_precondition(over(l_over, l_under))
        grasp.add_precondition(g_at(l_over))
        grasp.add_precondition(b_at(b, l_over))
        grasp.add_precondition(ungrasped())
        grasp.add_effect(air(l_over), True)
        grasp.add_effect(grasped(b), True)
        grasp.add_effect(ungrasped(), False)
        grasp.add_effect(hoverable(l_under), True)        
        
        grasp_on_floor = unified_planning.model.InstantaneousAction('grasp_on_floor', b=Block, l=Location)
        b = grasp_on_floor.parameter('b')
        l = grasp_on_floor.parameter('l')
        grasp_on_floor.add_precondition(is_on_floor(l))
        grasp_on_floor.add_precondition(g_at(l))
        grasp_on_floor.add_precondition(b_at(b, l))
        grasp_on_floor.add_precondition(ungrasped())
        grasp_on_floor.add_effect(grasped(b), True)
        grasp_on_floor.add_effect(ungrasped(), False)

        stack = unified_planning.model.InstantaneousAction('stack', b1=Block, l1=Location, b2=Block, l2=Location)
        b1 = stack.parameter("b1")
        l1 = stack.parameter("l1")
        b2 = stack.parameter("b2")
        l2 = stack.parameter("l2")
        stack.add_precondition(over(l1, l2))
        stack.add_precondition(b_at(b1, l1))
        stack.add_precondition(b_at(b2, l2))
        stack.add_precondition(grasped(b1)) # and g_at l1
        stack.add_effect(grasped(b1), False)
        stack.add_effect(air(l1), False)
        stack.add_effect(hoverable(l1), True)
        stack.add_effect(hoverable(l2), False)
        stack.add_effect(ungrasped(), True)
        
        floor = unified_planning.model.InstantaneousAction('floor', b=Block, l_1=Location)
        b = floor.parameter('b')
        l_1 = floor.parameter('l_1')
        floor.add_precondition(is_on_floor(l_1))
        floor.add_precondition(grasped(b))
        floor.add_precondition(g_at(l_1)) 
        floor.add_precondition(b_at(b, l_1)) # may be redundant
        floor.add_effect(grasped(b), False)
        floor.add_effect(ungrasped(), True)
        floor.add_effect(air(l_1), False)
        floor.add_effect(hoverable(l_1), True)

        
        
        #instantiate objects
        problem = unified_planning.model.Problem('minimal_problem')
        problem.add_fluent(g_at, default_initial_value=False)
        problem.add_fluent(hoverable, default_initial_value=True)
        problem.add_fluent(b_at, default_initial_value=False)
        problem.add_fluent(connected, default_initial_value=False)
        problem.add_fluent(over, default_initial_value=False)
        problem.add_fluent(closed, default_initial_value=False)
        problem.add_fluent(grasped, default_initial_value=False)
        problem.add_fluent(ungrasped, default_initial_value=True)
        problem.add_fluent(is_on_floor, default_initial_value=False)
        problem.add_fluent(air, default_initial_value=True)
        self.fluents = [g_at, hoverable, b_at, connected, over, closed, grasped, ungrasped, is_on_floor, air]
        
        problem.add_action(move)
        problem.add_action(close)
        problem.add_action(carry)
        problem.add_action(grasp)
        problem.add_action(grasp_on_floor)
        #problem.add_action(drop)
        problem.add_action(floor)
        problem.add_action(stack)
        self.actions = [move, close, carry, grasp, grasp_on_floor, floor, stack]
        
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
        
        """
        block1 = unified_planning.model.Object('block1', Block)
        block2 = unified_planning.model.Object('block2', Block)
        block3 = unified_planning.model.Object('block3', Block)
        """
        
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
        self.static_objects = [a1, a2, a3, a4, b1, b2, b3, b4, c1, c2, c3, c4]
        
        """
        problem.add_object(block1)
        problem.add_object(block2)
        problem.add_object(block3)
        """
        
        
        #   Testing:
        #problem.add_goal(And(g_at(c3)))
        #problem.add_goal(And(grasped(block3)))
        #problem.add_goal(And(b_at(block3, a1), b_at(block2, a2), g_at(a3)))
        #problem.add_goal(And(b_at(block3, a1), ungrasped()))
        #problem.add_goal(And(b_at(block3, a3), b_at(block2, a2), b_at(block1, a1), g_at(a4)))
        
        
        
        
        self.problem = problem
        self.plan = None
        #print(problem)
        
        self.children = []
        
class BlockStackingProblem:
    def __init__(self, mbsp):
        # duplicate minimal stacking problem
        self.problem = mbsp.problem.clone()

        
        blocks_at_locations = mbsp.inventory.blocks_at_locations
        
        
        p = self.problem # shorthand
        
        # Re-point to NEEDED planning terms
        Block = p.user_type("Block")
        
        connected = p.fluent("connected")
        over = p.fluent("over")
        is_on_floor = p.fluent("is_on_floor")
        air = p.fluent("air")
        g_at = p.fluent("g_at")
        hoverable = p.fluent("hoverable")
        b_at = p.fluent("b_at")
        grasped = p.fluent("grasped")
        
        a1 = p.object("a1")
        a2 = p.object("a2")
        a3 = p.object("a3")
        a4 = p.object("a4")

        b1 = p.object("b1")
        b2 = p.object("b2")
        b3 = p.object("b3")
        b4 = p.object("b4")

        c1 = p.object("c1")
        c2 = p.object("c2")
        c3 = p.object("c3")
        c4 = p.object("c4")


        
        # Add objects
        for block_str in blocks_at_locations.keys():
            b = unified_planning.model.Object(block_str, Block)
            p.set_initial_value(b_at(b, p.object(blocks_at_locations[block_str])), True)           
            p.set_initial_value(grasped(b), False)

            p.add_object(b)

        problem = p # again, shorthand 
        # Static relations
        problem.set_initial_value(connected(a1, a2), True)
        problem.set_initial_value(connected(a2, a3), True)
        problem.set_initial_value(connected(a3, a4), True)
        problem.set_initial_value(connected(a4, a3), True)
        problem.set_initial_value(connected(a3, a2), True)
        problem.set_initial_value(connected(a2, a1), True)
        problem.set_initial_value(connected(b1, b2), True)
        problem.set_initial_value(connected(b2, b3), True)
        problem.set_initial_value(connected(b3, b4), True)
        problem.set_initial_value(connected(b4, b3), True)
        problem.set_initial_value(connected(b3, b2), True)
        problem.set_initial_value(connected(b2, b1), True)
        problem.set_initial_value(connected(c1, c2), True)
        problem.set_initial_value(connected(c2, c3), True)
        problem.set_initial_value(connected(c3, c4), True)
        problem.set_initial_value(connected(c4, c3), True)
        problem.set_initial_value(connected(c3, c2), True)
        problem.set_initial_value(connected(c2, c1), True)
        problem.set_initial_value(connected(a4, b4), True)
        problem.set_initial_value(connected(b4, c4), True)
        problem.set_initial_value(connected(c4, b4), True)
        problem.set_initial_value(connected(b4, a4), True)
        problem.set_initial_value(over(a4,a3), True)
        problem.set_initial_value(over(a3,a2), True)
        problem.set_initial_value(over(a2,a1), True)
        problem.set_initial_value(over(b4,b3), True)
        problem.set_initial_value(over(b3,b2), True)
        problem.set_initial_value(over(b2,b1), True)
        problem.set_initial_value(over(c4,c3), True)
        problem.set_initial_value(over(c3,c2), True)
        problem.set_initial_value(over(c2,c1), True)
        problem.set_initial_value(is_on_floor(a1), True)
        problem.set_initial_value(is_on_floor(b1), True)
        problem.set_initial_value(is_on_floor(c1), True)
        
        problem.set_initial_value(air(a4), True)
        problem.set_initial_value(air(a3), True)
        problem.set_initial_value(air(a2), True)
        problem.set_initial_value(air(a1), True)
        problem.set_initial_value(air(b4), True)
        problem.set_initial_value(air(b3), True)
        problem.set_initial_value(air(b2), True)
        problem.set_initial_value(air(b1), True)
        problem.set_initial_value(air(c4), True)
        problem.set_initial_value(air(c3), True)
        problem.set_initial_value(air(c2), False)
        problem.set_initial_value(air(c1), False)
        
        # Dynamic relations
        # Standardized
        problem.set_initial_value(g_at(a4), True)

        # logical domain setting
        problem.set_initial_value(hoverable(c1), False)
        problem.set_initial_value(hoverable(c2), True)
        problem.set_initial_value(hoverable(b1), True)
        
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
        
    # these should be in a higher level, somewhat legible acting
    

