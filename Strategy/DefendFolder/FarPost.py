from math import atan2
from numpy import sign

from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from GameState import Orientation
from Maneuvers import NavigateTo

########################################################################################################
#States for the next level down
########################################################################################################



########################################################################################################
#Transition functions
########################################################################################################


def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_far_boost(game_info):
        return False

    ##########################

    
    def transition_to_far_post(game_info):
        return False

    ##########################

    def transition_to_in_net(game_info):
        if not game_info.teammate_in_net:
            return True
        return False

    ##########################

    def transition_to_clear(game_info):
        if sign(game_info.ball.pos.x) == sign(game_info.me.pos.x): #If we're on ball side
            teammate_our_side = False
            for mate in game_info.teammates:
                if sign(mate.pos.x) == sign(game_info.me.pos.x): #If there's a teammate also on our side
                    if mate.pos.y > game_info.ball.pos.y: #and they're not behindthe ball, go for ball
                        teammate_our_side = True
            if not teammate_our_side:
                return True

        return False 

    ##########################

    def transition_to_save(game_info):
        return False
    
    ##########################

    state_transitions = [transition_to_far_boost,
                         transition_to_far_post,
                         transition_to_in_net,
                         transition_to_clear,
                         transition_to_save]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            #Clear any RLU objects used
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

    ball_angle = atan2((game_info.ball.pos - game_info.me.pos).y,
                       (game_info.ball.pos - game_info.me.pos).x)
    rot = Orientation(pyr = [game_info.me.rot.pitch, ball_angle, game_info.me.rot.roll] )
    target_state = game_info.me.copy_state(pos = Vec3(-1050*game_info.ball_x_sign,-5120+140,0), rot = rot)

    controls = NavigateTo(game_info.me, target_state).input()
    persistent = game_info.persistent
    return controls, persistent
