"""
Multi-Agent Simple
"""
import tf_agents.agents
from tf_agents.specs import ArraySpec, BoundedArraySpec
import tensorflow as tf

learning_rate = 1e-3
obs_space = 5
act_space = 5


class Agent:
    def __init__(self):
        self.ddpg = tf_agents.agents.DdpgAgent(
            tf_agents.trajectories.time_step_spec(
                BoundedArraySpec(shape=(obs_space,), dtype='int8'),
                ArraySpec(shape=(), dtype='float32'),
            ),
            BoundedArraySpec(shape=(act_space,), dtype='float32'),
            tf_agents.networks.sequential.Sequential([
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(act_space, activation="linear"),
            ]),
            tf_agents.networks.sequential.Sequential([
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(1, activation="linear"),
            ]),
            tf.keras.optimizers.Adam(learning_rate=learning_rate),
            tf.keras.optimizers.Adam(learning_rate=learning_rate)
        )

        self.ddpg.initialize()


if __name__ == "__main__":
    x = Agent()
    #x.policy
    #avg_return = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
