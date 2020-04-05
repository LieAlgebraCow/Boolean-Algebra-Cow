from rlbot.agents.base_agent import SimpleControllerState

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_do_kickoff(game_info):
        return False

    ##########################

    def transition_to_get_boost(game_info):
        return False

    ##########################

    def transition_to_cover_net(game_info):
        return False

    ##########################

    state_transitions = [transition_to_do_kickoff,
                         transition_to_get_boost,
                         transition_to_cover_net]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            return next_states[i]

##########################################################################

def startup(game_info):

    return None, None

##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()
    controls.boost = 1

    return controls

