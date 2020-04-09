from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from StateMachine import State
import Strategy.KickoffFolder.DoKickoffFolder.DiagonalLeft  as DiagonalLeft
import Strategy.KickoffFolder.DoKickoffFolder.DiagonalRight as DiagonalRight
import Strategy.KickoffFolder.DoKickoffFolder.OffcenterLeft as OffcenterLeft
import Strategy.KickoffFolder.DoKickoffFolder.OffcenterRight as OffcenterRight
import Strategy.KickoffFolder.DoKickoffFolder.FarBack as FarBack

DiagonalLeftState = State(lambda game_info, next_states, sub_sm: DiagonalLeft.transition(game_info,
                                                                                         next_states,
                                                                                         sub_sm),
                          lambda game_info: DiagonalLeft.startup(game_info),
                          lambda game_info, sub_state_machine: DiagonalLeft.get_controls(game_info, sub_state_machine),
                          "DiagonalLeft",
                          False)
DiagonalRightState = State(lambda game_info, next_states, sub_sm: DiagonalRight.transition(game_info,
                                                                                           next_states,
                                                                                           sub_sm),
                           lambda game_info: DiagonalRight.startup(game_info),
                           lambda game_info, sub_state_machine: DiagonalRight.get_controls(game_info, sub_state_machine),
                           "DiagonalRight",
                           False)
OffcenterLeftState = State(lambda game_info, next_states, sub_sm: OffcenterLeft.transition(game_info,
                                                                                           next_states,
                                                                                           sub_sm),
                           lambda game_info: OffcenterLeft.startup(game_info),
                           lambda game_info, sub_state_machine: OffcenterLeft.get_controls(game_info, sub_state_machine),
                           "OffcenterLeft",
                           True)
OffcenterRightState = State(lambda game_info, next_states, sub_sm: OffcenterRight.transition(game_info,
                                                                                             next_states,
                                                                                             sub_sm),
                            lambda game_info: OffcenterRight.startup(game_info),
                            lambda game_info, sub_state_machine: OffcenterRight.get_controls(game_info, sub_state_machine),
                            "OffcenterRight",
                            True)
FarBackState = State(lambda game_info, next_states, sub_sm: FarBack.transition(game_info,
                                                                               next_states,
                                                                               sub_sm),
                     lambda game_info: FarBack.startup(game_info),
                     lambda game_info, sub_state_machine: FarBack.get_controls(game_info, sub_state_machine),
                     "FarBack",
                     True)

##########################################################################

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_do_kickoff(game_info):
        return False

    ##########################

    def transition_to_get_boost(game_info):
        return False

    ##########################

    def transition_to_cover_net(game_info):
        return False

    ##########################

    state_transitions = [transition_to_do_kickoff,
                         transition_to_get_boost,
                         transition_to_cover_net]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            return next_states[i]

##########################################################################

def startup(game_info):

    if game_info.me_diagonal_left:
        state = DiagonalLeftState
    elif game_info.me_diagonal_right:
        state = DiagonalRightState
    elif game_info.me_offcenter_left:
        state = OffcenterLeftState
    elif game_info.me_offcenter_right:
        state = OffcenterRightState
    elif game_info.me_far_back:
        state = FarBackState
    else:
        raise Exception("kickoff position not recognized")

    state_list = [DiagonalLeftState,
                  DiagonalRightState,
                  OffcenterLeftState,
                  OffcenterRightState,
                  FarBackState]

    persistent = game_info.persistent
    return state, state_list, persistent


##########################################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)

