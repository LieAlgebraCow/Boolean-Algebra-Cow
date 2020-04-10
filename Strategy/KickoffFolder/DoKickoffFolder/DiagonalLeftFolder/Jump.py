from math import atan2

from rlbot.agents.base_agent import SimpleControllerState
from rlutilities.mechanics import AerialTurn as RLU_AerialTurn

from Conversions import rot_to_mat3
from CowBotVector import Vec3
from GameState import Orientation


def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_boost(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_jump(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_fast_dodge(game_info):
        should_transition = False

        if game_info.me.pos.z > 40:
            should_transition = True
        return should_transition, game_info.persistent

    ##########################

    def transition_to_aerial_rotation(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_turn(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_dodge(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    state_transitions = [transition_to_boost,
                         transition_to_jump,
                         transition_to_fast_dodge,
                         transition_to_aerial_rotation,
                         transition_to_turn,
                         transition_to_dodge]

    for i in range(len(state_transitions)):
        should_transition, persistent = state_transitions[i](game_info)
        if should_transition:
            return next_states[i], persistent

##########################################################################

def startup(game_info):

    state = None
    state_list = None

    target_direction = Vec3(500, 0, 0) - game_info.me.pos
    target_yaw = atan2(target_direction.x, target_direction.y)
    persistent = game_info.persistent
    #persistent.aerial_turn.action = RLU_AerialTurn(game_info.utils_game.my_car)
    target_rot = Orientation(pitch = 0,
                             yaw = target_yaw,
                             roll = 0)
    #persistent.aerial_turn.action.target = rot_to_mat3(target_rot, game_info.team_sign)

    return state, state_list, persistent

##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()

    persistent = game_info.persistent
    #persistent.aerial_turn.action.step(game_info.dt)
    #controls = persistent.aerial_turn.action.controls
    controls.boost = 1
    controls.jump = 1
    
    return controls, persistent


