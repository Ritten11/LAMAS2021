Authors: Ella Collins, Lonneke Langeveld, and Ritten Roothaert. 

# Introduction

### The Resistance
For our project, we implemented a multi-agent simulation based on The Resistance. The Resistance is a multiplayer deductive reasoning role-playing game designed by Don Eskridge in 2010. The players are divided into two "factions": the Resistance (the "good guys") and the government spies (the "bad guys"). Within the game, players are sent on 5 missions that can either pass or fail. Both teams work to score at least three points. A minimum of five players is required for the game.

At the start of a game with five players, two players are chosen at random to be spies and the other three players are the resistance. The spies know each other's identity while the Resistance remains in the dark. Each round consists of several elements:
1. A Mission Leader is chosen. The first Mission Leader is chosen - after that, the Mission Leader to the left of the previous Mission Leader becomes the new Mission Leader.
2. The Mission Leader selects a team to send on the mission. The number of people on the team differs per mission.
3. All players vote on the team make-up. If the players agree (at least half the players should agree with the team), the team is sent on a mission. If the players disagree, a new player becomes the Mission Leader (the one to the left of the previous one), and step two and three are repeated. If there are 5 failed attempts to create a mission team, the government spies automatically get one point, and the next round starts.
4. On the mission, each person on the mission team places a card face-down. This card is either a "pass"-card or a "fail"-card. Resistance-players must always play a "pass"-card, whereas spies can choose to play either a "pass"- or "fail"-card. The Resistance wins the mission if all the cards played are "pass"-cards, whereas the spies win if one or more "fail"-cards are played. The faction who wins the game gets one point.

The winning condition is that one of the teams must win three points (a 'best out of five'-principle). Resistance players have to try to deduce who the spies are, to ensure that the spies cannot sabotage the missions. The spies attempt to keep their identity a secret from the Resistance.

### Our project
As we have mentioned, we implemented a multi-agent simulation based on the Resistance. We use higher-order knowledge and public announcements. We will describe all modifications we make for the sake of experiments under "Theory".

# Model 
We are going to model the Resistance game with the help of Dynamic Epistemic Logic. With five players we have a set of five agents A = {1,2,3,4,5}. Out of these agents, two agents are spies which we can denote by _s<sub>i/sub>_ meaning that agent _i_ is a spy. The worlds of the Kripke model will consist of every combination of spy pairs, resulting in 10 initial worlds. The initial model is shown below, where the reflexive relations are omitted for clarity. As can be seen from this model, the agents are only aware of their own identity.

![Image](/images/1main-model.jpg)

As the game proceeds, the model is simplified as the agents learn from the public announcements given at the end of each mission.

### Example run-through 
For a game with five agents A = {1,2,3,4,5}, where agent 1 and 2 are spies, and the rest are part of the resistance, the real world is _s<sub>1</sub>,s<sub>2</sub>_. Agent 1 and 2 are aware of each other's identities. Therefore, they are already aware of the real state of the model, whereas the resistance agents are only aware of their own identity. This is illustrated in the model below.

![Image](/images/2spies-known.jpg)

The mission leader is chosen at random: agent 4 is the mission leader and must propose a mission team. For mission 1, two players make up the mission team. Since agent 4 has not learnt anything about the identities of the other agents, they choose two players at random for the first mission: agent 1 and agent 5. Now the other agents must use their knowledge to either vote for or against this mission team. Since none of the resistance players know of the identity of agent 1, they will vote for the mission team. Also, the spies want a spy to be on a mission, so they will vote for the mission team. Therefore, the mission team is accepted and agent 1 and agent 5 go on the mission. 

On mission 1, agent 1 plays a fail card since they are a spy, and agent 5 plays a pass card since they are part of the resistance. As one fail card was played, the mission failed. The spies receive one point. This leads to the conclusion that either agent 1 is a spy or agent 5 is a spy. Therefore, the public announcement made is <img src="https://render.githubusercontent.com/render/math?math=[s1 \lor s5]">. This leads to the following model:

![Image](/images/3announcement.jpg)

As can been seen from the updated model, worlds in which neither agent 1 nor agent 5 is a spy are removed from the model. From this mission agent 5 knows that agent 1 played the fail card, since agent 1 was the only other agent on the mission. Therefore, agent 5 knows that agent 1 is a spy. Also, both spies, agent 1 and agent 2, now know that agent 5 knows that agent 1 is a spy. 

The next mission leader is chosen as the next player: agent 5. Mission 2 requires a three player team. Since agent 5 knows that agent 1 is a spy, _K<sub>5</sub>s<sub>1</sub>_, they will not include agent 5 in the mission team. Agent 5 does not know anything about the identity of the other players, so they choose three players from the remaining randomly. The proposed team is agent 3, agent 4 and agent 5. Since agents 1 and 2 know that agents 3, 4 and 5 are all part of the resistance, they will both vote against this mission team. However, agents 3, 4 and 5 will vote for this mission as they do not know that any of the other agents in the team are spies. This leads to a majority for the mission team, so the mission goes ahead. 

On mission 2, agents 3, 4 and 5 all play a pass card as they are all part of the resistance. This means that the mission passes and the resistance receives one point. This leads to the conclusion that agent 3, agent 4 and agent 5 are not spies. Therefore, the public annoucement made is 
<img src="https://render.githubusercontent.com/render/math?math=[\neg s_3 \wedge \neg s_4 \wedge \neg s_5]">

This public annoucement drastically reduces the model. The worlds with _s<sub>3</sub>_, _s<sub>4</sub>_ or _s<sub>5</sub>_ are removed. This model is illustrated below. 

![Image](/images/5reduction.png)

As can be seen, the only world that is left is the real state of the model, _s<sub>1</sub>,s<sub>2</sub>_. This means that all agents are aware of the real state of the world and the resistance players have figured out the itendity of the spies. In this example, after only two missions the goal has been reached. All agents know the identity of all the other agents.

## Theory

## Results

## Conclusion

# Running instructions


<!--- Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

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
