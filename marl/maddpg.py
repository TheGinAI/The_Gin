import numpy as np
import tensorflow as tf

tau = 0.01
clip_norm = 0.5


class Agent:
    def __init__(self):
        self.critic = CriticNetwork()
        self.critic_target = CriticNetwork()
        self.critic_target.model.set_weights(self.critic.model.get_weights())

        self.actor = ActorNetwork(self.critic)
        self.actor_target = ActorNetwork(self.critic)
        self.actor_target.model.set_weights(self.actor.model.get_weights())

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



class ActorNetwork:
    def __init__(self, critic_network):
        self.critic_network = critic_network
        self.optimizer = tf.keras.optimizers.Adam(lr=1e-4)

        self.input_layer = tf.keras.layers.Input(shape=(7,), dtype=tf.int8)

        self.hidden_layers = []
        self.hidden_layers.append(tf.keras.layers.Dense(64, activation="relu"))
        self.hidden_layers.append(tf.keras.layers.Dense(64, activation="relu"))

        self.output_layer = tf.keras.layers.Dense(5, activation="softmax")

        self.model = tf.keras.Sequential()
        self.model.add(self.input_layer)
        self.model.add(self.hidden_layers[0])
        self.model.add(self.hidden_layers[1])
        self.model.add(self.output_layer)

    def predict(self, obs):
        return self.model(obs, training=False)

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
        self.optimizer = tf.keras.optimizers.Adam(lr=1e-4)

        self.obs_input_layer = tf.keras.layers.Input(shape=(7,), dtype=tf.int8)
        self.act_input_layer = tf.keras.layers.Input(shape=(7,), dtype=tf.int8)
        self.input_layer = tf.keras.layers.Concatenate()([self.obs_input_layer, self.act_input_layer])

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
