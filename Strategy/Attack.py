from numpy import sign

from rlbot.agents.base_agent import SimpleControllerState


from CowBotVector import Vec3
from Maneuvers import GroundTurn


def transition(game_info,
               next_states,
               sub_state_machine):

    number_of_team_in_front_of_ball = 0
    ball_behind_me = False
    ball_behind_teammate_zero = False
    ball_behind_teammate_one = False
    if game_info.ball.pos.y < game_info.me.pos.y:
        ball_behind_me = True
        number_of_team_in_front_of_ball += 1
    if game_info.ball.pos.y < game_info.teammates[0].pos.y:
        ball_behind_teammate_zero = True
        number_of_team_in_front_of_ball += 1
    if game_info.ball.pos.y < game_info.teammates[1].pos.y:
        ball_behind_teammate_one = True
        number_of_team_in_front_of_ball += 1
        

    ball_x_sign = sign(game_info.ball.pos.x)


    ##########################

    def transition_to_transition_back(game_info):
     
        if number_of_team_in_front_of_ball == 3:
            return True
     
        elif number_of_team_in_front_of_ball == 2:
            return True
     
        elif number_of_team_in_front_of_ball == 1:
            if ball_behind_me:
                return True
            elif ball_behind_teammate_zero:
                if game_info.me.pos.x * ball_x_sign < game_info.teammates[1].pos.x * ball_x_sign:
                    return True
            elif ball_behind_teammate_one:
                if game_info.me.pos.x * ball_x_sign < game_info.teammates[0].pos.x * ball_x_sign:
                    return True

    ##########################

    def transition_to_kickoff(game_info): #Could be a few of these
        if game_info.is_kickoff_pause:
            return True
        return False

    ##########################

    def transition_to_attack(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################

    def transition_to_defend(game_info): #Return True to transition, return False to skip to the next one
        return False

    ##########################

    def transition_to_transition_forward(game_info): #Return True to transition, return False to skip to the next one
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

####################################################

def startup(game_info):

    return None, None


####################################################

def get_controls(game_info, sub_state_machine):
    controls = SimpleControllerState()

    controls = GroundTurn(game_info.me,
                          game_info.me.copy_state(pos = game_info.ball.pos)).input()


    return controls
