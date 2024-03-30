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

    while True:
        # trained agent
        draw_action = policy.action(time_step)
        time_step = env.step(draw_action.action)
        agn_return += time_step.reward

        if time_step.is_last():
            return [agn_return, rng_return]

        discard_action = policy.action(time_step)
        time_step = env.step(discard_action.action)
        agn_return += time_step.reward

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
