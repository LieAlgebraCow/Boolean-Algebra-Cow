from rlbot.agents.base_agent import SimpleControllerState

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_diagonal_left(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_diagonal_right(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_offcenter_left(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_offcenter_right(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_far_back(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    state_transitions = [transition_to_diagonal_left,
                         transition_to_diagonal_right,
                         transition_to_offcenter_left,
                         transition_to_offcenter_right,
                         transition_to_far_back]

    for i in range(len(state_transitions)):
        should_transition, persistent = state_transitions[i](game_info)
        if should_transition:
            return next_states[i], persistent

##########################################################################

def startup(game_info):

    state = None
    state_list = None
    persistent = game_info.persistent
    return state, state_list, persistent


##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()

    persistent = game_info.persistent
    return controls, persistent


