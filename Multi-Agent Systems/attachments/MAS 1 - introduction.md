(Slide-deck 1: intro examples)

Multi-agent systems can be understood and justified in many different ways
* Systems with many different smaller robots can be modelled this way (e.g. warehouses)
* Micro services can be modelled this way
* Human interaction (with coordination and negotiation) can be simulated and studied this way.
* It can also be understood as Distributed AI (DAI), inspired on societies rather than individuals


#### Agent
An agent is some computer system that lives in a virtual environment and acts "autonomously" in it following some objectives. For this, they need to:
* Contain some logic as to what to do in what case
* Observe the environment
    * Accessible environment
    * Inaccessible environment
        * They might only observe a part, tough, in a partially observable environment
* Maintain knowledge about the environment
* Act in the environment
    * Not on all of it at once, tough. They might have smaller spheres of influence
* Communicate with the environment
    * Coordination (Cooperative setting)
        * Cooperation among non-antagonist agents
    * Negotiation (non-cooperative setting)
        * Coordination among self-interested agents

There are generally four types:
* Reflex agents
    * Some input/output machine
    * No state
    * Pre-computed rules
    * no partial observability
* Model-based reflex agent
    * Reflex agent with state
    * Can handle history because of that
* Goal-based agent
    * they have some goal, some objective function
        * Terminal goals
            * Inherent goals, no questions asked
        * Instrumental goals
            * Goals that help achieve the terminal goals.
    * They reason about which actions they should take in order to achieve the goal.
    * Less efficient, but more adaptive and flexible
    * Can be understood as "theorem proofing agents"
        * The goal is the theorem you want to prove, the known facts are the possible actions. 
* Utility-based agents
    * Some utility function instead of a goal
    * This allows them to evaluate trade-offs among conflicting goals
    * Rational agents that have a utility function are called strategic agents. 
* Intelligent agents
    * It is a system that is reactive, can respond, can learn, can act pro-active, can be social. It is able to be a flexible. 
    * These usually have four components:
        * Actor
        * Critic
        * Learner
        * Explorer

#### Environments
* accessible vs inaccessible -> Can all of the environment be seen at once?
* deterministic vs non-deterministic -> do the same actions always lead to the same outcome?
* Static vs dynamic -> Does the environment change for other reasons than the actor's actions
