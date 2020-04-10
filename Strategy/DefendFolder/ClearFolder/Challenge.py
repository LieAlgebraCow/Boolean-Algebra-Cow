from rlbot.agents.base_agent import SimpleControllerState

from Mechanics import AirDodge
from Miscellaneous import car_coordinates_2d


########################################################################################################
#States for the next level down
########################################################################################################



########################################################################################################
#Transition functions
########################################################################################################

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_path(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_challenge(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    state_transitions = [transition_to_path,
                         transition_to_challenge]

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

    if game_info.me.wheel_contact:
        #If still on ground, jump
        controls.jump = 1
    else:
        #Once we've jumped, dodge towards the ball
        controls = AirDodge(car_coordinates_2d(game_info.me,
                                                       game_info.ball.pos - game_info.me.pos),
                                    game_info.me.jumped_last_frame).input()

    return controls, persistent


