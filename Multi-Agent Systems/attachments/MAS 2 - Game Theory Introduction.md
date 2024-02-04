(Slide deck 2 - GT & Pareto)

The science of strategic thinking, the mathematical study of interaction among independent, self-interested agents. This is to say, agents are (partially) competing for the same utility.

Agents are:
* Having preferences (structured in terms of an utility function)
* Self-interested (striving to maximise their own payoff)
* rational (They reason about their actions and decide rationally to maximise their own self-interest)
This is the simplest setup from which we can get results. It might not always be optimal.
-> All models are wrong, however, some are useful.
After evaluation, player's might end up with a strategy to follow upon
* A pure strategy is to always do the same thing
* A mixed strategy is to perform an action with a chance
-> slide 18 for calculating the utility of each of these, which should be trivial.

An n-person normal-form game is a tuple (n, A, u):
* N is the set of players
* A is the list of actions, where A_i is the set of actions available to a given player
    * Some specific solution is usually represented as a lowercase "a"
* u is the utility function
    * Preference can be written up in a function iff they are complete (any can be compared to any) and commutative (a < b and b < c -> a < c)

Setting up the rules for the game in such a way that the outcome is what is desired is sometimes called inverse game theory

There are multiple types of games
* zero sum (competitive) / positive sum (coordination) games
    * In zero sum games, it is proven there is always an optimum strategy
* Simultaneous / Sequential.
    * Either no one knows what the others are about to do, or you can watch. For example, rock paper scissors vs chess.
    * Simultaneous games can be put in the familiar matrices from economics.
    * Sequential trees can be put in game / decision trees.
* Cooperative / non-cooperative
    * in non-cooperative games, cooperation has to emerge, this is to say, there is some way in which everyone can get better. There cannot be contracts signed beforehand.
    * In cooperative games, contracts can exist


Normal form (Simultaneous and immediate payoff, the later of which is not mentioned again in any lecture) games can be written in matrices, here is a random example of one:

| | Left | Centre | Right | 
| --- | --- | --- | --- | 
| Up | 1, 0 | 1, 2 | 0, 1 | 
| Down | 0, 3 | 0, 1 | 2, 0 |

In these matricides,  Rows correspond to the actions of agent 1 (The "row player") and columns correspond to the actions of agent 2 (the "column player"). So, if player 1 decides to play "Up" and player 2 decides to play "Centre" the utility payoff is (1, 2), which is to say the row player gets 1 and the column player gets 2.

For these games, a strategy is something a player can decide beforehand to do. For example "Always play Up" or "Chose 50-50 between Centre and Right randomly." Strategies that have chances are mixed strategies, strategies without chances (so, just "do X" for normal form games, or what tree to follow for sequential games) are pure strategies.
-> Calculating the utility of a strategy "Expected utility for mixed strategies" is just multiplying all the possible utilities one *could* get with the chance that they happen.

In certain games, options can be Paetro-dominated [[EC lecture 11]] , meaning that some options might never be chosen. This happens when some point is worse in utility for all players. The options that are actually considered is the Paetro-optimal front
A strategy can also be dominated, which is to say that its utility is always lower (for all possible strategies of other agents) than another strategy.
* If one strategy is better *or equal* than another strategy in all cases, it only weakly dominates. The opposite is called strong domination
* If one strategy dominates all other strategies, it is *the* dominant strategy
-> To find solutions of a game, it is useful to eliminate all *strongly* dominated strategies from the possibilities to construct a smaller matrix. This is called IESDS "Iterated Elimination of Strictly Dominated Strategies", and is discussed again in [[MAS 3 - Named Game Strategies]]

##### Prisoner's dilemma
Actions -> C Cooperate, D -> Defect
* If they both cooperate, they both get reward R = 1
* if both defect, they get punishment P = 0
* With T > R Temptation pay-off and S < P sucker punishments for a prisonner's dillema.

| | 1 defects | 1 cooperates |
| --- | --- | --- |
| 2 defects | R, R | S, T |
| 2 cooperates | T, S | P, P |

There are more configurations, tough:
If S > P, and T < R there is harmony.
If T > R and S > P, There is greed -> Snowdrift / chicken / voluenteer
* Two drivers are blocked by snow drift on the road
* Both are reluctant to go out, tough, as they prefer the comfort of their car
* If they both shovel ,the discomfort is halved.

| | 1 defects | 1 cooperates |
| --- | --- | --- |
| 2 defects | 5, 5 | 3, 10 |
| 2 cooperates | 10, 3 | 0, 0 |

If S < P, and T < R, There is fear -> Stag hunt / Common interest game
* Two hunters know that a stag follow the same path
* If they cooperate and shoot the stag, there is plenty to eat
* They hide for a long time, and the stag does not show up. They do, however, spot rabits
* If one shoots a rabbit, the rabbits flee, and the stag is allarmed, so only one gets to eat.

| | 1 defects | 1 cooperates |
| --- | --- | --- |
| 2 defects | 10, 10 | 0, 4 |
| 2 cooperates | 4, 0 | 2, 2 |

If S < P and T > R, This is a prisoner's dilemma.
* The common story

| | 1 defects | 1 cooperates |
| --- | --- | --- |
| 2 defects | 1, 1 | -12, 0 |
| 2 cooperates | 0, -12 | -8, -8 |

Similar: split or steal. that famous "I am going to say steal" clip from the BBC

## Some names of games from the literature that might get used:
All of these are just names we give to particular types of configuration of normal-form games.

##### Hotelling's game / Ice cream time
* Two players, continuous action time
* Both have ice cream stands they can place somewhere on the beach
    * Customers go to the stand that is closest
-> Optimal strategy, both standing in the middle

##### Cournot Duopoly
* Two companies both put stuff on the market, but the price they get decreases as the amount of stuff put onto it by the two of them combined increases.

##### Congestion games / selfish routing
* In some road network, all people chose in the morning how to go to work.
* If too many people take the same path, 
    * Slide 33. Here, the amount of people going over a path is a number between 0 (no one) and 1 (everyone)
* Selfish people take, on average, longer than some person choosing the road in advance for everyone.

##### Tragedy of the commons
* n players have a common resource
* People's utility is dependent of the amount of that resource they take, and the amount that is left free, in such a way that they get 0 if everything is taken, but taking more is always more advantages to them. 

##### Public goods game
* N agents with some available capital K, putting it into some synergy bank account, that gets multiplied by some number greater than 1, and then redistributed evenly across all players.
* So, if the factor is 2 with four players, three of the players put in 20 euros, one puts in 0, the three make a profit of 18 euros, and the one free rider makes a profit of 38

##### Ultimatum game
* Kids get a box of ice-cream to share among themselves
* They can get all of it, as long as they agree on the division.
* If they fail to agree, they get nothing.
* It's a hot day, and the ice-cream is melting. So, the longer they argue, the less they get.

##### Traveller's dilemma
* An airline severely damages identical antiques purchased by two different travellers.
* They both have to tell the airline how much they think it is worth, and have no idea.
* If one guesses significantly higher than the other, the airline will presume the higher one is lying, and pay out the lower extra out of the pocket of the higher as "honesty reimbursement"

##### Penalty kicks
* Kicker can kick left or right
* Goalie can defend left or right
* Goalie wants to coordinate, kicker wants to ani-coordinate

##### Chicken's game
* The story of two guys in the 80s film who each want to be the last to break. 


