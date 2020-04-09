from rlbot.agents.base_agent import SimpleControllerState

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
        return False

    ##########################

    def transition_to_dodge(game_info): #Could be a few of these
        if game_info.me.pos.y > -240:
           return True
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
    controls.throttle = 1
    controls.boost = 1
    controls.steer = -1

    persistent = game_info.persistent
    return controls, persistent

