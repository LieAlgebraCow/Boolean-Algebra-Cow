from numpy import sign

from rlbot.agents.base_agent import SimpleControllerState

from Maneuvers import GroundTurn

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_mid_boost(game_info): #Could be a few of these

        return False

    ##########################

    def transition_to_back_boost(game_info):

        return False

    ##########################

    def transition_to_boost_pad(game_info):

        ball_x_sign = sign(game_info.ball.pos.x)

        if ball_x_sign == 1:
            far_mid_boost = game_info.boosts[15]
        else:
            far_mid_boost = game_info.boosts[18]

        if game_info.me.boost > 60:
            return True
        return False


    ##########################

    def transition_to_goal(game_info):
        
        return False

    ##########################

    state_transitions = [transition_to_mid_boost,
                         transition_to_back_boost,
                         transition_to_boost_pad,
                         transition_to_goal]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            return next_states[i]

##########################################################################

def startup(game_info):

    return None, None

##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()

    ball_x_sign = sign(game_info.ball.pos.x)

    if ball_x_sign == 1:
        far_back_boost = game_info.boosts[3]
    else:
        far_back_boost = game_info.boosts[4]

    controls = GroundTurn(game_info.me,
                          game_info.me.copy_state(pos = far_back_boost.pos)).input()

    return controls

