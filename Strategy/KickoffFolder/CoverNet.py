from math import atan2

from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from GameState import Orientation
from Maneuvers import NavigateTo

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_do_kickoff(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_get_boost(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_cover_net(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    state_transitions = [transition_to_do_kickoff,
                         transition_to_get_boost,
                         transition_to_cover_net]

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

    ball_angle = atan2((game_info.ball.pos - game_info.me.pos).y,
                       (game_info.ball.pos - game_info.me.pos).x)
    rot = Orientation(pyr = [game_info.me.rot.pitch, ball_angle, game_info.me.rot.roll] )
    target_state = game_info.me.copy_state(pos = Vec3(0,-5120-80,0), rot = rot)
    controls = NavigateTo(game_info.me, target_state).input()

    persistent = game_info.persistent
    return controls, persistent


