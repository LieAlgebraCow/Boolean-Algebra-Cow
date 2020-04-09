from math import atan2
from numpy import sign

from CowBotVector import Vec3
from GameState import Orientation
from Maneuvers import NavigateTo
from StateMachine import State

import Strategy.DefendFolder.InNet as InNet
import Strategy.DefendFolder.FarPost as FarPost
import Strategy.DefendFolder.FarBoost as FarBoost
import Strategy.DefendFolder.Clear as Clear

########################################################################################################
#States for the next level down
########################################################################################################

FarBoostState = State(lambda game_info, next_states, sub_sm: FarBoost.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: FarBoost.startup(game_info),
                      lambda game_info, sub_state_machine: FarBoost.get_controls(game_info, sub_state_machine),
                      "FarBoost",
                      True)
FarPostState = State(lambda game_info, next_states, sub_sm: FarPost.transition(game_info,
                                                                               next_states,
                                                                               sub_sm),
                     lambda game_info: FarPost.startup(game_info),
                     lambda game_info, sub_state_machine: FarPost.get_controls(game_info, sub_state_machine),
                     "FarPost",
                     True)
InNetState = State(lambda game_info, next_states, sub_sm: InNet.transition(game_info,
                                                                           next_states,
                                                                           sub_sm),
                   lambda game_info: InNet.startup(game_info),
                   lambda game_info, sub_state_machine: InNet.get_controls(game_info, sub_state_machine),
                   "InNet",
                   True)
ClearState = State(lambda game_info, next_states, sub_sm: Clear.transition(game_info,
                                                                           next_states,
                                                                           sub_sm),
                   lambda game_info: Clear.startup(game_info),
                   lambda game_info, sub_state_machine: Clear.get_controls(game_info, sub_state_machine),
                   "Clear",
                   False)
SaveState = State(lambda game_info, next_states, sub_sm: Save.transition(game_info,
                                                                           next_states,
                                                                           sub_sm),
                   lambda game_info: Save.startup(game_info),
                   lambda game_info, sub_state_machine: Save.get_controls(game_info, sub_state_machine),
                   "Save",
                   False)

########################################################################################################

########################################################################################################

def transition(game_info,
               next_states,
               sub_state_machine):

    ##########################

    def transition_to_kickoff(game_info): #Could be a few of these
        if game_info.is_kickoff_pause:
            return True
        return False

    ##########################

    def transition_to_transition_forward(game_info):

        if game_info.ball.pos.y < -1152:
            return False

        if game_info.number_of_team_in_front_of_ball == 1:
            if game_info.ball_behind_teammate_zero:
                if not game_info.teammate_one_ball_side:
                    #If the teammate behind the ball is more on the ball side than we are, leave
                    return True
            elif game_info.ball_behind_teammate_one:
                if not game_info.teammate_zero_ball_side:
                    #If the teammate behind the ball is more on the ball side than we are, leave
                    return True

        elif game_info.number_of_team_in_front_of_ball == 0:
            #If we're all three behind the ball
            if not (game_info.teammate_zero_ball_side or game_info.teammate_one_ball_side):
                return True

        return False

    ##########################

    def transition_to_attack(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################

    def transition_to_transition_back(game_info): #Return True to transition, return False to skip to the next one
        if game_info.ball.pos.y > -4000:
            if game_info.ball_behind_me:
                return True
        else:
            ball_x = game_info.ball.pos.x
            me_x = game_info.ball.pos.x
            if abs(ball_x) < abs(me_x) and sign(ball_x) == sign(me_x):
                return True

        return False

    ##########################

    def transition_to_defend(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################

    state_transitions = [transition_to_kickoff,
                         transition_to_attack,
                         transition_to_transition_back,
                         transition_to_defend,
                         transition_to_transition_forward]


    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            return next_states[i]

##########################################################################

def startup(game_info):

    if (not game_info.teammate_in_net) and (not game_info.teammate_far_post):
        state = InNetState
    elif not game_info.teammate_far_post:
        state = FarPostState
    elif (not game_info.teammate_in_net) and game_info.teammate_far_post:
        state = FarBoostState
    else:
        state = InNetState

    state_list = [FarBoostState,
                  FarPostState,
                  InNetState,
                  ClearState,
                  SaveState]
    
    persistent = game_info.persistent
    return state, state_list, persistent


##########################################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)



