from rlbot.agents.base_agent import SimpleControllerState

from Maneuvers import GroundTurn

########################################################################################################
#States for the next level down
########################################################################################################



########################################################################################################
#Transition functions
########################################################################################################

def transition(game_info,
               next_states,
               sub_state_machine):

    def transition_to_path(game_info): #Could be a few of these
        return False

    ##########################

    def transition_to_challenge(game_info): #Return True to transition, return False to skip to the next one

        ball_distance = (game_info.me.pos - game_info.ball.pos).magnitude()
        if game_info.ball.vel.magnitude() != 0 and game_info.me.vel.magnitude() != 0:        
            ball_car_dot = game_info.me.vel.normalize().dot(game_info.ball.vel.normalize())
        else:
            ball_car_dot = 0
        

        if ball_distance < 450 - 100*ball_car_dot and game_info.ball.pos.z < 250:
            return True

        return False

    ##########################

    state_transitions = [transition_to_path,
                         transition_to_challenge]

    for i in range(len(state_transitions)):
        if state_transitions[i](game_info):
            #Clear any RLU objects used
            return next_states[i]

########################################################################################################
#Startup
########################################################################################################

def startup(game_info):

    state = None
    state_list = None

    persistent = game_info.persistent
    return state, state_list, persistent

########################################################################################################
#Controls
########################################################################################################

def get_controls(game_info, sub_state_machine):

    controls = SimpleControllerState()

    persistent = game_info.persistent

    if persistent.path_follower.action != None:
        persistent.path_follower.action.step(game_info.dt)
        controls = persistent.path_follower.action.controls
    else:
        print("No path found!")
        controls = GroundTurn(game_info.me,
                              game_info.me.copy_state(pos = game_info.ball.pos)).input()

    return controls, persistent


