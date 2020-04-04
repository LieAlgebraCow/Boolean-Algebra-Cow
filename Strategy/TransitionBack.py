from math import atan2
from numpy import sign

from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from GameState import Orientation
from Maneuvers import GroundTurn, NavigateTo
from StateMachine import State
import Strategy.TransitionBackFolder.MidBoost as MidBoost
import Strategy.TransitionBackFolder.BackBoost as BackBoost
import Strategy.TransitionBackFolder.BoostPad as BoostPad
import Strategy.TransitionBackFolder.Goal as Goal


MidBoostState = State(lambda game_info, next_states, sub_sm: MidBoost.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: MidBoost.startup(game_info),
                      lambda game_info, sub_state_machine: MidBoost.get_controls(game_info, sub_state_machine),
                      "MidBoost",
                      True)
BackBoostState = State(lambda game_info, next_states, sub_sm: BackBoost.transition(game_info,
                                                                                   next_states,
                                                                                   sub_sm),
                       lambda game_info: BackBoost.startup(game_info),
                       lambda game_info, sub_state_machine: BackBoost.get_controls(game_info, sub_state_machine),
                       "BackBoost",
                       True)
BoostPadState = State(lambda game_info, next_states, sub_sm: BoostPad.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: BoostPad.startup(game_info),
                      lambda game_info, sub_state_machine: BoostPad.get_controls(game_info, sub_state_machine),
                      "BoostPad",
                      True)
GoalState = State(lambda game_info, next_states, sub_sm: Goal.transition(game_info,
                                                                         next_states,
                                                                         sub_sm),
                  lambda game_info: Goal.startup(game_info),
                  lambda game_info, sub_state_machine: Goal.get_controls(game_info, sub_state_machine),
                  "Goal",
                  True)

########################################################################################################

########################################################################################################

def transition(game_info,
               next_states,
               sub_state_machine):

    ball_x_sign = sign(game_info.ball.pos.x)
    far_post_distance = (game_info.me.pos - Vec3(-893*ball_x_sign,-5120,0)).magnitude()

    ##########################

    def transition_to_defend(game_info):
     
        if far_post_distance < 500:
            return True
        return False

    ##########################

    def transition_to_transition_forward(game_info):
        return False

    ##########################

    def transition_to_attack(game_info):
        return False

    ##########################

    def transition_to_transition_back(game_info):
        return False

    ##########################

    def transition_to_kickoff(game_info):
        if game_info.is_kickoff_pause:
            return True
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

    state = MidBoostState
    state_list = [MidBoostState,
                  BackBoostState,
                  BoostPadState,
                  GoalState]


    return state, state_list

##########################################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)
