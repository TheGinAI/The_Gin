import os

from tf_agents.agents.ddpg.actor_network import ActorNetwork
from tf_agents.agents.ddpg.critic_network import CriticNetwork
from tf_agents.drivers.dynamic_step_driver import DynamicStepDriver
from tf_agents.drivers.py_driver import PyDriver
from tf_agents.policies import random_tf_policy, PyTFEagerPolicy

os.environ['TF_USE_LEGACY_KERAS'] = '1'

import tf_agents.agents
from tf_agents.environments import TFPyEnvironment
from tf_agents.specs import ArraySpec, BoundedArraySpec, tensor_spec
import tensorflow as tf
from tf_agents.replay_buffers import reverb_replay_buffer
from tf_agents.replay_buffers import reverb_utils
from tf_agents.trajectories import trajectory
import reverb



from py_gin_env import PyGinEnv

learning_rate = 1e-3

# tf_agents.networks.sequential.Sequential([
#     tf.keras.layers.Dense(64, activation="relu"),
#     tf.keras.layers.Dense(64, activation="relu"),
#     tf.keras.layers.Dense(env.action_spec().shape[0], activation="linear"),
# ]),
# tf_agents.networks.sequential.Sequential([
#     tf.keras.layers.Ca
#     tf.keras.layers.Concatenate(axis=-1),
#     tf.keras.layers.Dense(64, activation="relu"),
#     tf.keras.layers.Dense(64, activation="relu"),
#     tf.keras.layers.Dense(1, activation="linear"),
# ]),


def make_agent(env):
    ddpg = tf_agents.agents.DdpgAgent(
        env.time_step_spec(),
        env.action_spec(),
        ActorNetwork(
            env.observation_spec(),
            env.action_spec(),
            fc_layer_params=(64, 64),
            dropout_layer_params=None,
            conv_layer_params=None,
            activation_fn=tf.keras.activations.relu,
            kernel_initializer=None,
            last_kernel_initializer=None,
            name="ActorNetwork"
        ),
        CriticNetwork(
            (env.observation_spec(), env.action_spec()),
            observation_conv_layer_params=None,
            observation_fc_layer_params=None,
            observation_dropout_layer_params=None,
            action_fc_layer_params=None,
            action_dropout_layer_params=None,
            joint_fc_layer_params=(64, 64),
            joint_dropout_layer_params=None,
            activation_fn=tf.keras.activations.relu,
            output_activation_fn=None,
            kernel_initializer=None,
            last_kernel_initializer=None,
            last_layer=None,
            name="CriticNetwork"
        ),
        tf.keras.optimizers.Adam(learning_rate=learning_rate),
        tf.keras.optimizers.Adam(learning_rate=learning_rate)
    )

    ddpg.initialize()
    return ddpg

def card_suit(card_id):
    poker_deck = {
    0: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': 'A ', 'suit': 'Club'},
    1: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': 'A ', 'suit': 'Diamond'},
    2: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': 'A ', 'suit': 'Heart'},
    3: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': 'A ', 'suit': 'Spade'},
    4: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '2 ', 'suit': 'Club'},
    5: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '2 ', 'suit': 'Diamond'},
    6: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '2 ', 'suit': 'Heart'},
    7: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '2 ', 'suit': 'Spade'},
    8: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '3 ', 'suit': 'Club'},
    9: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '3 ', 'suit': 'Diamond'},
    10: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '3 ', 'suit': 'Heart'},
    11: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '3 ', 'suit': 'Spade'},
    12: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '4 ', 'suit': 'Club'},
    13: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '4 ', 'suit': 'Diamond'},
    14: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '4 ', 'suit': 'Heart'},
    15: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '4 ', 'suit': 'Spade'},
    16: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '5 ', 'suit': 'Club'},
    17: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '5 ', 'suit': 'Diamond'},
    18: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '5 ', 'suit': 'Heart'},
    19: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '5 ', 'suit': 'Spade'},
    20: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '6 ', 'suit': 'Club'},
    21: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '6 ', 'suit': 'Diamond'},
    22: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '6 ', 'suit': 'Heart'},
    23: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '6 ', 'suit': 'Spade'},
    24: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '7 ', 'suit': 'Club'},
    25: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '7 ', 'suit': 'Diamond'},
    26: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '7 ', 'suit': 'Heart'},
    27: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '7 ', 'suit': 'Spade'},
    28: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '8 ', 'suit': 'Club'},
    29: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '8 ', 'suit': 'Diamond'},
    30: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '8 ', 'suit': 'Heart'},
    31: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '8 ', 'suit': 'Spade'},
    32: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '9 ', 'suit': 'Club'},
    33: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '9 ', 'suit': 'Diamond'},
    34: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '9 ', 'suit': 'Heart'},
    35: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '9 ', 'suit': 'Spade'},
    36: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '10', 'suit': 'Club'},
    37: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '10', 'suit': 'Diamond'},
    38: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '10', 'suit': 'Heart'},
    39: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '10', 'suit': 'Spade'},
    40: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': 'J ', 'suit': 'Club'},
    41: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': 'J ', 'suit': 'Diamond'},
    42: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': 'J ', 'suit': 'Heart'},
    43: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': 'J ', 'suit': 'Spade'},
    44: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': 'Q ', 'suit': 'Club'},
    45: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': 'Q ', 'suit': 'Diamond'},
    46: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': 'Q ', 'suit': 'Heart'},
    47: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': 'Q ', 'suit': 'Spade'},
    48: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': 'K ', 'suit': 'Club'},
    49: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': 'K ', 'suit': 'Diamond'},
    50: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': 'K ', 'suit': 'Heart'},
    51: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': 'K ', 'suit': 'Spade'},
    52: {'rank_code': '|', 'suit_code': ' ', 'rank': '  ', 'suit': 'side_blocker'},
    53: {'rank_code': ' ', 'suit_code': '_', 'rank': '__', 'suit': 'up_blocker'},
    54: {'rank_code': ' ', 'suit_code': '_', 'rank': '__', 'suit': 'down_blocker'},
    55: {'rank_code': '', 'suit_code': '\U0001F0A0', 'rank': ' x', 'suit': 'deck'},
    56: {'rank_code': '|', 'suit_code': '?', 'rank': '? ', 'suit': 'unknown'},
}  
    return "".join(poker_deck[card_id][i] for i in ['rank_code','suit_code','rank','rank_code'])

def card_shown(deck,discard_card,discard_amount,active,*players,**kw):
    assert len(players) <= 7 
    
    print("".join("=" for _ in range(60)))
    print(" The Gin - Interactive AI Card Game")
    
    for p, hand in enumerate(players, start=1):
        print("","".join("_" for _ in range((len(hand)*6)+10)))
#         print("|           ","     ".join(str(i) for i in range(len(hand))),"  |")
        print("|         "," ".join(card_suit(53)for _ in hand),"|")
        
        if active == 0 or active == p:
            print("|player %d:"%p," ".join(card_suit(i) for i in hand),"|")
        else:
            print("|player %d:"%p," ".join(card_suit(56) for _ in hand),"|")
        
        print("|         "," ".join(card_suit(52)for _ in hand),"|")
        print("|           ","     ".join(str(i+1) for i in range(len(hand))),"  |")
        print("","".join("-" for _ in range((len(hand)*6)+10)))
        

    print("")
    print(" deck:", "".join(card_suit(55)), str(deck))
    print("           "," ".join(card_suit(53)for _ in range(1)))
    print(" discarded:"," ".join(card_suit(i) for i in [discard_card]),'- amount:',"".join(card_suit(55)), str(discard_amount))
    print("           "," ".join(card_suit(52)for _ in range(1)),"".join(" " for _ in range(12)))
    print("".join("=" for _ in range(60)))


def make_reverb(i, env, agent):
    table_name = 'uniform_table_' + str(i)
    replay_buffer_signature = tensor_spec.from_spec(agent.collect_data_spec)
    replay_buffer_signature = tensor_spec.add_outer_dim(replay_buffer_signature)

    table = reverb.Table(
        table_name,
        max_size=100000,
        sampler=reverb.selectors.Uniform(),
        remover=reverb.selectors.Fifo(),
        rate_limiter=reverb.rate_limiters.MinSize(1),
        signature=replay_buffer_signature)

    reverb_server = reverb.Server([table])

    replay_buffer = reverb_replay_buffer.ReverbReplayBuffer(
        agent.collect_data_spec,
        table_name=table_name,
        sequence_length=2,
        local_server=reverb_server)

    rb_observer = reverb_utils.ReverbAddTrajectoryObserver(
        replay_buffer.py_client,
        table_name,
        sequence_length=2)

    random_policy = random_tf_policy.RandomTFPolicy(env.time_step_spec(), env.action_spec())

    PyDriver(
        env,
        PyTFEagerPolicy(
            random_policy, use_tf_function=True),
        [rb_observer],
        max_steps=100).run(env.reset())

    dataset = replay_buffer.as_dataset(
        num_parallel_calls=3,
        sample_batch_size=10,
        num_steps=2).prefetch(3)

    return reverb_server, rb_observer, dataset, iter(dataset)


# Might get stuck if it can't find winning card
def test_marl(env, policy):
    agn_return = 0.0
    rng_return = 0.0
    random_policy = random_tf_policy.RandomTFPolicy(env.time_step_spec(), env.action_spec())
    time_step = env.reset()
    env.action("GUI_MODE")

    while True:
        # trained agent, draw move
        draw_action = policy.action(time_step)
        time_step = env.step(draw_action.action)
        agn_return += time_step.reward

        if time_step.is_last():
            return [agn_return, rng_return]

        # trained agent, discard move
        discard_action = policy.action(time_step)
        time_step = env.step(discard_action.action)
        agn_return += time_step.reward

        # Player 1 finish
        env.action("LST_HAND")
        card_shown(len(env._deck.draw_pile),env._deck.discard_pile_top.card_id,len(env._deck.discard_pile),0,[card.card_id for card in env._hands[0]],[card.card_id for card in env._hand[1]])
        input()

        if time_step.is_last():
            return [agn_return, rng_return]

        # random
        draw_action = random_policy.action(time_step)
        time_step = env.step(draw_action.action)
        rng_return += time_step.reward

        if time_step.is_last():
            return [agn_return, rng_return]

        discard_action = random_policy.action(time_step)
        time_step = env.step(discard_action.action)
        rng_return += time_step.reward

        #Player 2 Finishes
        card_shown(len(env._deck.draw_pile),env._deck.discard_pile_top.card_id,len(env._deck.discard_pile),0,[card.card_id for card in env._hands[0]],[card.card_id for card in env._hand[1]])
        input()

        if time_step.is_last():
            return [agn_return, rng_return]

if __name__ == "__main__":
    eval_env = TFPyEnvironment(PyGinEnv(2))
    train_env = PyGinEnv(2)
    agents = [make_agent(train_env) for _ in range(2)]
    reverbs = [make_reverb(i, train_env, agents[i]) for i in range(2)]

    # (Optional) Optimize by wrapping some of the code in a graph using TF function.
    #agent.train = common.function(agent.train)

    # Reset the train step.
    for agent in agents:
        agent.train_step_counter.assign(0)

    # Evaluate the agent's policy once before training.
    sums = [0.0] * len(agents)
    for _ in range(5):
        for i, x in enumerate(test_marl(eval_env, agents[0].policy)):
            sums[i] += x

    for i in range(len(sums)):
        sums[i] /= 5

    returns = [sums]
    print(returns)

    # Reset the environment.
    time_step = train_env.reset()

    # Create a driver to collect experience.
    collect_drivers = [PyDriver(train_env, PyTFEagerPolicy(agent.collect_policy, use_tf_function=True), [reverb[1]], max_steps=2, max_episodes=1) for agent, reverb in zip(agents, reverbs)]

    for _ in range(1000000):
        for agent, reverb, collect_driver in zip(agents, reverbs, collect_drivers):
            iterator = reverb[3]

            # Collect a few steps and save to the replay buffer.
            time_step, _ = collect_driver.run(time_step)

            # Sample a batch of data from the buffer and update the agent's network.
            experience, unused_info = next(iterator)
            train_loss = agent.train(experience).loss

            step = agent.train_step_counter.numpy()

            if step % 100 == 0:
                print('step = {0}: loss = {1}'.format(step, train_loss))

        if step % 1000 == 0:
            sums = [0.0] * len(agents)
            for _ in range(5):
                for i, x in enumerate(test_marl(eval_env, agents[0].policy)):
                    sums[i] += x

            for i in range(len(sums)):
                sums[i] /= 5

            print('step = {0}: Average Return = {1}'.format(step, sums))
            returns.append(sums)
