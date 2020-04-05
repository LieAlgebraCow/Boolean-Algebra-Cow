from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from StateMachine import State
import Strategy.KickoffFolder.DoKickoff as DoKickoff
import Strategy.KickoffFolder.GetBoost as GetBoost
import Strategy.KickoffFolder.CoverNet as CoverNet


DoKickoffState = State(lambda game_info, next_states, sub_sm: DoKickoff.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: DoKickoff.startup(game_info),
                      lambda game_info, sub_state_machine: DoKickoff.get_controls(game_info, sub_state_machine),
                      "DoKickoff",
                      True)
GetBoostState = State(lambda game_info, next_states, sub_sm: GetBoost.transition(game_info,
                                                                                   next_states,
                                                                                   sub_sm),
                       lambda game_info: GetBoost.startup(game_info),
                       lambda game_info, sub_state_machine: GetBoost.get_controls(game_info, sub_state_machine),
                       "GetBoost",
                       True)
CoverNetState = State(lambda game_info, next_states, sub_sm: CoverNet.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: CoverNet.startup(game_info),
                      lambda game_info, sub_state_machine: CoverNet.get_controls(game_info, sub_state_machine),
                      "CoverNet",
                      True)


def transition(game_info,
               next_states,
               sub_state_machine):

    ball_distance = (game_info.me.pos - game_info.ball.pos).magnitude()
    closest_teammate_ball_distance = 100000
    farthest_teammate_ball_distance = 0
    for mate in game_info.teammates:
        mate_ball_distance = (mate.pos - game_info.ball.pos).magnitude()
        if mate_ball_distance < closest_teammate_ball_distance:
            closest_teammate_ball_distance = mate_ball_distance
            closest_teammate = mate
        if mate_ball_distance > farthest_teammate_ball_distance:
            farthest_teammate_ball_distance = mate_ball_distance
            farthest_teammate = mate

    def transition_to_kickoff(game_info):
        return False

    ##########################

    def transition_to_attack(game_info):

            return False

    ##########################

    def transition_to_transition_back(game_info):

        return False

    ##########################

    def transition_to_defend(game_info):

        return False

    ##########################

    def transition_to_transition_forward(game_info):
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

    pos = game_info.me.pos
    state = None

    #######################
    #Check where our bot and our teammates are on kickoff

    diagonal_left_spawn = Vec3(2048, -2560, 0)
    diagonal_right_spawn = Vec3(-2048, -2560, 0)
    offcenter_left_spawn = Vec3(256, -3840, 0)
    offcenter_right_spawn = Vec3(-256, -3840, 0)
    far_back_spawn = Vec3(0, -4608, 0)

    me_diagonal_left = False
    me_diagonal_right = False
    me_offcenter_left = False
    me_offcenter_right = False
    me_far_back = False
    
    if (pos - diagonal_left_spawn).magnitude() < 50:
        me_diagonal_left = True
    elif (pos - diagonal_right_spawn).magnitude() < 50:
        me_diagonal_right = True
    elif (pos - offcenter_left_spawn).magnitude() < 50:
        me_offcenter_left = True
    elif (pos - offcenter_right_spawn).magnitude() < 50:
        me_offcenter_right = True
    elif (pos - far_back_spawn).magnitude() < 50:
        me_far_back = True

    teammate_diagonal_left = False
    teammate_diagonal_right = False
    teammate_offcenter_left = False
    teammate_offcenter_right = False
    teammate_far_back = False
    
    for mate in game_info.teammates:
        if (mate.pos - diagonal_left_spawn).magnitude() < 50:
            teammate_diagonal_left = True
        elif (mate.pos - diagonal_right_spawn).magnitude() < 50:
            teammate_diagonal_right = True
        elif (mate.pos - offcenter_left_spawn).magnitude() < 50:
            teammate_offcenter_left = True
        elif (mate.pos - offcenter_right_spawn).magnitude() < 50:
            teammate_offcenter_right = True
        elif (mate.pos - far_back_spawn).magnitude() < 50:
            teammate_far_back = True

    ############################

    if me_diagonal_left:
        state = DoKickoffState

    elif me_diagonal_right:
        if not teammate_diagonal_left:
            state = DoKickoffState
        else:
            state = GetBoostState

    elif me_offcenter_left:
        if (not teammate_diagonal_left) and (not teammate_diagonal_right):
            state = DoKickoffState
        elif teammate_far_back:
            state = GetBoostState
        elif teammate_offcenter_right:
            state = CoverNetState

    elif me_offcenter_right:
        if teammate_diagonal_left and teammate_diagonal_right:
            state = CoverNetState
        else:
            state = GetBoostState
        
    elif me_far_back:
        state = CoverNetState
    else:
        raise ('no kickoff position chosen')

    state_list = [DoKickoffState,
                  GetBoostState,
                  CoverNetState]

    return state, state_list

##########################################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)

