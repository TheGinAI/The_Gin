# The Gin - Interactive AI Card Game

## Introduction

## Description
In order to achieve our goal of training an agent to be able to interactively play against a human we will leverage
several interesting Machine Learning tools, utilities and concepts. Those include **Python** with object oriented programming, **TensorFlow** learning and inference,
**Reinforcement Learning** with multiple **Agents**, and data visualization using matplotlib and custom graphics displays. We will also make use of numpy for code optimization.

### Tools & Approach Discussion

#### Python
Due to the nature of anything related to machine learning being very dynamic with usually many parameters that need to be tuned
or the need to entirely change the approach to the problem, a scripting language like Python is ideal. This is because if a change is needed,
there is no need to recompile the entire project, it is as simple as making the change and re-running the code. This allows us to test changes faster
to arrive at a working solution with less time spent waiting for the code to compile and more time actually analyzing the code and results.
Another benefit is that for projects that build upon very complex concepts like machine learning, but do not necessarily need that much code
because it is covered by libraries like TensorFlow, a easy to read high-level scripting language like Python allows to focus on the main problem at hand
instead of various complicated syntax and programming structures.

#### Object Oriented Programming
In order to effectively train a machine learning network, it is crucial to run as much data in parallel as possible. OOP helps make this easier
thanks to being able to create self-contained objects that keep track of the data of each game, thus greatly simplifying organizing the data and reducing the risk
of intertwining data of different games. Since the object classes serve as templates, it is easy to quickly create many parallel tasks by simply instantiating the desired number of objects.

#### TensorFlow
This is one of the most fully-fledged and flexible machine learning libraries for Python. It accommodates any type of learning paradigm, network nodes and layouts, and preprocessing and postprocessing operations one can think of.
Thanks to its great range of functionality it makes it easy to evaluate and combine different methodologies while still working within that same library and not having to bridge multiple libraries together.
Using TensorFlow will aid us both in the prototyping stage with its flexibility and in the final code with how mature and fast it is. Once we have trained the neural network
to our satisfaction using the training harness that TensorFlow provides, we will the run the network in inference mode which will allow us to watch it play or play against a human.

#### Multi-agent Reinforcement Learning
When training an artificial neural network we want it to analyze as much data as possible so that it can train on a varied set of data and build enough experience off of it to deal with new cases that it has not seen before.
When working with big data acquiring enough examples for the network to analyze is easy, but in the case of a card game there are only so many unique cards and that is usually nowhere near enough data.
The alternative could be for the network to play against a human, and learn from the action taken by the human player, unfortunately this introduces human bias which is undesirable when training a neural network model. Besides that it would take many hours of human interaction to train it.
An optimal approach is thus for the neural network to generate the data it trains on itself, in layman's terms the neural network can learn by playing against a copy of itself.
This way the neural network can gather thousands of hours of playing experience in a manner of minutes comparing to playing at a human pace.
The reinforcement part of this learning approach is that the agents receive a reward/penalty based on how well they did in the match, they then try to maximize this reward parameter.
This allows them to develop strategies against each other on their own, which can potentially go beyond strategies that humans can develop.
The reward is also the caveat of reinforcement learning, because an improperly tuned reward function might cause the agent to overshoot their learning and become to used to playing a copy of itself and not be adaptable enough to play against a human.
Beyond the configuration of the neural network layers itself, the reward function will be one of the most crucial aspects to tune in order to reach desirable training outcomes.

## Motivation
In the world we're living in today, it's crucial to utilize limited resources better to maximize our profit in the minimum possible time. In this instance, we're facing a similar objective to the card game 'gin,' whose goal is to form a specific combination in as few turns as possible. The project aims to develop a reinforcement learning algorithm-trained AI card game named 'gin' that allows humans to play against AI. The game 'gin' is played by observing other players' discarded cards and your current deck to form a combination of sets and runs. The training process is completed by having two AI agents complete a set and run a combination with seven cards in the shortest turns possible. AI agents will be able to observe and analyze other's player's actions to make better decisions. Moreover, this project is introduced for both educational and entertainment purposes.

### Education
For educational purpose, the projects aims to test and compare the limit of AI agent's decision making in shared resources with limit memory space to decent human players. This project will be developed with TensorFlow's environment-agent feature that allows user to develop their action environment, agent steps, and rewarding systems for their specific goal. The learning / training process is done through unsupervised learning to investigate AI agent's ability in decision making. We're hoping to see the difference between AI-agent and human player's action by testing if AI-agent are able to analysis other player's action to avoiding forming the same combination. Further more, human player tends to debate between continuning competing other player in case with simular combination and we would like to see how AI-agent would handle this instance. 

### Entertainment
For entertainment purpose, we're aiming to develop a more human-like AI agent in card game by modying it's memory space. Typically, AI agent is difficult to compete with due to it's memory capability. For instance, AI agent will be able to remember all past discarded cards to analyze what cards are still in the deck and decide it's target combination accordingly. We're projecting to limit AI agent's memory space to make them more human-like to create cases where AI agent and human players will be coincidentally forming the same combination; this will add more entertainment value. 


