from numpy import sign

from rlbot.agents.base_agent import SimpleControllerState

from Maneuvers import GroundTurn

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_mid_boost(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_back_boost(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_boost_pad(game_info):
        should_transition = False

        if game_info.ball_x_sign == 1:
            far_back_boost = game_info.boosts[3]
        else:
            far_back_boost = game_info.boosts[4]

        if game_info.me.boost > 60:
            should_transition = True

        if not far_back_boost.is_active:
            should_transition = True
        return should_transition, game_info.persistent


    ##########################

    def transition_to_goal(game_info):
        should_transition = False

        return should_transition, game_info.persistent


    ##########################

    state_transitions = [transition_to_mid_boost,
                         transition_to_back_boost,
                         transition_to_boost_pad,
                         transition_to_goal]

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

    if game_info.ball_x_sign == 1:
        far_back_boost = game_info.boosts[3]
    else:
        far_back_boost = game_info.boosts[4]

    controls = GroundTurn(game_info.me,
                          game_info.me.copy_state(pos = far_back_boost.pos)).input()

    persistent = game_info.persistent
    return controls, persistent


