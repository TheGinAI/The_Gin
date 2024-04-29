# The_Gin

A simple template of the project

## Description

The goal of our project is to train a machine learning model (MLM) using TensorFlow to play the best game of gin physically possible, so that we can observe the limits of current open-source MLM libraries -- which in our case is TensorFlow's Python library.

We are defining playing the best possible game of gin by balancing luck and skill, because in gin you need four out of seven cards to be exact in number to declare a legitimate win, but because of the seven cards in a hand being shuffled for randomness, it is possible for the MLM to draw a winning hand. In the event of such a case, there was no action that occurred prior to a win (reward), making that single iteration of the 10,000 completely useless for training purposes.

Essentially, the best possible game for the MLM to play is one where it does not at least win right off the bat, since it has to take -- a soon to be defined -- minimum number of actions for that iteration to yield learning progression in the epoch.

On the surface, the game has little room for strategy and more to do with the luck of the draw. Due to the nature of this project, we can solve this contingency while simultaneously running the risk of: Discovering unique case strategies to apply in a physical environment, defining a set of outlier environmental variables (starting hands/decks), while answering why and how they impacted the training process, demonstrating the ability of how simplicity can be used as the medium to support a complex machine learning network, allowing leeway for teaching/presentation purposes relating to machine learning, finding what limitations there were (if any) with TensorFlow during the training phase of our MLM, and answering if our methodology was truly the best (open-source) approach.

Our approach will be done by creating a set of parameters that our model will explore, with the hope that after 10,000 training iterations -- it can maintain a superhuman win rate (which will be defined later on). The roadmap for this is simple: First, using Python we will define the environment for the machine learning model to train in. Next is designing a TF (TensorFlow) MLM to play gin against a copy of itself. Then through trial and error, remove/add/optimize the MLM learning parameters until they learn to play at our soon to be defined, "superhuman win rate". Finally, create support for a human to play one-on-one against our model to showcase its progress.

### Group Members and Roles

* Kanglin Xu
   * CEO
* Tomas Rohatynski
   * President

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Development
This project aims to design and train an artificial neural network to play the card game gin. Similarly to the Alpha Go Zero developed by Google, our project aims to train the agent by having it play against itself and not import any game data from other players. The implementation is first designed based on MADDPG (Multi-Agent Deep Deterministic Actor-Critic Policy Gradient), where the learning involves multiple agents and environments and acts based on the other agent’s actions and environment policies. Later on, we modified the design to adapt DDPG for Multi-agent learning. To briefly summarize the essential implementation, we first define the rules of the card game gin in the environment, then design the agent that analyzes the environment and acts upon it.
Furthermore, the agent inputs the action based on observing the environment. The other agents input the actions based on the previous actions, and the environment will reward them based on their actions. The goal of each agent is to finish the combination of cards before the other agent does so. Within the project, we also analyze each agent’s actions and improve our reward definition to fine-tune the training. 

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

* Kanglin Xu - kanglin.xu@ttu.edu
* Tomas Rohatynski - trohatyn@ttu.edu

## Version History

* 0.2
    * Code Clean Up
    * Readme Update
* 0.1
    * Initial Release

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
[1] M. Abadi, A. Agarwal, P. Barham, E. Brevdo, Z. Chen,
C. Citro, G. S. Corrado, A. Davis, J. Dean, M. Devin,
S. Ghemawat, I. Goodfellow, A. Harp, G. Irving,
M. Isard, Y. Jia, R. Jozefowicz, L. Kaiser, M. Kudlur,
J. Levenberg, D. Man ́e, R. Monga, S. Moore, D. Murray,
C. Olah, M. Schuster, J. Shlens, B. Steiner, I. Sutskever,
K. Talwar, P. Tucker, V. Vanhoucke, V. Vasudevan,
F. Vi ́egas, O. Vinyals, P. Warden, M. Wattenberg,
M. Wicke, Y. Yu, and X. Zheng, “TensorFlow: Large-
scale machine learning on heterogeneous systems,”
2015, software available from tensorflow.org. [Online].
Available: https://www.tensorflow.org/
[2] J. Hu, M. P. Wellman et al., “Multiagent reinforcement
learning: theoretical framework and an algorithm.” in
ICML, vol. 98, 1998, pp. 242–250.
[3] L. Canese, G. C. Cardarilli, L. Di Nunzio, R. Fazzolari,
D. Giardino, M. Re, and S. Span`o, “Multi-agent reinforce-
ment learning: A review of challenges and applications,”
Applied Sciences, vol. 11, no. 11, p. 4948, 2021.
[4] Me!, “Gin rummy,” Dec 2018. [Online]. Available:
https://www.rummyrulebook.com/pages/gin-rummy/
[5] ——, “Straight gin,” Jan 2019. [Online]. Avail-
able: https://www.rummyrulebook.com/pages/straight-gin-
rummy/
[6] R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, and I. Mor-
datch, “Multi-agent actor-critic for mixed cooperative-
competitive environments,” Neural Information Process-
ing Systems (NIPS), 2017.
[7] T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez,
Y. Tassa, D. Silver, and D. Wierstra, “Continuous control
with deep reinforcement learning,” 2019.
