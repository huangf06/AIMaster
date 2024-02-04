(slidedeck 4 sequential games)

Represented with trees

Continuous values can be represented with arcs.

In contrast to the matrix-like simultaneous / normal-form games, which are also sometimes called "stage" games (as they deal with one stage), players can (partially) observe the other's actions, and react on them.

Games can be perfect / imperfect, and they can be complete / incomplete
* Perfect: All history of all players is known to all players
* Imperfect: Players might be unaware of what other players did.

* Complete: There is no private information, all players know the entire tree / matrix
* Imperfect: There is private information

There is a distinction between Mutual information and common knowledge
* Common knowledge: All players know, and all players know that all players know
* Mutual information: All players know, but no one is sure if the others know.

| | Perfect | Imperfect |
| --- | --- | --- |
| Complete | Chess | Simultaneous games |
| Incomplete | Open cry actions | Sealed bid auctions |

What type of equilibrium exists depends on complete / incomplete and sequential / simultaneous.

| | Simultaneous | Sequential |
| --- | --- | --- |
| Complete | Nash eq. | Backwards Induction |
| Incomplete | Bayesian Nash eq. | Perfect Nash eq.|

### Backwards induction
Presumes perfect information -> this is to say know what the other players did before them.
* The path found like this is usually called the equilibrium path.
* Backwards induction will always lead to a Nash equilibrium.
    * However, not all Nash equilibria are achievable, because some of them are based on "non-credible threads", which is to say that they presume a player made a non-rational decision earlier in the tree.
        * This is the same as saying that a Nash equilibrium might not be an equilibrium to all sub-games.
        * The "good" credible Nash equilibrium is called the perfect Nash equilibrium, or sub-game perfect Nash equilibrium or SPNE.
    * Here "Nash Equilibrium" means "what happens when you (bluntly) translate this tree into a matrix," for binary trees, each row/column would just be a series of "Left/right/right" for a matrix constructed like this.
        * This weird way of constructing a matrix is only really relevant for games with imperfect information.
        * This is called putting the tree in normal form, and can perhaps be better understood as a complete plan that each player makes in advance.

Example:
##### Stackelberg's duopoly
* A Sequential version of Cournout's duopoly [[MAS 2 - Game Theory Introduction]]. 
* By computing the partial derivatives of the optimal responses like usual, you can find that here, unlike the simultaneous version, the first mover has some advantage, as the leader is not playing best response to the follower: they don't have to.
