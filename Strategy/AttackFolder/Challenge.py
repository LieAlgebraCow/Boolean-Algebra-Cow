from rlbot.agents.base_agent import SimpleControllerState

from Mechanics import AirDodge

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

        if game_info.ball.pos.y - game_info.me.pos.y > 600:
            should_transition = True

        return should_transition, game_info.persistent

    ##########################

    def transition_to_challenge(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_aerial(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    state_transitions = [transition_to_path,
                         transition_to_challenge,
                         transition_to_aerial]


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

    ball_direction = game_info.ball.pos - game_info.me.pos

    controls = AirDodge(ball_direction,
                        game_info.me.jumped_last_frame).input()

    persistent = game_info.persistent
    return controls, persistent


