Authors: Ella Collins, Lonneke Langeveld, and Ritten Roothaert. 

# Introduction

### The Resistance
For our project, we implemented a multi-agent simulation based on The Resistance. The Resistance is a multiplayer deductive reasoning role-playing game designed by Don Eskridge in 2010. The players are divided into two "factions": the Resistance (the "good guys") and the government spies (the "bad guys"). Within the game, players are sent on 5 missions that can either pass or fail. Both teams work to score at least three points. A minimum of five players is required for the game.

At the start of a game with five players, two players are chosen at random to be spies and the other three players are the resistance. The spies know each other's identity while the Resistance remains in the dark. Each round consists of several elements:
1. A Mission Leader is chosen. The first Mission Leader is chosen randomly - after that, the player to the left of the previous Mission Leader becomes the new Mission Leader.
2. The Mission Leader selects a team to send on the mission. The number of people on the team differs per mission.
3. All players vote on the team composition. If at least half of the players agree with the team composition, the team is sent on a mission. If more than half of the players disagree with the team composition, a new player becomes the Mission Leader and step two and three are repeated. If there are 5 failed attempts to create a mission team, the government spies automatically get one point, and the next round starts.
4. On the mission, each player on the mission team places a card face-down. This card is either a "pass"-card or a "fail"-card. Resistance-players must always play a "pass"-card, whereas spies can choose to play either a "pass"- or "fail"-card. The Resistance wins the mission if all the cards played are "pass"-cards, whereas the spies win if one or more "fail"-cards are played. The faction who wins the mission gets one point.

The winning condition is that one of the teams must win three points (a 'best out of five'-principle). Resistance players have to try to deduce who the spies are, to ensure that the spies cannot sabotage the missions. The spies attempt to keep their identity a secret from the Resistance.

### Our project
With the use of higher-order knowledge, used for reasoning, and public announcements, used to announcement the results of a round, we impletemnted a multi-agent simulation based on the Resistance. We will describe our simplifications of the game and modifications for the purpose of experimentation under "Theory".

# Theory
## Kripke model
We want to model The Resistance with the help of Dynamic Epistemic Logic. With five players, we have a set of five agents A = {1, 2, 3, 4, 5}. Out of these five agents, two agents are randomly appointed as spies. We denote this as _s<sub>i</sub>_, meaning that agent _i_ is a spy.
The worlds of our Kripke model consist of every possible combination of spy pairs, which, for five agents, results in 10 initial worlds. The initial model is shown below. We have omitted the reflexive relations for clarity. As can be seen from this model, the agents are only aware of their own identity.

![Image](/images/1main-model.jpg)

As the game proceeds, the model is simplified as the agents learn from the public announcements given at the end of each mission. This public announcement is based on whether a fail-card was played during the mission. We will now give an example of how the game works in terms of updating the Kripke model.

### Example run-through 
We model a game with five agents (A = {1, 2, 3, 4, 5}), where agent 1 and 2 are spies. The rest of the agents are Resistance members. This means that the real world is _s<sub>1</sub>,_ _s<sub>2</sub>_.
As per the rules, the spies are aware of who the other spies are; thus, agent 1 and 2 are aware of each other's identities. It is also common knowledge that the spies know who the spies are. Resistance members are still only aware of their own identity. This is illustrated in the model below. Note that the modeel at this stage would be the same regardless of the real world.

![Image](/images/2spies-known.jpg)

The Mission Leader is chosen at random. In this case, agent 4 is the Mission Leader and must propose a mission team.
For mission 1, two players make up the mission team. Since agent 4 has not learnt anything about the identities of the other agents, they choose two players at random for the first mission: agent 1 and agent 5.
Now the other agents must use their knowledge to either vote for or against this mission team. Since none of the Resistance members know of the identity of agent 1 (who is a spy), they will vote _for_ the mission team. This is already a majority for the mission, so the spies' votes are irrelevant. However, in this case they would also vote _for_ the mission, as there is a spy on the mission. This means that the mission team is now accepted, and agent 1 and agent 5 go on the mission.

For this run-through, we simplify the playing of the cards; a spy will always play a fail-card. As such, agent 1 will now play a fail-card (as they are a spy), and agent 5 plays a pass-card (as they are part of the Resistance). Given that one fail-card was played, the mission has failed. This means that the spies now receive one point.
The fact that a fail-card was played can be used to update the knowledge of the agent in the form of a public announcement. The agents know that either agent 1 or agent 5 is a spy. The public announcement made is <img src="https://render.githubusercontent.com/render/math?math=[s1 \lor s5]">. The resulting model is shown below:

![Image](/images/3announcement.jpg)

As can been seen from the updated model, worlds in which neither agent 1 nor agent 5 are spies are removed from the model. From this mission, agent 5 knows that agent 1 played the fail card, since agent 1 was the only other agent on the mission. Therefore, agent 5 knows that agent 1 is a spy. Also, both spies, agent 1 and agent 2, now know that agent 5 knows that agent 1 is a spy.

The next mission leader is chosen as the next player: agent 5. Mission 2 requires a three player team. Since agent 5 knows that agent 1 is a spy, _K<sub>5</sub>s<sub>1</sub>_, they will not include agent 1 in the mission team. Agent 5 does not know anything about the identity of the other players, so they choose three players from the remaining randomly. The proposed team is agent 3, agent 4 and agent 5.
Since agents 1 and 2 know that agents 3, 4 and 5 are all part of the Resistance, they will both vote against this mission team (as the Resistance will figure out who the spies are, as only pass-cards will be played).
However, agents 3, 4, and 5 will vote for this mission team as they do not know that any of the other agents in the team are spies. This leads to a majority for the mission team, so the mission goes ahead.

On mission 2, agents 3, 4, and 5 all play a pass card as they are all part of the Resistance. This means that the mission passes and the Resistance receives one point. The success of the mission leads to the conclusion that agent 3, agent 4 and agent 5 are not spies. Therefore, the public announcement made is 
<img src="https://render.githubusercontent.com/render/math?math=[\neg s_3 \wedge \neg s_4 \wedge \neg s_5]">

This public announcement drastically reduces the model. The worlds with _s<sub>3</sub>_, _s<sub>4</sub>_ or _s<sub>5</sub>_ are removed. This model is illustrated below. 

![Image](/images/5reduction.png)

As can be seen, the only world that is left is the real state of the model, _s<sub>1</sub>, s<sub>2</sub>_. This means that all agents are aware of the real state of the world and the Resistance players have figured out the itendity of the spies. In this example, after only two missions the goal has been reached. All agents know the identity of all the other agents. 

The Resistance will win this game. They will vote against a mission team including spies and only propose mission teams exclusively consisting of resistance agents. Therefore, after 5 missions the score will be resistance: 4, spies: 1.
  
## Our program and implementation
  We use Python to build the simulation of The Resistance. We use Python's library [mesa](https://github.com/projectmesa/mesa) for the agent-based modelling and the [mlsolver](https://github.com/erohkohl/mlsolver) (modal logic solver) library for building, maintaining, and updating our Kripke model.

## Epistemic logic
  There are two different types of agent in this game: Resistance members and spies. The epistemic logic differs for these agents. We have given some introduction into the epistemic logic in the example run-through of the game; we will elaborate more here.
  
  At the beginning of the game, it is basically "no one knows anything". Once the spies know who the spies are, this knowledge updates, such that it becomes common knowledge that the spies know the identity of both spies. However, it is impossible for the resistance agents to deduce who the spies are at this moment. We will look at the different rounds of the game (as described in the Introduction), and see how epistemic logic can be used.
  
  - **Choosing the Mission Leader**: No epistemic logic is used in this case. The first Mission Leader is chosen at random, and after that, the Mission Leader is rotated.
  - **Team selection**: In the selection of the teams, it matters whether the Mission Leader is a Resistance member or a spy.
    - **Resistance**: a resistance agent does not want to send a spy on a mission, as this can cause the mission to fail. Using the Kripke model, we determine whether the agent knows the identity of one or both of the spies. If they do know a spy's identity, the agent will avoid choosing this agent for the team. To form the team, the agent will choose themselves, as they know their own identity, and any agent they are not certain is a spy.
    - **Spy**: a spy aims to sabotage the mission. This means a spy wants to choose a mission team that will not be voted down by the rest of the agents. Therefore, the spy must determine whether the identity of a spy has been revealed to any of the agents, whether the spy knows that another agent knows a spy. This is done using the Kripke model. If one spy's identity is known by an agent, the mission leader chooses the other spy for the mission and randomly fills the rest of the mission with resistance agents. If both identities are known, the team leader randomly chooses a spy for the mission, as they do not want to end up with a mission consisting of only resistance agents.
  - **Vote on the team make-up**: Each agent casts a vote. Again, it is important whether an agent is a Resistance member or a spy.
    - **Resistance**: 
    - **Spy**: 
  - **Playing the cards**: The card played by an agent is dependent on whether the agent is a spy or Resistance member.
    - **Resistance**: a Resistance agent will always play a pass-card
    - **Spy**: the card played by a spy depends on whether the spies are using epistemic logic to make their decision.
      - Without epistemic logic: the spies will always play a fail-card.
      - With epistemic logic: the spies will deterine whether playing a fail-card will result in the identity of both spies being revealed. If this is the case, they will choose to play a pass-card to prevent the identities from being revealed. Otherwise, they will play a fail-card.
  - **Updating knowledge**: Firstly, a public announcement is made to all the agents about the result of the mission. This is used to update the Kripke model to reflect the knowledge gained from the announcement. Secondly, the resistance agents can use the result of the mission and the voting round to reason about the identity of the spies. 
    - **Public announcement**: The public announcement removes worlds that are no longer possible given the results of the mission. The public announcement made depends on the cards played by the agents on the mission.
      - Only fail cards: this means that only spies were on the mission. Therefore, the announcement would be that the agents on the mission are spies. 
      - One fail card and pass cards: this means that one spy was on the mission. The announcement would be that one of the agents one the mission is a spy. 
      - Two fail cards and one or more pass cards: this means that two spies were on the mission with one or more resistance members. The annoucement here would be that two of the agents on the mission are spies. 
      - Only pass cards: the annoucenement for this situation depends on whether the spies are using epistemic logic (as explained above) to choose the card they play. With reasoning spies, nothing can be determined on a passed mission as the spies can play pass-cards to avoid detection. With non-reasoning spies, the annoucement would be that all agents on the mission are not spies.
    - **Resistance reasoning**: The resistance agents can reflect on who voted for a mission that failed. For a mission to be sabotaged, a spy must be on the mission. This means that the spies would be in favour of that mission team and would have voted for it. Therefore, a resistance agent can use that information to weed out the identity of the spies. This involves updating the Kripke model with an announcement based on the knowledge of the agent.

## Experiments
  We run several experiments, where we vary different settings. The first setting is one that is varied for both of the other two experiments, meaning we have 10 experiments in total: (3 + 2) * 2. As the quantifiable evaluation metric, we use the percentage of games that are won by the Resistance. The settings we vary are the following: 
  1. **Spies reason about a fail-card using second-order knowledge vs. Spies always play a fail-card**: We find that the most important part of this project is using knowledge. As such, we have decided that for each of the other experiments we do, we want to see how knowledge would influence the outcome of the game. In a simplified version of the game, spies always play a fail-card. This means that whenever there is a spy on the mission, the mission will automatically fail and the spies gain a point. However, this also gives away information on the identity of the spies. In the version where spies reason about whether or not to play a fail-card, spies try to find out whether playing a fail-card would cause a Resistance agent to be sure of the identity of the spy. If this is the case, a spy does *not* play a fail-card; else, the spy does.
  2. **Every mission has teams of 2 vs. Every mission has teams of 3 vs. The number of team members is as described in the rules**: We vary the number of people on a mission such that we have three settings: [2, 2, 2, 2, 2] (2 people on each mission), [3, 3, 3, 3, 3] (three people on each mission), and [2, 3, 2, 3, 3] (as is described in the rules).
  3. **5 players vs. 6 players**: In both settings, there are only two spies - the rules state that the number of spies is a third of the total number of players, rounded up. We are interested in seeing how the extra Resistance-member influences the knowledge and overall gameplay.

# Results

# Conclusion

# Running instructions


<!--- Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for
In the case of a Resistance agent, you do not want to send a spy on a mission, as this will likely cause your mission to fail (depending on whether or not the spy plays a fail-card). The Resistance agent will thus put together a team in which no spies are present.

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/Ritten11/LAMAS2021/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
-->
