from Maneuvers import GroundTurn

from BallPrediction import ball_contact_binary_search
from CowBotVector import Vec3

from StateMachine import State

import Strategy.DefendFolder.SaveFolder.Path as Path
import Strategy.DefendFolder.SaveFolder.Challenge as Challenge


########################################################################################################
#States for the next level down
########################################################################################################

PathState = State(lambda game_info, next_states, sub_sm: Path.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: Path.startup(game_info),
                      lambda game_info, sub_state_machine: Path.get_controls(game_info, sub_state_machine),
                      "Path",
                      True)
ChallengeState = State(lambda game_info, next_states, sub_sm: Challenge.transition(game_info,
                                                                               next_states,
                                                                               sub_sm),
                     lambda game_info: Challenge.startup(game_info),
                     lambda game_info, sub_state_machine: Challenge.get_controls(game_info, sub_state_machine),
                     "Challenge",
                     True)

########################################################################################################
#Transition functions
########################################################################################################

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_far_boost(game_info):
        return False

    ##########################

    def transition_to_far_post(game_info):
        return False

    ##########################

    def transition_to_in_net(game_info):
        return False

    ##########################

    def transition_to_clear(game_info):
        return False

    ##########################

    def transition_to_save(game_info):
        return False
    
    ##########################

    state_transitions = [transition_to_far_boost,
                         transition_to_far_post,
                         transition_to_in_net,
                         transition_to_clear,
                         transition_to_save]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            #Clear any RLU objects used
            return next_states[i]

##########################################################################

def startup(game_info):

    state = PathState
    state_list = [PathState,
                  ChallengeState]

    persistent = game_info.persistent
    away_from_net = game_info.ball.pos - Vec3(0,-5120-80,0)
    end_tangent = 
  
    #TODO: Dynamically update end_tangent as well
    intercept_slice, persistent.path_follower.path, persistent.path_follower.action = ball_contact_binary_search(game_info, end_tangent = end_tangent)
    #persistent.path_follower.end = intercept_slice.pos

    return state, state_list, persistent

##########################################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)


