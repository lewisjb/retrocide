# Proof of concept
import random

class Society:
    def __init__(self, agents):
        self.agents = agents
        self.iteration = 0

    def next_iteration(self):
        pass

class AgentConnection:
    """
        Connection between two agents.
        Based off George Levinger's model of relationships
    """

    STAGE_ACQUAINTANCE  = 0
    STAGE_BUILDUP       = 1
    STAGE_CONTINUATION  = 2
    STAGE_DETERIORATION = 3
    STAGE_ENDING        = 4

    def __init__(self, agent):
        self.agent = agent
        self.stage = 0

        # The 8 basic emotions
        self.joy = 0
        self.trust = 0
        self.fear = 0
        self.surprise = 0
        self.sadness = 0
        self.disgust = 0
        self.anger = 0
        self.anticipation = 0

    def get_connection_factor(self):
        return (0.5 + self.joy + self.trust + self.surprise + self.anticipation
                 - self.fear - self.sadness - self.disgust - self.anger)

class Agent:
    def __init__(self, dna):
        self.connections = [] # Connections with other agents
        self.age = 0 # Age in iterations (days)

        self.dna = dna
        self.unpack_dna()

    def unpack_dna(self):
        sex = ord(self.dna[0])
        personality = ord(self.dna[1])

        self.sex = bool(sex)
        self.personality = [bool(personality & (1 << i)) for i in xrange(4)]

    def add_connection(self, agent):
        self.connections.append(AgentConnection(agent))
        agent.connections.append(AgentConnection(self))

    def get_connection(self, agent):
        for c in self.connections:
            if c.agent == agent:
                return c

    def create_offspring(self, partner):
        random.seed(self.age + partner.age)
        first = None
        second = None
        if random.random() < 0.5:
            # Gets the first half of this agent and second of partner
            # XXX Don't hardcode
            first = self.dna[0]
            second = partner.dna[1]
        else:
            first = partner.dna[0]
            second = partner.dna[1]

        offspring_dna = "%c%c" % (first, second) # XXX Need new way for more dna
        offspring = Agent(offspring_dna)

        # Make connections with parents
        offspring.add_connection(self)
        offspring.add_connection(partner)

        return offspring

    def get_relationship_factor(self, agent, visited=None):
        if visited == None:
            visited = {}

        if self == agent:
            return 1.0

        factor = 0.0
        for c in self.connections:
            if visited.get(c.agent, False):
                continue
            tmp = visited.copy()
            tmp[self] = True
            factor += (c.get_connection_factor() *
                            c.agent.get_relationship_factor(agent, tmp))

        return factor


def generate_random_agent(seed):
    sex = random.random() < 0.5
    personality = [random.random() < 0.5 for _ in xrange(4)]
    personality_int = 0
    for i in xrange(4):
        if personality[i]:
            personality_int |= (1 << i)

    dna = "%c%c" % (sex, personality_int) # XXX Fix dis
    agent = Agent(dna)

    return agent


def generate_random_society(seed=None):
    if seed == None: seed == os.urandom()
    random.seed(seed)
    num_agents = random.randrange(10, 21)

    agents = []
    for _ in xrange(num_agents):
        agents.append(generate_random_agent(seed))

    num_connections = random.randrange(num_agents - 5, num_agents + 6)

    while num_connections > 0:
        a1 = agents[random.randrange(0, num_agents)]
        a2 = agents[random.randrange(0, num_agents)]

        if a1 != a2:
            c1 = a1.get_connection(a2)
            if c1:
                c2 = a2.get_connection(a1)
                c1.stage += 1
                c2.stage += 1
            else:
                a1.add_connection(a2)

        num_connections -= 1

    society = Society(agents)

    return society


# How do people meet new people?
# How do connections change?

"""
DNA Spec:
    Sex (1 = Male, 0 = Female)
    Myer-Briggs


"""
