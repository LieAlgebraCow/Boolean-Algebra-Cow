from math import pi
from numpy import sign

from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from Mechanics import CancelledFastDodge

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_boost(game_info):
        return False

    ##########################

    def transition_to_jump(game_info):
        return False

    ##########################

    def transition_to_fast_dodge(game_info):
        return False

    ##########################

    def transition_to_aerial_rotation(game_info):
        if game_info.me.pos.y > -1800:
            return True
        return False

    ##########################

    def transition_to_turn(game_info):
        return False

    ##########################

    def transition_to_dodge(game_info):
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
    return state, state_list, persistent


##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()
    controls = CancelledFastDodge(game_info.me, Vec3(1, -1, 0)).input()

    persistent = game_info.persistent
    return controls, persistent


