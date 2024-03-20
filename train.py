import time
import os
from typing import List

from gin_env import Deck
from marl.maddpg import Agent as MADDPGAgent, list_softmax

import numpy as np
import tensorflow as tf

if tf.config.experimental.list_physical_devices('GPU'):
    tf.config.experimental.set_memory_growth(tf.config.experimental.list_physical_devices('GPU')[0],
                                             True)

def train():
    """
    This is the main training function, which includes the setup and training loop.
    It is meant to be called automatically by sacred, but can be used without it as well.

    :param _run:            Sacred _run object for legging
    :param exp_name:        (str) Name of the experiment
    :param save_rate:       (int) Frequency to save networks at
    :param display:         (bool) Render the environment
    :param restore_fp:      (str)  File-Patch to policy to restore_fp or None if not wanted.
    :param hard_max:        (bool) Only output one action
    :param max_episode_len: (int) number of transitions per episode
    :param num_episodes:    (int) number of episodes
    :param batch_size:      (int) batch size for updates
    :param update_rate:     (int) perform critic update every n environment steps
    :param use_target_action:   (bool) use action from target network
    :return:    List of episodic rewards
    """
    # Create environment
    print(_run.config)
    env = make_env()

    # Create agents
    agents = get_agents(_run, env, env.n_adversaries)

    logger = RLLogger(exp_name, _run, len(agents), env.n_adversaries, save_rate)

    # Load previous results, if necessary
    if restore_fp is not None:
        print('Loading previous state...')
        for ag_idx, agent in enumerate(agents):
            fp = os.path.join(restore_fp, 'agent_{}'.format(ag_idx))
            agent.load(fp)

    obs_n = env.reset()

    print('Starting iterations...')
    while True:
        # get action
        if use_target_action:
            action_n = [agent.target_action(obs.astype(np.float32)[None])[0] for agent, obs in
                        zip(agents, obs_n)]
        else:
            action_n = [agent.action(obs.astype(np.float32)) for agent, obs in zip(agents, obs_n)]
        # environment step
        if hard_max:
            hard_action_n = softmax_to_argmax(action_n, agents)
            new_obs_n, rew_n, done_n, info_n = env.step(hard_action_n)
        else:
            action_n = [action.numpy() for action in action_n]
            new_obs_n, rew_n, done_n, info_n = env.step(action_n)

        logger.episode_step += 1

        done = all(done_n)
        terminal = (logger.episode_step >= max_episode_len)
        done = done or terminal

        # collect experience
        for i, agent in enumerate(agents):
            agent.add_transition(obs_n, action_n, rew_n[i], new_obs_n, done) #########
        obs_n = new_obs_n

        for ag_idx, rew in enumerate(rew_n):
            logger.cur_episode_reward += rew #########
            logger.agent_rewards[ag_idx][-1] += rew

        if done:
            obs_n = env.reset()
            episode_step = 0
            logger.record_episode_end(agents)

        logger.train_step += 1

        # policy updates
        train_cond = not display
        for agent in agents:
            if train_cond and len(agent.replay_buffer) > batch_size * max_episode_len:
                if logger.train_step % update_rate == 0:  # only update every 100 steps
                    q_loss, pol_loss = agent.update(agents, logger.train_step) #########

        # for displaying learned policies
        if display:
            time.sleep(0.1)
            env.render()

        # saves logger outputs to a file similar to the way in the original MADDPG implementation
        if len(logger.episode_rewards) > num_episodes:
            logger.experiment_end()
            return logger.get_sacred_results()


if __name__ == '__main__':
    # Create environment
    deck = Deck()
    hands = deck.deal(2)
    agents = [MADDPGAgent(), MADDPGAgent()]

    for agent, hand in zip(agents, hands):
        draw_or_discard_phase = 0
        drawn_card = None

        # if 0, draw from face down, if 1, draw from face up
        draw_action = int(round(np.array(agent.predict([[draw_or_discard_phase, 1, 1, 1, 1, 1, 1, 1, 1, 1,]]))[0][0]))

        if draw_action == 0:
            print("Drawing from draw pile")
            hand.draw_from_draw_pile()
        elif draw_action == 1:
            print("Drawing from discard pile")
            drawn_card = deck.discard_pile_top
            hand.draw_from_discard_pile()

        draw_or_discard_phase = 1
        discard_action = list_softmax(np.array(agent.predict([[draw_or_discard_phase, 1, 1, 1, 1, 1, 1, 1, 1, 1,]]))[0][1:])

        id_primary = np.argmax(discard_action)
        print("Discarding card: " + str(hand[id_primary]))

        if drawn_card:
            if drawn_card == hand[id_primary]:
                print("Can't dicard card drawn from discard pile")

                discard_action = np.delete(discard_action, id_primary)
                id_secondary = np.argmax(discard_action)

                print("Discarding instead card: " + str(hand[id_secondary]))

