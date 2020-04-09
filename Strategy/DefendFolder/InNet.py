from math import atan2
from numpy import sign

from CowBotVector import Vec3
from GameState import Orientation
from Maneuvers import NavigateTo

def transition(game_info,
               next_states,
               sub_state_machine):

    ##########################
    
    def transition_to_far_boost(game_info):
        return False

    ##########################
    
    def transition_to_far_post(game_info):
        return False

    ##########################

    def transition_to_in_net(game_info):
        return False

    ##########################

    def transition_to_clear(game_info):
        if game_info.number_of_team_in_front_of_ball == 1:
            if game_info.ball_behind_teammate_zero:
                if not game_info.teammate_one_ball_side:
                    #If the teammate behind the ball is more on the ball side than we are, leave
                    return True
            elif game_info.ball_behind_teammate_one:
                if not game_info.teammate_zero_ball_side:
                    #If the teammate behind the ball is more on the ball side than we are, leave
                    return True

        elif game_info.number_of_team_in_front_of_ball == 0:
            if not (game_info.teammate_zero_ball_side or game_info.teammate_one_ball_side):
                return True

        return False

    ##########################

    def transition_to_save(game_info):
        if game_info.ball_prediction.check_on_net() == -1:
            return True
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

    ball_angle = atan2((game_info.ball.pos - game_info.me.pos).y,
                       (game_info.ball.pos - game_info.me.pos).x)
    rot = Orientation(pyr = [game_info.me.rot.pitch, ball_angle, game_info.me.rot.roll] )
    target_state = game_info.me.copy_state(pos = Vec3(0,-5120-60,0), rot = rot)
    controls = NavigateTo(game_info.me, target_state).input()

    if game_info.me.wheel_contact:
        if game_info.me.rot.roll > 0.15:
            controls.steer = 1
        elif game_info.me.rot.roll < - 0.15:
            controls.steer = -1

                    
    persistent = game_info.persistent
    return controls, persistent


