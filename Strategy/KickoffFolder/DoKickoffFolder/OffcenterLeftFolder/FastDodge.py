from rlbot.agents.base_agent import SimpleControllerState

from Mechanics import CancelledFastDodge
from StateMachine import State

########################################################################################################
#States for the next level down
########################################################################################################



########################################################################################################
#Transition functions
########################################################################################################

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_start(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_turn(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_jump(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_fast_dodge(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_land(game_info):
        should_transition = False
        if game_info.me.wheel_contact:
            should_transition = True

        return should_transition, game_info.persistent

    ##########################

    def transition_to_pre_dodge(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_dodge(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################
    
    state_transitions = [transition_to_start,
                         transition_to_turn,
                         transition_to_jump,
                         transition_to_fast_dodge,
                         transition_to_dodge,
                         transition_to_pre_dodge,
                         transition_to_final_jump,
                         transition_to_land]

    for i in range(len(state_transitions)):
        should_transition, persistent = state_transitions[i](game_info)
        if should_transition:
            return next_states[i], persistent

########################################################################################################
#Startup
########################################################################################################

def startup(game_info):

    state = None
    state_list = None

    persistent = game_info.persistent
    return state, state_list, persistent

########################################################################################################
#Controls
########################################################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()

    controller_input = CancelledFastDodge(game_info.me, 1).input()

    persistent = game_info.persistent
    return controls, persistent


