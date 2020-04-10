from math import atan2
from numpy import sign

from CowBotVector import Vec3
from GameState import Orientation
from Maneuvers import NavigateTo
from rlbot.agents.base_agent import SimpleControllerState

def transition(game_info,
               next_states,
               sub_state_machine):

        ##########################

    def transition_to_far_boost(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_far_post(game_info):

        should_transition = False
        if not game_info.teammate_far_post:
            should_transition = True
        return should_transition, game_info.persistent

    ##########################

    def transition_to_in_net(game_info):

        should_transition = False
        if (not game_info.teammate_far_post) and (not game_info.teammate_in_net):
            should_transition = True

        return should_transition, game_info.persistent

    ##########################

    def transition_to_clear(game_info):
        should_transition = False
        if sign(game_info.ball.pos.x) == sign(game_info.me.pos.x):
            should_transition = True
        return should_transition, game_info.persistent

    ##########################

    def transition_to_save(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    state_transitions = [transition_to_far_boost,
                         transition_to_far_post,
                         transition_to_in_net,
                         transition_to_clear,
                         transition_to_save]

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

    ball_angle = atan2((game_info.ball.pos - game_info.me.pos).y,
                       (game_info.ball.pos - game_info.me.pos).x)
    rot = Orientation(pyr = [game_info.me.rot.pitch, ball_angle, game_info.me.rot.roll] )
    target_state = game_info.me.copy_state(pos = Vec3(-3072*game_info.ball_x_sign,-4096,0), rot = rot)

    controls = NavigateTo(game_info.me, target_state).input()
    persistent = game_info.persistent
    return controls, persistent


