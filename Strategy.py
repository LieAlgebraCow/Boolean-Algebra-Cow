'''

This file is the start of Boolean Algebra Cow strategy.  It (and associated files that come up in the future), completely replaces the old 'Planning' folder from Boolean Algebra Calf.

'''

class StateMachine:


    def __init__(self, name):
        self.name = name
        self.current_state = None


    def add_state(state):
        self.current_states = state


    def update(game_info):
        self.current_state = self.current_state.transition(game_info)


    def get_controls(self):
        pass

class State:

    def __init__(self, transition, name):
        self.transition = transition
        self.name = name




##########################################################################



#For now everything is a 1v1.  I'll fix team code again in the future.
            #if self.game_info.team_mode == "1v1":
            self.plan, self.persistent = Strategy.make_plan(self.game_info,
                                                            self.plan.old_plan,
                                                            self.persistent)

            #Check if it's a kickoff.  If so, we'll run kickoff code later on.
            self.kickoff_position = update_kickoff_position(self.game_info,
                                                            self.kickoff_position)














