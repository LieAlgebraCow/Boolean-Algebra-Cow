from rlbot.agents.base_agent import SimpleControllerState

def transition(game_info,
               next_states,
               sub_state_machine):

    ball_distance = (game_info.me.pos - game_info.ball.pos).magnitude()
    closest_teammate_ball_distance = 100000
    for mate in game_info.teammates:
        mate_ball_distance = (mate.pos - game_info.ball.pos).magnitude()
        if mate_ball_distance < closest_teammate_ball_distance:
            closest_teammate_ball_distance = mate_ball_distance
            closest_teammate = mate
    
    
    def transition_to_kickoff(game_info):
        return False

    ##########################

    def transition_to_attack(game_info):
        
        if ball_distance < closest_teammate_ball_distance - 5:
            return True
        elif (abs(ball_distance - closest_teammate_ball_distance) < 5) and game_info.me.pos.x > 0:
            return True
        return False

    ##########################

    def transition_to_transition_back(game_info):

        if (abs(ball_distance - closest_teammate_ball_distance) < 5) and game_info.me.pos.x < 0:
            return True

        return True

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

        return None, None


##########################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()

    return controls

