from rlbot.agents.base_agent import SimpleControllerState

from StateMachine import State

import Strategy.KickoffFolder.DoKickoffFolder.DiagonalRightFolder.Boost as Boost
import Strategy.KickoffFolder.DoKickoffFolder.DiagonalRightFolder.Jump as Jump
import Strategy.KickoffFolder.DoKickoffFolder.DiagonalRightFolder.FastDodge as FastDodge
import Strategy.KickoffFolder.DoKickoffFolder.DiagonalRightFolder.AerialRotation as AerialRotation
import Strategy.KickoffFolder.DoKickoffFolder.DiagonalRightFolder.Turn as Turn
import Strategy.KickoffFolder.DoKickoffFolder.DiagonalRightFolder.Dodge as Dodge

##########################################################################

BoostState = State(lambda game_info, next_states, sub_sm: Boost.transition(game_info,
                                                                           next_states,
                                                                           sub_sm),
                   lambda game_info: Boost.startup(game_info),
                   lambda game_info, sub_state_machine: Boost.get_controls(game_info, sub_state_machine),
                   "Boost",
                   True)
JumpState = State(lambda game_info, next_states, sub_sm: Jump.transition(game_info,
                                                                         next_states,
                                                                         sub_sm),
                  lambda game_info: Jump.startup(game_info),
                  lambda game_info, sub_state_machine: Jump.get_controls(game_info, sub_state_machine),
                  "Jump",
                  True)
FastDodgeState = State(lambda game_info, next_states, sub_sm: FastDodge.transition(game_info,
                                                                                   next_states,
                                                                                   sub_sm),
                       lambda game_info: FastDodge.startup(game_info),
                       lambda game_info, sub_state_machine: FastDodge.get_controls(game_info, sub_state_machine),
                       "FastDodge",
                       True)
AerialRotationState = State(lambda game_info, next_states, sub_sm: AerialRotation.transition(game_info,
                                                                                             next_states,
                                                                                             sub_sm),
                            lambda game_info: AerialRotation.startup(game_info),
                            lambda game_info, sub_state_machine: AerialRotation.get_controls(game_info, sub_state_machine),
                            "AerialRotation",
                            True)
TurnState = State(lambda game_info, next_states, sub_sm: Turn.transition(game_info,
                                                                         next_states,
                                                                         sub_sm),
                  lambda game_info: Turn.startup(game_info),
                  lambda game_info, sub_state_machine: Turn.get_controls(game_info, sub_state_machine),
                  "Turn",
                  True)
DodgeState = State(lambda game_info, next_states, sub_sm: Dodge.transition(game_info,
                                                                           next_states,
                                                                           sub_sm),
                   lambda game_info: Dodge.startup(game_info),
                   lambda game_info, sub_state_machine: Dodge.get_controls(game_info, sub_state_machine),
                   "Dodge",
                   True)

##########################################################################


def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_diagonal_left(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_diagonal_right(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_offcenter_left(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_offcenter_right(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_far_back(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    state_transitions = [transition_to_diagonal_left,
                         transition_to_diagonal_right,
                         transition_to_offcenter_left,
                         transition_to_offcenter_right,
                         transition_to_far_back]

    for i in range(len(state_transitions)):
        should_transition, persistent = state_transitions[i](game_info)
        if should_transition:
            return next_states[i], persistent

##########################################################################

def startup(game_info):

    state = BoostState
    state_list = [BoostState,
                  JumpState,
                  FastDodgeState,
                  AerialRotationState,
                  TurnState,
                  DodgeState]
    persistent = game_info.persistent
    return state, state_list, persistent


##########################################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)
