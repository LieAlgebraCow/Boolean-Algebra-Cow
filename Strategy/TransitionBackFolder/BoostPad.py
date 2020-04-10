from numpy import sign

from rlbot.agents.base_agent import SimpleControllerState

from Maneuvers import GroundTurn

def transition(game_info,
               next_states,
               sub_state_machine):

    if game_info.ball_x_sign == 1:
        boost_pad = game_info.boosts[12]
    else:
        boost_pad = game_info.boosts[14]

    def transition_to_mid_boost(game_info): #Could be a few of these
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_back_boost(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_boost_pad(game_info):
        should_transition = False

        return should_transition, game_info.persistent

    ##########################

    def transition_to_goal(game_info):
        should_transition = False
        
        if game_info.me.boost > 80:
            should_transition = True
        if game_info.me.pos.y < -1050 and game_info.me.pos.x > 0:
            should_transition = True
        if not boost_pad.is_active:
            should_transition = True

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
        boost_pad = game_info.boosts[12]
    else:
        boost_pad = game_info.boosts[14]

    controls = GroundTurn(game_info.me,
                          game_info.me.copy_state(pos = boost_pad.pos)).input()

    persistent = game_info.persistent
    return controls, persistent

