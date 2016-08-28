# Proof of concept
import random

# Generated from http://listofrandomnames.com

random_names = [
    [ "Isidra", "Cordie", "Edda", "Magali", "Klara", "Tina", "Irena", "Kandice",
    "Jade", "Lena", "Mitzie", "Gwyneth", "Fae", "Ofelia", "Meghann", "Jasmine",
    "Hollie", "Mendy", "Debi", "Lilliana", "Jenae", "Bunny", "Carmel",
    "Blanca", "Emilie", "Trang", "Reta", "Roxanne", "Love", "Kary", "Beatris",
    "Estrella", "Shenika", "Gabrielle", "Fernanda", "Herta", "Paz", "Ashlee",
    "Essie", "Candance", "Ryann", "Kizzy", "Eliz", "Macy", "Mae", "Mathilde",
    "Jenell", "Fredda", "Teressa", "Clarisa" ],
    [ "Rico", "Elias", "Doug", "Bret", "Cedric", "Ivory", "Lacy",
    "Granville", "Dee", "Eli", "Tom", "Ezequiel", "Harry", "Vernon", "Hyman",
    "Roderick", "Beau", "Dale", "Abraham", "Stevie", "Clair", "Clay", "Marion",
    "Ted", "Clayton", "Carmelo", "Frederick", "Stephen", "Nathan", "Rosario",
    "Lowell", "Genaro", "Luigi", "Tad", "Joan", "Ralph", "Blake", "Kevin",
    "Clark", "Clifford", "Efren", "Hong", "Anthony", "Vince", "Manual",
    "Moses", "Emanuel", "Joseph", "Brendon", "Jules" ]
]

class Society:
    def __init__(self, agents):
        self.agents = agents
        self.iteration = 0

    def __str__(self):
        ret = ""
        mlen = max((len(a.name) for a in self.agents))

        ret += "ID"
        ret += " " * (10 - len("ID"))
        ret += "Name"
        ret += " " * (mlen + 4 - len("Name"))
        ret += "Age"
        ret += " " * (10 - len("Age"))
        ret += "Sex"
        ret += " " * (11 - len("Gender"))
        ret += "Personality\n"

        for i, a in enumerate(self.agents):
            ret += str(i)
            ret += " " * (10 - len(str(i)))
            ret += a.name
            ret += " " * (mlen + 4 - len(a.name))
            ret += str(a.age)
            ret += " " * (10 - len(str(a.age)))
            gender = "Male" if a.sex else "Female"
            ret += gender
            ret += " " * (11 - len(gender))

            # Personality
            ret += "I" if a.personality[0] else "E"
            ret += "N" if a.personality[1] else "S"
            ret += "F" if a.personality[2] else "T"
            ret += "P" if a.personality[3] else "J"

            ret += "\n"

        return ret

    def next_iteration(self):
        self.iteration += 1
        random.seed(self.iteration + len(self.agents))
        for agent in self.agents:
            for i, a in enumerate(self.agents):
                rf = agent.get_relationship_factor(a)
                if random.random() - 0.1 < rf:
                    # They met (or met again)
                    agent.encounter(a, rf, self.iteration)
        #XXX Check age of connections

    @classmethod
    def generate_random(cls, seed=None):
        if seed == None: seed == os.urandom()
        random.seed(seed)
        num_agents = random.randrange(10, 21)

        agents = []
        for _ in xrange(num_agents):
            agents.append(Agent.generate_random(seed))

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

class Emotion:
    def __init__(self):
        self.joy = 0
        self.trust = 0
        self.fear = 0
        self.surprise = 0
        self.sadness = 0
        self.disgust = 0
        self.anger = 0
        self.anticipation = 0

    def get_abs_emotion(self):
        return (self.joy + self.trust + self.surprise + self.anticipation
                 - self.fear - self.sadness - self.disgust - self.anger)

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

        self.emotions = Emotion()

        self.last_encounter = 0 # Last iteration where they encountered

    def get_connection_factor(self):
        return 0.5 + self.emotions.get_abs_emotion()

class Agent:
    def __init__(self, dna, name):
        self.connections = [] # Connections with other agents
        self.age = 0 # Age in iterations (days)
        self.emotions = Emotion()
        self.name = name

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

    #XXX Make it get half of the parents personalities
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
        offspring_name = random_names[sex][random.randrange(50)]
        offspring = Agent(offspring_dna, offspring_name)

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

    def encounter(self, agent, rf, iteration):
        # Take into account: Sex, Personality, relationship factor,
        # current emotions, age
        c = self.get_connection(agent)
        if c:
            c.last_encounter = iteration
        age_diff = agent.age - self.age
        diff_sex = self.sex == agent.sex

        s_emotions = self.emotions.get_abs_emotion()
        a_emotions = agent.emotions.get_abs_emotion()

        # Personality compatibility (greedy solution)
        pc = sum([self.personality[i] == agent.personality[i]
                    for i in xrange(4)])

        # Handle encounter

    @classmethod
    def generate_random(cls, seed):
        sex = random.random() < 0.5
        personality = [random.random() < 0.5 for _ in xrange(4)]
        personality_int = 0
        for i in xrange(4):
            if personality[i]:
                personality_int |= (1 << i)

        dna = "%c%c" % (sex, personality_int) # XXX Fix dis
        name = random_names[sex][random.randrange(50)]
        agent = Agent(dna, name)

        agent.age = random.randrange(0, 1000)

        return agent






# How do people meet new people?
# How do connections change?

"""
DNA Spec:
    Sex (1 = Male, 0 = Female)
    Myer-Briggs


"""
