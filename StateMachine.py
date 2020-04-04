class StateMachine:

    def __init__(self, name):
        self.name = name
        self.current_state = None
        self.states = None

    def add_state(self, state):
        self.current_state = state

    def update(self, game_info):
        old_state = self.current_state
        transition_state = self.current_state.transition(game_info,
                                                         self.states,
                                                         self.current_state.sub_state_machine)

        if (old_state == None) or (transition_state.name != old_state.name):
            if not transition_state.is_bottom:
                self.current_state = transition_state
                self.current_state.sub_state_machine = StateMachine("Hello") #Generate name based on level

                startup = self.current_state.startup(game_info)
                self.current_state.sub_state_machine.add_state(startup[0])
                self.current_state.sub_state_machine.states = startup[1]
            else:
                self.current_state = transition_state
                

    def get_controls(self, game_info):
        return self.current_state.get_controls(game_info, self.current_state.sub_state_machine)

    def bottom_state(self):
        if self.current_state.sub_state_machine == None:
            return self.current_state
        else:
            return self.current_state.sub_state_machine.bottom_state


class State:

    def __init__(self,
                 transition,
                 startup,
                 get_controls,
                 name,
                 is_bottom):

        self.name = name
        self.pretransition = transition
        self.prestartup = startup
        self.get_controls = get_controls
        self.sub_state_machine = None
        self.is_bottom = is_bottom


    def transition(self,
                   game_info,
                   next_states,
                   sub_state_machine):

        transition_state = self.pretransition(game_info,
                                              next_states,
                                              sub_state_machine)

        if transition_state != None:
            
            return transition_state

        elif transition_state == None:

            if self.sub_state_machine != None:
                self.sub_state_machine.update(game_info)

            return self


    def startup(self,
                game_info):


        temp_startup = self.prestartup(game_info)
        if temp_startup[0] == None:
            return self
        else:
            return temp_startup
