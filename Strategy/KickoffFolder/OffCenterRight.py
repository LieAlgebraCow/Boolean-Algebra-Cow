from rlbot.agents.base_agent import SimpleControllerState

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_diagonal_left(game_info):
        return False

    ##########################

    def transition_to_diagonal_right(game_info):
        return False

    ##########################

    def transition_to_offcenter_left(game_info):
        return False

    ##########################
    def transition_to_offcenter_right(game_info):
        return False

    ##########################

    def transition_to_far_back(game_info):
        return False

    ##########################

    state_transitions = [transition_to_diagonal_left,
                         transition_to_diagonal_right,
                         transition_to_offcenter_left,
                         transition_to_offcenter_right,
                         transition_to_far_back]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            return next_states[i]

##########################################################################

def startup(game_info):

    return None, None

##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()
    controls.throttle = 1
    controls.steer = 1

    return controls

