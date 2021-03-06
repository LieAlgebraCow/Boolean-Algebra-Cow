from numpy import sign

from rlbot.agents.base_agent import SimpleControllerState

from BallPrediction import ball_contact_binary_search
from CowBotVector import Vec3
from Maneuvers import GroundTurn
from StateMachine import State

import Strategy.AttackFolder.Path as Path
import Strategy.AttackFolder.Challenge as Challenge
import Strategy.AttackFolder.Aerial as Aerial

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
AerialState = State(lambda game_info, next_states, sub_sm: Aerial.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: Aerial.startup(game_info),
                      lambda game_info, sub_state_machine: Aerial.get_controls(game_info, sub_state_machine),
                      "Aerial",
                      False)

########################################################################################################
#Transition functions
########################################################################################################

def transition(game_info,
               next_states,
               sub_state_machine):

    ##########################

    def transition_to_kickoff(game_info):
        should_transition =  False
        if game_info.is_kickoff_pause:
            should_transition =  True

        return should_transition, game_info.persistent

    ##########################

    def transition_to_transition_back(game_info):

        should_transition =  False

        if game_info.number_of_team_in_front_of_ball == 3:
            #If everyone is in front of the ball, leave
            should_transition =  True
     
        elif game_info.number_of_team_in_front_of_ball == 2:
            #If two bots are in front of the ball, leave
            should_transition =  True
     
        elif game_info.number_of_team_in_front_of_ball == 1:
            if game_info.ball_behind_me: #If we are in front of the ball, leave
                should_transition =  True
            elif game_info.ball_behind_teammate_zero:
                if game_info.teammate_one_ball_side:
                    should_transition =  True
            elif game_info.ball_behind_teammate_one:
                if game_info.teammate_zero_ball_side:
                    should_transition =  True

        return should_transition, game_info.persistent

    ##########################

    def transition_to_attack(game_info):
        should_transition =  False
        return should_transition, game_info.persistent
            

    ##########################

    def transition_to_defend(game_info):
        should_transition =  False
        return should_transition, game_info.persistent

        
    ##########################

    def transition_to_transition_forward(game_info):
        should_transition = False
        return should_transition, game_info.persistent

        
    ##########################

    state_transitions = [transition_to_kickoff,
                         transition_to_attack,
                         transition_to_transition_back,
                         transition_to_defend,
                         transition_to_transition_forward]
    
    for i in range(len(state_transitions)):
        should_transition, persistent = state_transitions[i](game_info)
        if should_transition:
            return next_states[i], persistent

####################################################

def startup(game_info):

    state = PathState
    state_list = [PathState,
                  ChallengeState,
                  AerialState]
    persistent = game_info.persistent

    end_tangent = Vec3(0, 1, 0)
  
    #TODO: Dynamically update end_tangent as well
    intercept_slice, persistent.path_follower.path, persistent.path_follower.action = ball_contact_binary_search(game_info, end_tangent = end_tangent)
    #persistent.path_follower.end = intercept_slice.pos

    return state, state_list, persistent

####################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)

