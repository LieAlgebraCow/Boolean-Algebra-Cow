from rlbot.agents.base_agent import SimpleControllerState

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_kickoff(game_info): #Could be a few of these

        return True

    ##########################

    def transition_to_attack(game_info):
        
        return False


    ##########################

    def transition_to_transition_back(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################

    def transition_to_defend(game_info): #Return True to transition, return False to skip to the next one

        return False

    ##########################

    def transition_to_transition_forward(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################


    state_transitions = [transition_to_kickoff,
                         transition_to_attack,
                         transition_to_transition_back,
                         transition_to_defend,
                         transition_to_transition_forward]

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

    persistent = game_info.persistent
    return controls, persistent
