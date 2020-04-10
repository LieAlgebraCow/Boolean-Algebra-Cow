from rlbot.agents.base_agent import SimpleControllerState

from Maneuvers import GroundTurn

from StateMachine import State
import Strategy.KickoffFolder.DoKickoffFolder.OffcenterLeftFolder.Start as Start
import Strategy.KickoffFolder.DoKickoffFolder.OffcenterLeftFolder.Turn as Turn
import Strategy.KickoffFolder.DoKickoffFolder.OffcenterLeftFolder.Jump as Jump
import Strategy.KickoffFolder.DoKickoffFolder.OffcenterLeftFolder.FastDodge as FastDodge
import Strategy.KickoffFolder.DoKickoffFolder.OffcenterLeftFolder.Land as Land
import Strategy.KickoffFolder.DoKickoffFolder.OffcenterLeftFolder.PreDodge as PreDodge
import Strategy.KickoffFolder.DoKickoffFolder.OffcenterLeftFolder.Dodge as Dodge

########################################################################################################
#States for the next level down
########################################################################################################

StartState = State(lambda game_info, next_states, sub_sm: Start.transition(game_info,
                                                                                         next_states,
                                                                                         sub_sm),
                          lambda game_info: Start.startup(game_info),
                          lambda game_info, sub_state_machine: Start.get_controls(game_info, sub_state_machine),
                          "Start",
                          True)
TurnState = State(lambda game_info, next_states, sub_sm: Turn.transition(game_info,
                                                                                           next_states,
                                                                                           sub_sm),
                           lambda game_info: Turn.startup(game_info),
                           lambda game_info, sub_state_machine: Turn.get_controls(game_info, sub_state_machine),
                           "Turn",
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
LandState = State(lambda game_info, next_states, sub_sm: Land.transition(game_info,
                                                                               next_states,
                                                                               sub_sm),
                     lambda game_info: Land.startup(game_info),
                     lambda game_info, sub_state_machine: Land.get_controls(game_info, sub_state_machine),
                     "Land",
                     True)
PreDodgeState = State(lambda game_info, next_states, sub_sm: PreDodge.transition(game_info,
                                                                                             next_states,
                                                                                             sub_sm),
                            lambda game_info: PreDodge.startup(game_info),
                            lambda game_info, sub_state_machine: PreDodge.get_controls(game_info, sub_state_machine),
                            "PreDodge",
                            True)
DodgeState = State(lambda game_info, next_states, sub_sm: Dodge.transition(game_info,
                                                                               next_states,
                                                                               sub_sm),
                     lambda game_info: Dodge.startup(game_info),
                     lambda game_info, sub_state_machine: Dodge.get_controls(game_info, sub_state_machine),
                     "Dodge",
                     True)

########################################################################################################
#Transition functions
########################################################################################################

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

    state = StartState
    state_list = [StartState,
                  TurnState,
                  JumpState,
                  FastDodgeState,
                  DodgeState,
                  PreDodgeState,
                  FinalJumpState,
                  LandState]

    persistent = game_info.persistent
    return state, state_list, persistent


##########################################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)


