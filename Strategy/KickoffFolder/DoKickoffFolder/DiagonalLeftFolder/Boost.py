from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from Maneuvers import GroundTurn

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_boost(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_jump(game_info):
        should_transition = False

        if game_info.me.pos.y > -2350:
            should_transition = True
        return should_transition, game_info.persistent

    ##########################

    def transition_to_fast_dodge(game_info):
        should_transition = False
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
            print(next_states[i].name)
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
    controls = GroundTurn(game_info.me,
                              game_info.me.copy_state(pos = Vec3(0, -900, 0))).input()
    controls.boost = 1

    persistent = game_info.persistent
    return controls, persistent

