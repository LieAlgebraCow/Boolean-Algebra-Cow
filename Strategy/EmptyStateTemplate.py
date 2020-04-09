from rlbot.agents.base_agent import SimpleControllerState

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

    def transition_to_path(game_info): #Could be a few of these
        return False

    ##########################

    def transition_to_challenge(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################

    state_transitions = [transition_to_path,
                         transition_to_challenge]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            #Clear any RLU objects used
            return next_states[i]

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

    persistent = game_info.persistent
    return controls, persistent


