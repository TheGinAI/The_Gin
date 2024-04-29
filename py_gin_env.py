from tf_agents.environments.py_environment import PyEnvironment
from tf_agents.specs import BoundedArraySpec
import numpy as np
from tf_agents.trajectories import time_step as ts
from tf_agents.environments import utils

from gin_env import Deck, Card


# TensorFlow Environment wrapper around the Gin model
class PyGinEnv(PyEnvironment):
    def __init__(self, player_count):
        self._action_spec = BoundedArraySpec(shape=(9,), dtype=np.float32, minimum=0, maximum=1, name='action')
        self._observation_spec = BoundedArraySpec(shape=(10,), dtype=np.int32, minimum=-1, maximum=51, name='observation')
        self._episode_ended = False

        self._move_num = 0
        self._player_count = player_count
        self._current_player = 0
        self._draw_or_discard = 0
        self._deck = Deck()
        self._hands = self._deck.deal(player_count)
        self._discarded = None

    def deck(self):
        return self._deck

    # Action is a list like [draw_from_discard_or_draw_pile_or_retrieve_hand, 8x_probability_of_discarding_card_index]
    def action_spec(self):
        return self._action_spec

    # Observation is a list like [draw_or_discard_action_input_next, discard_pile_top, 7x_cards_on_hand_and_1x_undefined_or_8x_cards_on_hand]
    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._episode_ended = False

        self._move_num = 0
        self._current_player = 0
        self._draw_or_discard = 0
        self._deck = Deck()
        self._hands = self._deck.deal(self._player_count)

        return ts.restart(np.array([self._draw_or_discard, self._deck.discard_pile_top.card_id] + [x.card_id for x in self._hands[self._current_player]] + [-1], dtype=np.int32))


    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        # Special action to return the player indicated by action[1] hand for display
        if action[0] == -1:
            return ts.transition(np.array([len(self._deck.draw_pile)] + [self._deck.discard_pile_top.card_id] + [x.card_id for x in self._hands[action[1]]]), 0)

        elif self._draw_or_discard == 0:
            draw_action = int(round(action[0]))

            if draw_action < 0.5:
                # Draw from draw pile
                self._discarded = Card(-1)
                self._hands[self._current_player].draw_from_draw_pile()
            elif draw_action >= 0.5:
                # Draw from discard pile
                self._discarded = self._deck.discard_pile_top
                self._hands[self._current_player].draw_from_discard_pile()

            if self._hands[self._current_player].check():
                self._episode_ended = True
                return ts.termination(np.array([self._draw_or_discard, self._deck.discard_pile_top.card_id] + [x.card_id for x in self._hands[self._current_player]], dtype=np.int32), 100.0)
            else:
                self._draw_or_discard = 1
                return ts.transition(np.array([self._draw_or_discard, self._deck.discard_pile_top.card_id] + [x.card_id for x in self._hands[self._current_player]], dtype=np.int32), 0.0, 1.0)
        elif self._draw_or_discard == 1:
            # Select card index to discard with highest probability
            discard_action = action[1:]
            id_primary = np.argmax(discard_action)

            # Discarding card that was just drawn from the discard pile is not allowed, select discard action with second highest probability
            if self._discarded == self._hands[self._current_player][id_primary]:
                discard_action = np.delete(discard_action, id_primary)
                id_secondary = np.argmax(discard_action)
                self._hands[self._current_player].discard(id_secondary)
            else:
                self._hands[self._current_player].discard(id_primary)

            self._move_num += 1
            self._current_player = (self._current_player + 1) % self._player_count
            self._draw_or_discard = 0

            # End the game in a draw after each player has made 100 turns
            if self._move_num >= 100 * self._player_count:
                return ts.termination(np.array([self._draw_or_discard, self._deck.discard_pile_top.card_id] + [x.card_id for x in self._hands[self._current_player]] + [-1], dtype=np.int32), -1.0)
            else:
                return ts.transition(np.array([self._draw_or_discard, self._deck.discard_pile_top.card_id] + [x.card_id for x in self._hands[self._current_player]] + [-1], dtype=np.int32), -1.0, 1.0)


if __name__ == "__main__":
    environment = PyGinEnv(2)
    utils.validate_py_environment(environment, episodes=5)
