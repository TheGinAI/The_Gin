# The Gin - Interactive AI Card Game

## Introduction
The goal of our project is to train a Machine Learning model using TensorFlow to win a game of Gin in as few moves as possibly, so that we can observe the limits of current open-source learning model libraries -- which in our case is TensorFlow's Python library.  

For many, the card game "gin" has little to do with strategy and more to do with the luck of the draw. With the nature of this project, we can solve this contingency while simultaneously running the risk of discovering never before seen strategies, defining what are the outlier environmental variables (starting hands/decks) and how they impacted the training process, demonstrating how a simple game can be used as the medium to support a complex deep learning network and simplifying the network for teaching/presentation purposes, finding what limitations there were (if any) with TensorFlow during the training phase of our model, and reaching an answer to if our methodology was truly the best (open-source) approach.

Our approach will be done by setting up a set of parameters that our model will explore, with the hope that after 10,000 training iterations -- it can maintain a superhuman win rate which will be defined later on. The roadmap for this is simple: First, using Python we will define the environment for the model to train in. Next, we will design a TF (TensorFlow) model to play gin against a copy of itself. Then through trial and error, remove/add/optimize the models learning parameters until they learn to play at our soon to be defined, "superhuman win rate". Finally, create support for a human to play one-on-one against our model to showcase its progress.

## Description
The goal is to train a artificial neural network agent to be able to interactively play against a human.
To achieve this we will leverage several interesting Machine Learning tools, utilities and concepts.
Those include **Python** with object oriented programming, **TensorFlow** learning and inference,
**Reinforcement Learning** with multiple **Agents**, and data visualization using matplotlib and custom 
graphics displays. We will also make use of numpy for speed optimization.

### Gin card game
We have decided to train the artificial neural network to play Gin, this is because this card game has properties that play well
with neural network models. Specifically, the number of observations and actions is always the same, which is a
prerequisite for any artificial neural network. Besides this Gin also has a very clear win/loss condition,
that does not leave any ambiguities as to how one got to a winning hand.

The rules of Gin are as follows:
1. Deck of cards with jokers removed is used (52 cards)
2. Each player is dealt 7 cards
3. One more card is drawn and placed face-up next to the deck
4. The player left of the dealer goes first
5. Player must pick either a face-down card from the deck, or a face-up card next to the deck
6. Player must discard 1 card to the face-up pile next to the deck
   - If a card was drawn from the face-up pile, then that same card can not immediately be discarded
   - If a card was drawn from the face-down deck, it may be immediately discarded
   - Otherwise, a card that is in the players hand at the start of their turn may be discarded
   - At the end of their turn, the player must always have exactly 7 cards in their hand
7. The first player to have one set or run of 3 cards and one set or run of 4 cards wins
   - Valid set is when the player has 3 or 4 cards of the rank (and different suits), e.g. two of clubs, hearts, and spades
   - Valid run is when the player has 3 or 4 cards in sequence of the same suit, e.g. two, three, and four of clubs
   - Ace cards can either be counted as before 'two' or after 'king', wrapping around (e.g. king, ace, two) is not allowed
   - Player indicates that they have won by discarding the card that is not part of their winning face-down on the discard pile

### Tools & Approach Discussion

#### Python
Due to the nature of anything related to machine learning being very dynamic with usually many parameters that need to be tuned
or the need to entirely change the approach to the problem, a scripting language like Python is ideal. This is because if a change is needed,
there is no need to recompile the entire project, it is as simple as making the change and re-running the code. This allows us to test changes faster
to arrive at a working solution with less time spent waiting for the code to compile and more time actually analyzing the code and results.
Another benefit is that for projects that build upon very complex concepts like machine learning, but do not necessarily need that much code
because it is covered by libraries like TensorFlow, a easy to read high-level scripting language like Python allows to focus on the main problem at hand
instead of various complicated syntax and programming structures. Python also has tools like matplotlib that make data visualization easy to add, and another tool
called NumPy that allow leveraging the speed of C for processing intensive tasks which will help us get more training done in less time.

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
In the world we are living in today, it is crucial to utilize limited resources better to maximize our profit in the minimum possible time. In this instance, we are facing a similar objective to the card game 'gin', whose goal is to form a specific combination in as few turns as possible. The project aims to develop a reinforcement learning algorithm-trained AI card game named 'gin' that allows humans to play against AI. The game 'gin' is played by observing other players' discarded cards and your current deck to form a combination of sets and runs. The training process is completed by having two AI agents complete a set and run a combination with seven cards in the shortest turns possible. AI agents will be able to observe and analyze other's player's actions to make better decisions. Moreover, this project is introduced for both educational and entertainment purposes.

### Education
For educational purpose, the projects aims to test and compare the limit of AI agent's decision making in shared resources with limit memory space to decent human players. This project will be developed with TensorFlow's environment-agent feature that allows user to develop their action environment, agent steps, and rewarding systems for their specific goal. The learning / training process is done through unsupervised learning to investigate the AI agent's ability in decision making. We are hoping to see the difference between an AI-agent and a human player's actions by testing if AI-agents are able to analyse other player's action and avoid forming the same combination. Furthermore, human players tend to eventually figure that another player is holding on to the cards they need to be able to finish their set or run and we would like to see how AI-agent would handle this instance. 

### Entertainment
For entertainment purpose, we are aiming to develop a more human-like AI agent in card game by modying it is memory space. Typically, an AI agent is difficult to compete with due to its memory capability. For instance, the AI agent will be able to remember all past discarded cards to analyze what cards are still in the deck and decide its target combination accordingly. We are aiming to limit the AI agent's memory space to make them more human-like to create cases where AI agent and human players will be coincidentally forming the same combination; this will add more entertainment value.


