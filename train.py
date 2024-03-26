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
    done = False
    update_rate = 100  # match marl/maddpg.py/max_transition_experience
    step = 0

    # Create environment
    deck = Deck()
    hands = deck.deal(2)
    agents = [MADDPGAgent(), MADDPGAgent()]

    prev_obs_draw = [[], []]
    prev_obs_discard = [[], []]

    prev_obs_draw[0] = [0, deck.discard_pile_top.card_id] + [x.card_id for x in hands[0]] + [0]
    prev_obs_draw[1] = [0, deck.discard_pile_top.card_id] + [x.card_id for x in hands[1]] + [0]

    prev_obs_discard[0] = [1, deck.discard_pile_top.card_id] + [x.card_id for x in hands[0]] + [0]
    prev_obs_discard[1] = [1, deck.discard_pile_top.card_id] + [x.card_id for x in hands[1]] + [0]

    while True:
        tmp_transition_draw = [[], []]
        tmp_transition_discard = [[], []]

        for agn in range(2):
            draw_or_discard_phase = 0
            drawn__discard_card = None

            draw_obs = [draw_or_discard_phase, deck.discard_pile_top.card_id] + [x.card_id for x in hands[agn]] + [0]

            # if 0, draw from face down, if 1, draw from face up
            draw_action_full = np.array(agents[agn].predict([draw_obs]))[0]
            draw_action = int(round(draw_action_full[0]))

            if draw_action >= 0:
                #print("Drawing from draw pile")
                hands[agn].draw_from_draw_pile()
            elif draw_action < 0:
                #print("Drawing from discard pile")
                drawn__discard_card = deck.discard_pile_top
                hands[agn].draw_from_discard_pile()

            draw_or_discard_phase = 1
            discard_obs = [draw_or_discard_phase, deck.discard_pile_top.card_id] + [x.card_id for x in hands[agn]]
            discard_action_full = np.array(agents[agn].predict([discard_obs]))[0]
            discard_action = list_softmax(discard_action_full[1:])

            id_primary = np.argmax(discard_action)
            #print("Discarding card: " + str(hands[agn][id_primary]))

            if drawn__discard_card:
                if drawn__discard_card == hands[agn][id_primary]:
                    #print("Can't dicard card drawn from discard pile")

                    discard_action = np.delete(discard_action, id_primary)
                    id_secondary = np.argmax(discard_action)

                    #print("Discarding instead card: " + str(hands[agn][id_secondary]))
                    hands[agn].discard(id_secondary)
                else:
                    hands[agn].discard(id_primary)
            else:
                hands[agn].discard(id_primary)

            reward = hands[agn].reward()
            if hands[agn].check():
                done = True

            tmp_transition_draw[agn] = (prev_obs_draw[agn], draw_action_full, reward, draw_obs)
            tmp_transition_discard[agn] = (prev_obs_discard[agn], discard_action_full, reward, discard_obs)

            prev_obs_draw[agn] = draw_obs
            prev_obs_discard[agn] = discard_obs

        for agn in range(2):
            agents[agn].add_transition_draw(
                [tmp_transition_draw[0][0], tmp_transition_draw[1][0]],
                [tmp_transition_draw[0][1], tmp_transition_draw[1][1]],
                tmp_transition_draw[agn][2],
                [tmp_transition_draw[0][3], tmp_transition_draw[1][3]],
                done
            )

            agents[agn].add_transition_discard(
                [tmp_transition_discard[0][0], tmp_transition_discard[1][0]],
                [tmp_transition_discard[0][1], tmp_transition_discard[1][1]],
                tmp_transition_discard[agn][2],
                [tmp_transition_discard[0][3], tmp_transition_discard[1][3]],
                done
            )

            if step % update_rate == 0 and step != 0:  # only update every 100 steps
                print(step)
                q_loss, pol_loss = agents[agn].update(agents, step)

        print(step)
        step += 1

        if done:
            print(agn, " WON")
            break