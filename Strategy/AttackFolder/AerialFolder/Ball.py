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

    def transition_to_ball(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_recover(game_info):
        should_transition = False
        if game_info.game_time > game_info.persistent.aerial.action.arrival_time + 0.1:
            should_transition = True

        return should_transition, game_info.persistent

    ##########################

    state_transitions = [transition_to_ball,
                         transition_to_recover]

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

    persistent = game_info.persistent

    persistent.aerial.action.step(game_info.dt)
    controls = persistent.aerial.action.controls

    return controls, persistent


