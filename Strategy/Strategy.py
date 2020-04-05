from StateMachine import State
import Strategy.Kickoff as Kickoff
import Strategy.Attack as Attack
import Strategy.TransitionBack as TransitionBack
import Strategy.Defend as Defend
import Strategy.TransitionForward as TransitionForward


KickoffState = State(lambda game_info, next_states, sub_sm: Kickoff.transition(game_info,
                                                                               next_states,
                                                                               sub_sm),
                    lambda game_info: Kickoff.startup(game_info),
                    lambda game_info, sub_state_machine: Kickoff.get_controls(game_info,
                                                                              sub_state_machine),
                     "Kickoff",
                     False)
AttackState = State(lambda game_info, next_states, sub_sm: Attack.transition(game_info,
                                                                             next_states,
                                                                             sub_sm),
                    lambda game_info: Attack.startup(game_info),
                    lambda game_info, sub_state_machine: Attack.get_controls(game_info,
                                                                             sub_state_machine),
                    "Attack",
                    True)
TransitionBackState = State(lambda game_info, next_states, sub_sm: TransitionBack.transition(game_info,
                                                                                             next_states,
                                                                                             sub_sm),
                            lambda game_info: TransitionBack.startup(game_info),
                            lambda game_info, sub_state_machine: TransitionBack.get_controls(game_info,
                                                                                             sub_state_machine),
                            "Transition Back",
                            False)
DefendState = State(lambda game_info, next_states, sub_sm: Defend.transition(game_info,
                                                                             next_states,
                                                                             sub_sm),
                    lambda game_info: Defend.startup(game_info),
                    lambda game_info, sub_state_machine: Defend.get_controls(game_info,
                                                                             sub_state_machine),
                    "Defend",
                    True)
TransitionForwardState = State(lambda game_info, next_states, sub_sm: TransitionForward.transition(game_info,
                                                                                           next_states,
                                                                                           sub_sm),
                               lambda game_info: TransitionForward.startup(game_info),
                               lambda game_info, sub_state_machine: TransitionForward.get_controls(game_info, sub_state_machine),
                               "Transition Forward",
                               True)


