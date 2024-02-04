(Slide deck 2 - GT & Pareto)

Dominated & dominant & peatro-optimal from [[MAS 2 - Game Theory Introduction]]

#### IESDS
Iterated elimination of strictly dominated strategies.
* Basically, if you want to know what rational people are going to do, you can eliminate dominated strategies from both sides, and get a simpler game that way.
* As long as there is strict domination, the order of eliminating strategies does not matter.

#### Domination with a mixed strategy

| | L | H |
| --- | --- | --- |
| T | 0, 3 | 3, 0 |
| M | 1, 1 | 1, 1|
| B | 4, 0 | 0. 4|

Here, the strategy 50% chance of T and 50% chance of B dominates the strategy M, as 0.5x4 + 0.5x0 > 1 and 0.5x3 + 0.5x0 > 1
#### Best response:
The best response is defined as what to do in a case where you know what the other players are going to do.
* If two responses are the same, the player will be indifferent, and any mixing also works.
* This also works in a continuous space, and with mixed strategies.
    * For these, you take the partial derivative of the utility function to get the function that gives the best response for each input the other can do.
        * Setting these best responses to be equal gives *a* [[MAS 4 - Nash Equilibrium]]


(slide deck 3 - minregret safety nash)

Some of these strategies might seem weird, but they are there to prove a point. It's not necessarily true that rational agents will chose these strategies.
#### Regret minimisation
Regret -> Difference between what you actually got, and the best payoff you could have gotten with your opponents current choice
Maximum regret -> The biggest regret that could happen with the current choice.
Regret minimisation, then, is to chose the strategy that has the smallest maximum regret.

#### Safety Strategy / Maximin value
Safety strategy: What is the best outcome I can secure, irrespective of the opponent's action.
Worst possible outcome -> What is the worst thing that could happen if I do x
Then, pick the strategy with the maximum worse possible outcome.
* Relevant if the opponent is malicious
* Relevant for 0-sum games, where the opponent is not really malicious, but, rather, is trying to maximise their own. 
This also works with mixed strategies, for which there is the intuitive graph on slide 21

#### Punishment Strategy / minimax value
Pick the strategy such that the best response of the opponent is as low as possible.
The punishment strategy of player 2, results in the minimax valye of player 1
* This, too, works with mixed strategies.

#### Key takeaways from the strategies:
* The punishment strategy provides an upper bound to the safety strategy and vice versa
    * What your opponent can force on you is an upper bound to how safe you can be
    * What you can guarentee to get is a lower bound to what your opponent can force on you
* Which one is better, regret minimisation or safety depends on what type of game it is.
    * Slide 31 has a graph, on the S and T from [[MAS 2 - Game Theory Introduction]] prisoner's dilemma. 