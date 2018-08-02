import copy
import numpy as np
import os
import pygame
from abstract import abstract_state
from solitaire_code import solitaire
import pdb


class SolitaireState(abstract_state.AbstractState):
    env_name = "solitaire"
    num_players = 1

    def __init__(self):
        self.current_state = solitaire.game()
        self.current_state.shuffle()
        self.game_outcome = None  # 0 - player 1 won, 'draw' - draw, 1 - player 2 won, None - game not over

        self.resources = {}  # sprites for pygame

    def reinitialize(self):
        self.current_state = solitaire.game()
        self.current_state.shuffle()  # set up initial piece configuration
        self.current_player = 0
        self.game_outcome = None

    def clone(self):            # Internal Python3.6 function
        new_state = copy.copy(self)
        new_state.current_state = copy.copy(self.current_state)
        return new_state

    def set(self, state):
        self.current_state = state.current_state        # ADD
        # self.current_player = state.current_player
        self.game_outcome = state.game_outcome

    def take_action(self, action):         # What is action    ERROR
        reward = self.current_state.move_piece()
        pdb.set_trace()
        self.current_state.last_action, previous_player = action, self.current_player   # Setup functions for last_action  ERROR  // Global CHANGE of previous_player to previous_action
        self.b_player()                # Can be found in abstract_state.py

        self.current_state.cached_actions = []
        self.get_actions()  # Line 53
        if len(self.current_state.cached_actions) == 0:
            self.game_outcome = previous_player if self.current_state.is_checked(self.get_current_color()) else 'draw'
            if self.game_outcome != 'draw':
                reward = self.current_state.piece_values['k']

        # The current player gets the opposite of the reward (e.g. losing a piece)
        return np.array([-1 * reward if player_idx == self.current_player else reward
                         for player_idx in range(self.num_players)])

    def get_actions(self):
        if len(self.current_state.cached_actions) == 0:
            self.current_state.cached_actions = self.current_state.get_actions()
        return self.current_state.cached_actions

    # def get_current_color(self):
        # return 'white' if self.current_player == 0 else 'black'

    def get_value_bounds(self):
        pdb.set_trace()
        king_value = self.current_state.piece_values['k']  # defeat / victory
        queen_value = self.current_state.piece_values['q']
        return {'defeat': -1 * king_value, 'victory': king_value,
                'min non-terminal': -1 * queen_value, 'max non-terminal': queen_value,
                'pre-computed min': None, 'pre-computed max': None,
                'evaluation function': None}

    def is_terminal(self):
        return self.game_outcome is not None


    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return self.current_state.__str__()  # print board
    