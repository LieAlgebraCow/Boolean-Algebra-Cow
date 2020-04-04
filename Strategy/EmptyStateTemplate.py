from rlbot.agents.base_agent import SimpleControllerState

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_state_1(game_info): #Could be a few of these
        return False

    ##########################

    def transition_to_state_2(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################

    state_transitions = [transition_to_state_1, transition_to_state_2]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            return next_states[i]

##########################################################################

def startup(game_info):

    return None, None

##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()

    return controls
