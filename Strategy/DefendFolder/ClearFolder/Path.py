from rlbot.agents.base_agent import SimpleControllerState

from BallPrediction import ball_contact_binary_search
from CowBotVector import Vec3
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

    def transition_to_path(game_info):
        should_transition = False
        return should_transition, game_info.persistent

    ##########################

    def transition_to_challenge(game_info):
        should_transition = False 

        ball_distance = (game_info.me.pos - game_info.ball.pos).magnitude()
        if game_info.ball.vel.magnitude() != 0 and game_info.me.vel.magnitude() != 0:        
            ball_car_dot = game_info.me.vel.normalize().dot(game_info.ball.vel.normalize())
        else:
            ball_car_dot = 0    

        if ball_distance < 450 - 100*ball_car_dot and game_info.ball.pos.z < 250:
            should_transition = True
    
        return should_transition, game_info.persistent

    ##########################

    state_transitions = [transition_to_path,
                         transition_to_challenge]

    for i in range(len(state_transitions)):
        should_transition, persistent = state_transitions[i](game_info)
        if should_transition:
            return next_states[i], persistent

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
        end_tangent = Vec3(0, 1, 0)
  
        #If we didn't have a path already, try to find one. Just ground turn for now, but
        #when we find one we'll follow it starting next tick.
        intercept_slice, persistent.path_follower.path, persistent.path_follower.action = ball_contact_binary_search(game_info, end_tangent = end_tangent)
        #persistent.path_follower.end = intercept_slice.pos
        
        controls = GroundTurn(game_info.me,
                              game_info.me.copy_state(pos = game_info.ball.pos)).input()


    return controls, persistent




