import os

from tf_agents.agents.ddpg.actor_network import ActorNetwork
from tf_agents.agents.ddpg.critic_network import CriticNetwork

os.environ['TF_USE_LEGACY_KERAS'] = '1'

import tf_agents.agents
from tf_agents.environments import TFPyEnvironment
from tf_agents.specs import ArraySpec, BoundedArraySpec
import tensorflow as tf



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


# Might get stuck if it can't find winning card
def test_marl(env, policies):
    returns = [0.0] * len(policies)
    time_step = env.reset()

    while True:
        for i, policy in enumerate(policies):
            draw_action = policy.action(time_step)
            time_step = env.step(draw_action.action)
            returns[i] += time_step.reward

            discard_action = policy.action(time_step)
            time_step = env.step(discard_action.action)
            returns[i] += time_step.reward

            if time_step.is_last():
                return returns


if __name__ == "__main__":
    env = TFPyEnvironment(PyGinEnv(2))
    agents = [make_agent(env) for _ in range(2)]

    print(test_marl(env, [x.policy for x in agents]))

    #x.policy
    #avg_return = compute_avg_return(eval_env, agent.policy, num_eval_episodes)