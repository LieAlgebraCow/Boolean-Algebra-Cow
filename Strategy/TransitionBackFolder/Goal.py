from numpy import sign
from math import atan2

from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from GameState import Orientation
from Maneuvers import GroundTurn, NavigateTo

def transition(game_info,
               next_states,
               sub_state_machine):

    '''
    This state never transitions within the TransitionBack state above.
    If we're leaving this state, it's to enter a Defend state, which is done at a higher level.
    '''

    def transition_to_mid_boost(game_info): #Could be a few of these

        return False

    ##########################

    def transition_to_back_boost(game_info):

        return False

    ##########################

    def transition_to_boost_pad(game_info):

        return False


    ##########################

    def transition_to_goal(game_info):
        
        return False

    ##########################

    state_transitions = [transition_to_mid_boost,
                         transition_to_back_boost,
                         transition_to_boost_pad,
                         transition_to_goal]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            return next_states[i]

##########################################################################

def startup(game_info):

    state = None
    state_list = None

    persistent = game_info.persistent
    return state, state_list, persistent

##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()
    ball_x_sign = sign(game_info.ball.pos.x)

    ball_angle = atan2((game_info.ball.pos - game_info.me.pos).y,
                       (game_info.ball.pos - game_info.me.pos).x)
    rot = Orientation(pyr = [game_info.me.rot.pitch, ball_angle, game_info.me.rot.roll] )
    target_state = game_info.me.copy_state(pos = Vec3(-1450*ball_x_sign,-5120+140,0), rot = rot)
    controls = NavigateTo(game_info.me, target_state).input()

    persistent = game_info.persistent
    return controls, persistent

