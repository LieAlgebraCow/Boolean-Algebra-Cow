'''

This file will hold functions for choosing which path to take.  It will be intermediate
 between Cowculate and Maneuvers.

Arc_line_arc is the first pathing we use, but could be replaced later.

This entire file might be obsolete because RLU does it better

'''

from math import pi, asin, sqrt, acos, atan2

from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from Maneuvers import GroundTurn
from Mechanics import FrontDodge
from Miscellaneous import angles_are_close, cap_magnitude, min_radius, is_drivable_point

import GlobalRendering

#############################################################################################

#############################################################################################

class GroundPath:

    def __init__(self, current_state = None):
        self.length = None
        self.time_to_traverse = None
        self.waypoints = []
        self.current_state = current_state
        self.finished = False

        #A list of vec3 for the path
        self.discretized_path = None

        #The RLU Curve object for the path follower
        self.RLU_curve = None

    def input(self):
        '''
        Following a ground path.
        Doesn't currently do anything (obviously), but I want to check if there's a way to
        wrap up the RLU path following into here, because that would be convenient.
        All mechanical improvements to path following should be done within RLU at this point.
        '''
        pass

    #############################################################################################

    def path_is_out_of_bounds( self ):
        '''
        Returns a Boolean for whether or not the given goes outside the stadium.
        For now, we count walls and curves as out of bounds.
        '''

        for point in self.discretized_path:
            if is_drivable_point(point):
                continue
            else:
                return True
        return False
