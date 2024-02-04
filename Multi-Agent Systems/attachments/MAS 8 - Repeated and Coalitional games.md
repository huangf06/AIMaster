(slidedeck 5 GT negotiation iterated)

Repeat the same one-shot (stage) game. (special case of the sequential game.)

For a finite, and more importantly known amount of repetitions, the utility is just taken as the sum of utilities
For an infinite, which is equivalent to a unknown amount of repetitions, the utility is taken as a sum of increasingly discounted utilities of the single game.
* This is just to make it finite.
* Can be understood as a "now is more valuable than later" or as a "there is a chance that the random stopped moment has happened already."

This effects all sorts of outcomes e.g. Prisoner's dilemma:
* For finite versions, not so much. (The last round, you just defect, and then, for the second-to-last, you defect, so it does not change anything.)
* For infinite games, you have different strategies:
    * Tit-for-Tat. (Collaborate if the other collaborates, defect if your opponent defects)
    * Grim trigger. (Collaborate as long as opponent collaborates, but, as soon as they defect, defect yourself.)
        * This is not rational, Continued cooperation is, as long as delta (that discount you multiply by for every later version) is above one half.
            * Delta more than one half can be interpreted as the idea that at every point in time, the chance that there will be a next game, is more than 50%. (this might be specific to the payout, but the slides suggest not.)

## Coalitional Game theory
Basic modelling unit is the group, not the individual.

Transferable vs non-transferable utility
* Transferable: all agents in the group get part of the utility
    * Think money: the group can share it.
* non-transferable: the utility only matters per individual, it cannot be shared.

Synergy / super-additive games:
* If you add a member of the group, the total for the group goes up by more than one individual on their own.
    * In other words, all agents should work together, as the grand coalition outperforms any subset.

##### Shapely Value
The rational ways to split the utility of the group for Super-additive games.

For example: fair division of taxi fees:
* Some people are going home, and they are all on the same road, so they should take the taxi together, and split up the bill somehow.
    * The intuitive solution is to split the bill proportionally to the amount of distance *they* have to travel. (This is already the Shapely value, just calculated informally)
    * This can also be calculated as the average amount of money to pay over all permutations of paying order (if the furthest way pays first, the rest doesn't need to pay, if they arrive in order, they pay the additions.) This is equivalent to the Shapely value, if a little hard to proof.
* This intuition is correct for what Shapely is, but the actual maths is more complicated, see slide 11 and onwards. As formulas are given on the test, this might not be relevant to learn.

#### Shapely's Axioms
The Shapely value is the only value that is fair, which is to say that it is the only one that satisfies these axioms.
* Players are interchangeable if all their contributions are always the same
* Players are dummies if they can only contribute exactly as much as they would have been able to alone.