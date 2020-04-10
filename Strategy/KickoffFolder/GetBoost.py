from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from StateMachine import State
import Strategy.KickoffFolder.GetBoostFolder.LeftBoost as LeftBoost
import Strategy.KickoffFolder.GetBoostFolder.RightBoost as RightBoost



##########################################################################

LeftBoostState = State(lambda game_info, next_states, sub_sm: LeftBoost.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: LeftBoost.startup(game_info),
                      lambda game_info, sub_state_machine: LeftBoost.get_controls(game_info, sub_state_machine),
                      "LeftBoost",
                      True)
RightBoostState = State(lambda game_info, next_states, sub_sm: RightBoost.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: RightBoost.startup(game_info),
                      lambda game_info, sub_state_machine: RightBoost.get_controls(game_info, sub_state_machine),
                      "RightBoost",
                      True)

##########################################################################

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
    if game_info.me.pos.x > 0:
        state = LeftBoostState
    else:
        state = RightBoostState
        
    state_list = [LeftBoostState,
                  RightBoostState]
    persistent = game_info.persistent
    return state, state_list, persistent


##########################################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)


