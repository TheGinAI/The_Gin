import numpy as np
import tensorflow as tf

from marl.replay_buffer import EfficientReplayBuffer

tau = 0.01
clip_norm = 0.5
buff_size = 5
obs_shape = (8,)
act_shape = (8,)
batch_size = 1
decay = 0.95  # gamma
max_transition_experience = 100
total_num_agents = 2


class Agent:
    def __init__(self):
        self.critic = CriticNetwork()
        self.critic_target = CriticNetwork()
        self.critic_target.model.set_weights(self.critic.model.get_weights())

        self.actor = ActorNetwork(self.critic)
        self.actor_target = ActorNetwork(self.critic)
        self.actor_target.model.set_weights(self.actor.model.get_weights())

        self.replay_buffer = EfficientReplayBuffer(max_transition_experience, total_num_agents, obs_shape[0], act_shape[0])

    def save(self, path):
        self.critic.model.save_weights(path + 'critic.h5', )
        self.critic_target.model.save_weights(path + 'critic_target.h5')
        self.actor.model.save_weights(path + 'actor.h5')
        self.actor_target.model.save_weights(path + 'actor_target.h5')

    def load(self, path):
        self.critic.model.load_weights(path + 'critic.h5')
        self.critic_target.model.load_weights(path + 'critic_target.h5')
        self.actor.model.load_weights(path + 'actor.h5')
        self.actor_target.model.load_weights(path + 'actor_target.h5')

    def predict(self, obs):
        return self.actor.predict(obs)

    def target_predict(self, obs):
        return self.actor_target.predict(obs)

    def add_transition(self, obs_n, act_n, rew, new_obs_n, done_n):
        self.replay_buffer.add(obs_n, act_n, rew, new_obs_n, float(done_n))

    def target_update(self):
        # update critic
        net_weights = np.array(self.critic.model.get_weights())
        target_net_weights = np.array(self.critic_target.model.get_weights())
        new_weights = tau * net_weights + (1.0 - tau) * target_net_weights
        self.critic_target.model.set_weights(new_weights)

        # update actor
        net_weights = np.array(self.actor.model.get_weights())
        target_net_weights = np.array(self.actor_target.model.get_weights())
        new_weights = tau * net_weights + (1.0 - tau) * target_net_weights
        self.actor_target.model.set_weights(new_weights)

    def update(self, agents, step):
        obs_n, acts_n, rew_n, next_obs_n, done_n = self.replay_buffer.sample(batch_size)
        weights = tf.ones(rew_n.shape)

        # Train the critic, using the target actions in the target critic network, to determine the
        # training target (i.e. target in MSE loss) for the critic update.
        target_act_next = [a.target_action(obs) for a, obs in zip(agents, next_obs_n)]
        target_q_next = self.critic_target.predict(next_obs_n, target_act_next)
        q_train_target = rew_n[:, None] + decay * target_q_next

        td_loss = self.critic.train(obs_n, acts_n, q_train_target, weights).numpy()[:, 0]

        # Train the policy.
        policy_loss = self.actor.train(obs_n, acts_n)

        # Update target networks.
        self.target_update()


class ActorNetwork:
    def __init__(self, critic_network):
        self.critic_network = critic_network
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)

        self.input_layer = tf.keras.layers.Input(shape=obs_shape, dtype=tf.int8)

        self.hidden_layers = []
        self.hidden_layers.append(tf.keras.layers.Dense(64, activation="relu"))
        self.hidden_layers.append(tf.keras.layers.Dense(64, activation="relu"))

        self.output_layer = tf.keras.layers.Dense(act_shape[0], activation="softmax")

        self.model = tf.keras.Sequential()
        self.model.add(self.input_layer)
        self.model.add(self.hidden_layers[0])
        self.model.add(self.hidden_layers[1])
        self.model.add(self.output_layer)

    def predict(self, obs):
        return self.model(tf.convert_to_tensor(obs), training=False)

    @tf.function
    def train(self, obs):
        with tf.GradientTape() as tape:
            act = self.predict(obs)
            act_q = self.critic_network.predict(obs, act)
            policy_regularization = tf.math.reduce_mean(tf.math.square(act))
            loss = -tf.math.reduce_mean(act_q) + 1e-3 * policy_regularization

        gradients = tape.gradient(loss, self.model.trainable_variables)

        """
        Clips gradients by their own norm (needed for MADDPG)
        instead of global norm (suggested by TF docs).
        """
        for i, gradient in enumerate(gradients):
            gradients[i] = tf.clip_by_norm(gradient, clip_norm)

        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        return loss


class CriticNetwork:
    """
    Also known as Q-Network
    """
    def __init__(self):
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)

        self.input_layer = tf.keras.layers.Input(shape=(obs_shape[0] + act_shape[0],), dtype=tf.int8)

        self.hidden_layers = []
        self.hidden_layers.append(tf.keras.layers.Dense(64, activation="relu"))
        self.hidden_layers.append(tf.keras.layers.Dense(64, activation="relu"))

        self.output_layer = tf.keras.layers.Dense(1, activation="linear")

        self.model = tf.keras.Sequential()
        self.model.add(self.input_layer)
        self.model.add(self.hidden_layers[0])
        self.model.add(self.hidden_layers[1])
        self.model.add(self.output_layer)

    def predict(self, obs, act):
        """
        concatenation might not work in tf.function, hence wrapper
        """
        return self.__predict(obs + act)

    @tf.function
    def __predict(self, cat):
        return self.model(cat)

    def train(self, obs, act, target_q, weights):
        """
        concatenation might not work in tf.function, hence wrapper
        """
        return self.__train(obs + act, target_q, weights)

    @tf.function
    def __train(self, cat, target_q, weights):
        with tf.GradientTape() as tape:
            pred_q = self.__predict(cat)
            td_loss = tf.math.square(target_q - pred_q)
            loss = tf.reduce_mean(td_loss * weights)

        gradients = tape.gradient(loss, self.model.trainable_variables)

        """
        Clips gradients by their own norm (needed for MADDPG)
        instead of global norm (suggested by TF docs).
        """
        for i, gradient in enumerate(gradients):
            gradients[i] = tf.clip_by_norm(gradient, clip_norm)

        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        return td_loss
