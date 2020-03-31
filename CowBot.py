from functools import partial
from math import pi, ceil
import random

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

import rlutilities as utils
from rlutilities.mechanics import AerialTurn as RLU_AerialTurn
from rlutilities.mechanics import Aerial as RLU_Aerial
from rlutilities.mechanics import Dodge as RLU_Dodge
from rlutilities.mechanics import FollowPath as RLU_FollowPath
from rlutilities.simulation import Curve

from BallPrediction import PredictionPath, ball_contact_binary_search
from Conversions import Vec3_to_vec3, rot_to_mat3
from Cowculate import Cowculate 
from GameState import BallState, CarState, GameState, Hitbox, Orientation
from Kickoffs.Kickoff import Kickoff, update_kickoff_position
from Mechanics import PersistentMechanics, FrontDodge
from Miscellaneous import predict_for_time
from Pathing.PathPlanning import shortest_arclinearc
import Strategy

#A flag for testing code.
#When True, all match logic will be ignored.
#Planning will still take place, but can be overridden,
#and no action will be taken outside of the "if TESTING:" blocks.

TESTING = False
DEBUGGING = False
if TESTING or DEBUGGING:
    import random
    from math import sqrt

    import GlobalRendering #Only needed for rendering.
    from StateSetting import *
    from BallPrediction import *
    from Mechanics import CancelledFastDodge, aerial_rotation
    from Maneuvers import GroundTurn
    from Pathing.ArcLineArc import ArcLineArc
    from Simulation import *
    import Kickoffs.Fast_Kickoffs

class BooleanAlgebraCow(BaseAgent):

    '''
    This is the class within which our entire bot lives.
    Anything not saved to an attribute of this class will be deleted after an input for the frame is returned.
    The only methods of this class that we use are to get information from the framework, like field info or rigid body tick
    '''

    def initialize_agent(self):
        #This runs once before the bot starts up
        self.is_init = True
        self.teammate_indices = []
        self.opponent_indices = []

        self.game_info = None
        self.kickoff_position = "Other"
        self.kickoff_data = None
        self.jumped_last_frame = None
        self.path_state = 'Reset'
        self.path = None
        self.waypoint_index = 2

        self.plan = None
        self.old_kickoff_data = None
        self.utils_game = None
        self.old_inputs = SimpleControllerState()

        #This will be used to remember opponent actions.  Maybe load in opponent bots preemptively one day?
        self.memory = None
        #These are used to specify or set states in the code.
        self.zero_ball_state = BallState(pos = None,
                                         rot = None,
                                         vel = None,
                                         omega = None,
                                         latest_touch = None,
                                         hit_location = None)
        self.zero_car_state = CarState(pos = None,
                                       rot = None,
                                       vel = None,
                                       omega = None,
                                       demo = None,
                                       wheel_contact = None,
                                       supersonic = None,
                                       jumped = None,
                                       double_jumped = None,
                                       boost = None,
                                       jumped_last_frame = None)
        self.persistent = PersistentMechanics()
        self.my_timer = 0
        
        #Put testing-only variables here
        if TESTING:
            self.state = 'RESET'
            self.target_loc = None
            self.target_time = None
            self.takeoff_time = None
            self.start_time = None
            self.old_game_info = None
            self.dodge = None
            self.path_target = None

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        ###############################################################################################
        #Startup info - run once at start
        ###############################################################################################

        #Initialization info
        if self.is_init:
            self.is_init = False
            self.field_info = self.get_field_info()
            self.match_settings = self.get_match_settings()
 
            #Find teammates and opponents
            self.teammate_indices = []
            self.opponent_indices = []
    
            for i in range(packet.num_cars):
                if i == self.index:
                    pass
                elif packet.game_cars[i].team == self.team:
                    self.teammate_indices.append(i)
                else:
                    self.opponent_indices.append(i)

            self.utils_game = utils.simulation.Game(self.index, self.team)
            utils.simulation.Game.set_mode("soccar")

            if TESTING or DEBUGGING:
                GlobalRendering.renderer = self.renderer


        ###############################################################################################
        #Prediction and Game state info
        ###############################################################################################

        self.prediction = PredictionPath(ball_prediction = self.get_ball_prediction_struct(),
                                         source = "Framework",
                                         team = self.team,
                                         utils_game = self.utils_game,
                                         condition = lambda slices: len(slices) < 360)

        #Game state info
        self.game_info = GameState( packet = packet,
                                    utils_game = self.utils_game,
                                    field_info = self.field_info,
                                    match_settings = self.match_settings,
                                    my_index = self.index,
                                    my_team = self.team,
                                    ball_prediction = self.prediction,
                                    teammate_indices = self.teammate_indices,
                                    opponent_indices = self.opponent_indices,
                                    my_old_inputs = self.old_inputs,
                                    rigid_body_tick = self.get_rigid_body_tick() )

        ###############################################################################################
        #Planning
        ###############################################################################################

        if not TESTING:
            self.top_level_decisions.update()
            return self.top_level_decisions.get_controls()
            

        ###############################################################################################
        #Update RLU Mechanics as needed
        ###############################################################################################

        #If we're in the first frame of an RLU mechanic, start up the object.
        #If we're finished with it, reset it to None
        self.persistent = update_RLU_mechanics(self.persistent, self.game_info)


        ###############################################################################################
        #Testing 
        ###############################################################################################

        if TESTING:

            #Copy-paste from a testing file here
            output = SimpleControllerState()
            current_state = self.game_info.me

            ###

            #Reset the testing position
            if self.state == 'RESET':
                output = SimpleControllerState()
                self.my_timer = 0
                self.RESET = False                    
                
                #Reset to a stationary setup when the bot is reloaded
                ball_pos = Vec3(0, 1500, 120)
                ball_state = self.zero_ball_state.copy_state(pos = Vec3(0,0,92.75),
                                                             vel = Vec3(0,0,0),
                                                             omega = Vec3(0,0,0))

                #Set car state
                car_pos = Vec3(256, -3840, 18.65)
                car_vel = Vec3(0, 0, 0)
                car_state = self.zero_car_state.copy_state(pos = car_pos,
                                                           vel = car_vel,
                                                           rot = Orientation(pitch = 0,
                                                                             yaw = pi/2,
                                                                             roll = 0),
                                                           boost = 100)
                self.set_game_state(set_state(self.game_info,
                                              current_state = car_state,
                                              ball_state = ball_state))

                self.state = 'WAIT'

            ###

            elif self.state == 'WAIT':
                self.my_timer += 0.00833
                #Wait for state setting to work
                output = SimpleControllerState()
                if self.my_timer < 0.2:
                    pass

                else:
                    self.state = 'KICKOFF'

            ###

            elif self.state == 'KICKOFF':
                output, self.persistent = Kickoffs.Fast_Kickoffs.offcenter(self.game_info,
                                                                          -1,
                                                                          self.persistent)            

            self.old_inputs = output
            return output


            #####################################
            #End of frame stuff that needs to be in the testing block as well
            if output.throttle == 0:
                output.throttle = 0.01
                
            #Making sure that RLU output is interpreted properly as an input for RLBot
            framework_output = SimpleControllerState()
            framework_output.throttle = output.throttle
            framework_output.steer = output.steer
            framework_output.yaw = output.yaw
            framework_output.pitch = output.pitch
            framework_output.roll = output.roll
            framework_output.boost = output.boost
            framework_output.handbrake = output.handbrake
            framework_output.jump = output.jump
            return framework_output


        ###############################################################################################
        #Run either Kickoff or Cowculate
        ###############################################################################################

        if self.game_info.is_kickoff_pause == True:
            if self.old_kickoff_data != None:
                self.kickoff_data = Kickoff(self.game_info,
                                            self.kickoff_position,
                                            self.old_kickoff_data.memory,
                                            self.persistent)
            else:
                self.kickoff_data = Kickoff(self.game_info,
                                            self.kickoff_position,
                                            None,
                                            self.persistent)

            output, self.persistent = self.kickoff_data.input()

        else:
            output, self.persistent = Cowculate(self.plan,
                                                self.game_info,
                                                self.prediction,
                                                self.persistent)

        ###############################################################################################
        #Update previous frame variables and return
        ###############################################################################################

        self.old_kickoff_data = self.kickoff_data
        self.old_inputs = output

        #Make sure we don't get stuck turtling. Not sure how effective this is.
        if output.throttle == 0:
            output.throttle = 0.01

        #Making sure that RLU output is interpreted properly as an input for RLBot
        framework_output = finalize_output(output)
        return framework_output


###############################################################################################
#
###############################################################################################

def finalize_output(output):
    framework_output = SimpleControllerState()
    framework_output.throttle = output.throttle
    framework_output.steer = output.steer
    framework_output.yaw = output.yaw
    framework_output.pitch = output.pitch
    framework_output.roll = output.roll
    framework_output.boost = output.boost
    framework_output.handbrake = output.handbrake
    framework_output.jump = output.jump

    return framework_output

###############################################################################################


def update_RLU_mechanics(persistent,
                         game_info):

    if persistent.aerial_turn.initialize:
        persistent.aerial_turn.initialize = False
        persistent.aerial_turn.action = RLU_AerialTurn(game_info.utils_game.my_car)
        persistent.aerial_turn.action.target = rot_to_mat3(persistent.aerial_turn.target_orientation, game_info.team_sign)
    elif not persistent.aerial_turn.check:
        persistent.aerial_turn.action = None
    persistent.aerial_turn.check = False
    ###
    if persistent.aerial.initialize:
        persistent.aerial.initialize = False
        persistent.aerial.action = RLU_Aerial(game_info.utils_game.my_car)
        persistent.aerial.action.target = Vec3_to_vec3(persistent.aerial.target_location, game_info.team_sign)
        persistent.aerial.action.arrival_time = persistent.aerial.target_time
        persistent.aerial.action.up = Vec3_to_vec3(persistent.aerial.target_up, game_info.team_sign)
    elif not persistent.aerial.check:
        persistent.aerial.action = None
    persistent.aerial.check = False
    ###
    if not persistent.path_follower.check:
        persistent.path_follower.action = None
    persistent.path_follower.check = False
    ###
    if not persistent.dodge.check:
        persistent.dodge.action = None
    persistent.dodge.check = False

    return persistent
