from math import atan2, pi

from rlbot.agents.base_agent import SimpleControllerState
from rlutilities.mechanics import AerialTurn as RLU_AerialTurn

from Conversions import rot_to_mat3
from CowBotVector import Vec3
from GameState import Orientation

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_boost(game_info): #Could be a few of these
        return False

    ##########################

    def transition_to_jump(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################

    def transition_to_fast_dodge(game_info): #Could be a few of these
        return False

    ##########################

    def transition_to_aerial_rotation(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################

    def transition_to_turn(game_info): #Could be a few of these
        if game_info.me.wheel_contact:
            return True
        return False

    ##########################

    def transition_to_dodge(game_info): #Could be a few of these
        return False

    ##########################



    state_transitions = [transition_to_boost,
                         transition_to_jump,
                         transition_to_fast_dodge,
                         transition_to_aerial_rotation,
                         transition_to_turn,
                         transition_to_dodge]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            return next_states[i]

##########################################################################

def startup(game_info):

    state = None
    state_list = None

    persistent = game_info.persistent
    persistent.aerial_turn.action = RLU_AerialTurn(game_info.utils_game.my_car)
    target_rot = Orientation(pitch = pi/3,
                             yaw = game_info.me.rot.yaw,
                             roll = 0)
    persistent.aerial_turn.action.target = rot_to_mat3(target_rot, game_info.team_sign)

    return state, state_list, persistent

##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()

    persistent = game_info.persistent
    persistent.aerial_turn.action.step(game_info.dt)
    controls = persistent.aerial_turn.action.controls
    controls.boost = 1
    controls.steer = 1


    return controls, persistent
