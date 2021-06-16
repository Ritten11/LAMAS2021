""" Three wise men puzzle

Module contains data model for three wise men puzzle as Kripke strukture and agents announcements as modal logic
formulas
"""

from ResistanceModel.mlsolver.kripke import KripkeStructure, World
from ResistanceModel.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star


class WiseMenWithHat:
    """
    Class models the Kripke structure of the "Three wise men example.
    """

    knowledge_base = []

    def __init__(self):
        worlds = [
            World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
            World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
            World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
            World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

            World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
            World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
            World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
            World('WWW', {'1:W': True, '2:W': True, '3:W': True}),
        ]

        relations = {
            '1': {('RWW', 'WWW'), ('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
            '2': {('RWR', 'RRR'), ('RWW', 'RRW'), ('WRR', 'WWR'), ('WWW', 'WRW')},
            '3': {('WWR', 'WWW'), ('RRR', 'RRW'), ('RWW', 'RWR'), ('WRW', 'WRR')}
        }

        relations.update(add_reflexive_edges(worlds, relations))
        relations.update(add_symmetric_edges(relations))

        self.ks = KripkeStructure(worlds, relations)

        # Wise man ONE does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('1', Atom('1:R'))), Not(Box_a('1', Not(Atom('1:R'))))))

        # This announcement implies that either second or third wise man wears a red hat.
        self.knowledge_base.append(Box_star(Or(Atom('2:R'), Atom('3:R'))))

        # Wise man TWO does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('2', Atom('2:R'))), Not(Box_a('2', Not(Atom('2:R'))))))

        # This announcement implies that third men has be the one, who wears a red hat
        self.knowledge_base.append(Box_a('3', Atom('3:R')))

class Resistance3Agents:
    """
    This class models the Kripke structure of the Resistance game with 3 agents.
    """
    knowledge_base = []

    def __init__(self):
        worlds = [
            World('1', {'1': True, '2': False, '3': False}),
            World('2', {'1': False, '2': True, '3': False}),
            World('3', {'1': False, '2': False, '3': True})
            ]
        relations = {
            '1': {('2', '3'), ('3', '2')},
            '2': {('1', '3'), ('3', '1')},
            '3': {('1', '2'), ('2', '1')}
        }
        relations.update(add_reflexive_edges(worlds, relations))
        self.ks = KripkeStructure(worlds, relations)

class Resistance5Agents: 
    """
    This class models the Kripke structure of the Resistance game with 5 agents.
    """
    knowledge_base = []

    def __init__(self, N = 5):
        worlds, kripke_worlds = self.create_worlds(N)

        relations = self.create_relations(worlds, N)

        relations.update(add_reflexive_edges(kripke_worlds, relations))
        relations.update(add_symmetric_edges(relations))  # does the update function replace the previous relations?
        self.ks = KripkeStructure(kripke_worlds, relations)

    def create_worlds(self, N):
        worlds = []
        for one in range(1, N+1):
            for two in range(1, N+1):
                if one != two and (str(two)+str(one)) not in worlds: 
                    world = str(one)+str(two)
                    worlds.append(world)
        world_truths = []
        for world in worlds:
            diction = {}
            #world_truths[world] = {p: True for p in world}
            for agent in range(1, N+1):
                if str(agent) not in world:
                    diction[str(agent)] = False
                else:
                    diction[str(agent)] = True
            world_truths.append(diction)

        kripke_worlds = []
        for i, world in enumerate(worlds):
            kripke_worlds.append(World(world, world_truths[i]))
        return worlds, kripke_worlds

    def create_relations(self, worlds, N):
        relations = {}
        for agent in range(1,N+1):
            relations[str(agent)] = []

        for agent in range(1, N+1):
            for world1 in worlds:
                for world2 in worlds:
                    if world1 != world2:
                        if str(agent) in world1 and str(agent) in world2 and (world2, world1) not in relations[str(agent)]:
                            relations[str(agent)].append((world1,world2))
                        if str(agent) not in world1 and str(agent) not in world2 and (world2, world1) not in relations[str(agent)]:
                            relations[str(agent)].append((world1,world2))
        for x in relations:
            relations[x] = set(relations[x])
        return relations


def add_symmetric_edges(relations):
    """Routine adds symmetric edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for r in agents_relations:
            x, y = r[1], r[0]
            result_agents.add((x, y))
        result[agent] = result_agents
    return result


def add_reflexive_edges(worlds, relations):
    """Routine adds reflexive edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for world in worlds:
            result_agents.add((world.name, world.name))
        result[agent] = result_agents
    return result
