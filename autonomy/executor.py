"""

Robot package imports

"""

import os
import sys

import threading

PRINT = True

class Executor:
    
    def __init__(self, robot=None, event_variable=None):
        self.robot_actual = True
        if not robot:
            try:
                connect_function() # will raise exception
                """
                
                Robot connection
                
                """
            except Exception as e:
                
                self.robot_actual = False #Mock
                self.robot = None
        else:
            self.robot = robot
            
        self.event = event_variable # potentially used for execution interruption

    """
    
    Plan primitive actions ( = robot motor commands)
    
    """

    def execute(self, plan):
        if PRINT:
            print("%%%%%%%%%%%%%% Plan Execution: %%%%%%%%%%%%%")

        """
        
        Setting
        
        """
        
        """
        
        Object Naming
        
        """
        
        for action in plan.actions:
            if self.robot_actual:
                if PRINT:
                    print("executing " + str(action))
                exec("self." + str(action))
            else:
                print('exec("self.' + str(action) + '")') # Targets action primitives
        if PRINT:
            print("Goal reached.")
            print("%%%%%%%%%%%%%% End Plan Execution: %%%%%%%%%%%%%")	

