from rlbot.agents.base_agent import SimpleControllerState

from CowBotVector import Vec3
from StateMachine import State
import Strategy.KickoffFolder.DoKickoff as DoKickoff
import Strategy.KickoffFolder.GetBoost as GetBoost
import Strategy.KickoffFolder.CoverNet as CoverNet

########################################################################################################
#States for the next level down
########################################################################################################


DoKickoffState = State(lambda game_info, next_states, sub_sm: DoKickoff.transition(game_info,
                                                                                   next_states,
                                                                                   sub_sm),
                       lambda game_info: DoKickoff.startup(game_info),
                       lambda game_info, sub_state_machine: DoKickoff.get_controls(game_info, sub_state_machine),
                       "DoKickoff",
                       False)
GetBoostState = State(lambda game_info, next_states, sub_sm: GetBoost.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: GetBoost.startup(game_info),
                      lambda game_info, sub_state_machine: GetBoost.get_controls(game_info, sub_state_machine),
                      "GetBoost",
                      False)
CoverNetState = State(lambda game_info, next_states, sub_sm: CoverNet.transition(game_info,
                                                                                 next_states,
                                                                                 sub_sm),
                      lambda game_info: CoverNet.startup(game_info),
                      lambda game_info, sub_state_machine: CoverNet.get_controls(game_info, sub_state_machine),
                      "CoverNet",
                      True)

########################################################################################################
#Transition functions
########################################################################################################

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
        #If we can get the next touch, and a teammate doesn't have a better one

        return False

    ##########################

    def transition_to_transition_back(game_info):
        #Pretty much always go get boost
        if sub_state_machine.current_state == DoKickoffState and not game_info.is_kickoff_pause:
            #If we just took the kickoff and hit the ball, go get boost
            return True

        if sub_state_machine.current_state == GetBoostState and game_info.me.boost > 90:
            #If we're going for boost, make sure we get it
            return True

        return False

    ##########################

    def transition_to_defend(game_info):
        if sub_state_machine.current_state == CoverNetState and not game_info.is_kickoff_pause:
            #If we were waiting in net for the kickoff, go to DefendState after the ball is hit
            return True

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


########################################################################################################
#Startup
########################################################################################################

def startup(game_info):

    state = None

    ############################

    print("Diagonal Left" , game_info.me_diagonal_left, game_info.me.pos)
    print(game_info.me_diagonal_right)
    print(game_info.me_offcenter_left)
    print(game_info.me_offcenter_right)
    print(game_info.me_far_back)



    if game_info.me_diagonal_left:
        state = DoKickoffState

    elif game_info.me_diagonal_right:
        if not game_info.teammate_diagonal_left:
            state = DoKickoffState
        else:
            state = GetBoostState

    elif game_info.me_offcenter_left:
        if (not game_info.teammate_diagonal_left) and (not game_info.teammate_diagonal_right):
            state = DoKickoffState
        elif game_info.teammate_far_back:
            state = GetBoostState
        else:
            state = CoverNetState

    elif game_info.me_offcenter_right:
        if game_info.teammate_diagonal_left and game_info.teammate_diagonal_right:
            state = CoverNetState
        else:
            state = GetBoostState
        
    elif game_info.me_far_back:
        state = CoverNetState

    else:
        raise Exception('no kickoff position chosen')

    state_list = [DoKickoffState,
                  GetBoostState,
                  CoverNetState]

    persistent = game_info.persistent
    return state, state_list, persistent

########################################################################################################
#Controls
########################################################################################################

def get_controls(game_info, sub_state_machine):

    return sub_state_machine.get_controls(game_info)

