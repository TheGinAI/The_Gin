import numpy as np


class EfficientReplayBuffer(object):
    def __init__(self, size, n_agents, obs_shape_n, act_shape_n):
        """Create Prioritized Replay buffer.

        Parameters
        ----------
        size: int
            Max number of transitions to store in the buffer. When the buffer
            overflows the old memories are dropped.
        """
        self._obs_n = []
        self._acts_n = []
        self._obs_tp1_n = []
        self._n_agents = n_agents
        for idx in range(n_agents):
            self._obs_n.append(np.empty([size, obs_shape_n], dtype=np.float32))
            self._acts_n.append(np.empty([size, act_shape_n], dtype=np.float32))
            self._obs_tp1_n.append(np.empty([size, obs_shape_n], dtype=np.float32))
        self._done = np.empty([size], dtype=np.float32)
        self._reward = np.empty([size], dtype=np.float32)
        self._maxsize = size
        self._next_idx = 0
        self.full = False
        self.len = 0

    def __len__(self):
        return self.len

    def add(self, obs_t, action, reward, obs_tp1, done):
        for ag_idx in range(self._n_agents):
            self._obs_n[ag_idx][self._next_idx] = obs_t[ag_idx]
            self._acts_n[ag_idx][self._next_idx] = action[ag_idx]
            self._obs_tp1_n[ag_idx][self._next_idx] = obs_tp1[ag_idx]
        self._reward[self._next_idx] = reward
        self._done[self._next_idx] = done

        if not self.full:
            self._next_idx = self._next_idx + 1
            if self._next_idx > self._maxsize - 1:
                self.full = True
                self.len = self._maxsize
                self._next_idx = self._next_idx % self._maxsize
            else:
                self.len = self._next_idx - 1
        else:
            self._next_idx = (self._next_idx + 1) % self._maxsize

    def sample(self, batch_size):
        """
        Sample a batch of experiences.

        Parameters
        ----------
        batch_size: int
            How many transitions to sample.

        Returns
        -------
        obs_batch: np.array
            batch of observations
        act_batch: np.array
            batch of actions executed given obs_batch
        rew_batch: np.array
            rewards received as results of executing act_batch
        next_obs_batch: np.array
            next set of observations seen after executing act_batch
        done_mask: np.array
            done_mask[i] = 1 if executing act_batch[i] resulted in
            the end of an episode and 0 otherwise.
        """
        if batch_size > self.len:
            raise RuntimeError('Too few samples in buffer to generate batch.')

        indices = np.random.randint(self.len, size=[batch_size])

        obs_n = []
        acts_n = []
        next_obs_n = []
        for ag_idx in range(self._n_agents):
            obs_n.append(self._obs_n[ag_idx][indices])
            acts_n.append(self._acts_n[ag_idx][indices].copy())
            next_obs_n.append(self._obs_tp1_n[ag_idx][indices])

        rew = self._reward[indices]
        done = self._done[indices]
        return obs_n, acts_n, rew, next_obs_n, done