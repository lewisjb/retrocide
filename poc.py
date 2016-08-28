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
            agent.age += 1

            if agent.pregnant > 0:
                agent.pregnant += 1
                if agent.pregnant > 9 * 30:
                    # Create baby
                    self.agents.append(agent.create_offspring(agent.partner))

                    # Reset pregnancy
                    agent.partner.pregnant = 0
                    agent.partner.partner = None
                    agent.pregnant = 0
                    agent.partner = None

            for i, a in enumerate(self.agents):
                #rf = agent.get_relationship_factor(a)
                # XXX Fix RF Speed
                rf = 0.1
                if random.random() - 0.1 < rf:
                    # They met (or met again)
                    agent.encounter(a, rf, self)

            last_encounter = 0
            for c in agent.connections:
                if c.last_encounter > last_encounter:
                    last_encounter = c.last_encounter

                inactivity = self.iteration - c.last_encounter
                if inactivity > 100:
                    c.emotions.decrease_all()

                if not c.emotions.any_emotion():
                    agent.sever(c)

            # Handle emotions
            if agent.emotions.sadness > 10:
                # Depression =/= sadness, but this is easier to code
                agent.kill(agent) # Suicide

            # Old age
            if agent.age > random.randrange(50 * 365, 100 * 365):
                agent.die()


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

    def decrease_all(self):
        if self.joy > 0:
            self.joy -= 1
        if self.trust > 0:
            self.trust -= 1
        if self.fear > 0:
            self.fear -= 1
        if self.surprise > 0:
            self.surprise -= 1
        if self.sadness > 0:
            self.sadness -= 1
        if self.disgust > 0:
            self.disgust -= 1
        if self.anger > 0:
            self.anger -= 1
        if self.anticipation > 0:
            self.anticipation -= 1

    def any_emotion(self):
        if (self.joy or self.trust or self.fear or self.surprise or
            self.sadness or self.disgust or self.anger or self.anticipation):
                return True
        return False

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

        self.pregnant = 0 # How many days pregnant

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
        offspring_name = random_names[bool(first)][random.randrange(50)]
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

    def encounter(self, agent, rf, society):
        # Take into account: Sex, Personality, relationship factor,
        # current emotions, age
        c = self.get_connection(agent)
        if c:
            c.last_encounter = society.iteration
        else:
            self.add_connection(agent)
            c = self.get_connection(agent)
        co_c = agent.get_connection(self)

        age_diff = agent.age - self.age
        diff_sex = self.sex == agent.sex

        s_emotions = self.emotions.get_abs_emotion()
        a_emotions = agent.emotions.get_abs_emotion()

        # Personality compatibility (greedy solution)
        pc = sum([self.personality[i] == agent.personality[i]
                    for i in xrange(4)])

        # Handle encounter

        # Murder (they can both die)
        if self.emotions.anger > 10:
            self.kill(agent)
        if agent.emotions.anger > 10:
            agent.kill(self)

        # Procreating
        if diff_sex:
            if self.age > 16 * 365 and agent.age > 16 * 365:
                if self.can_procreate() and agent.can_procreate():
                    if pc > 2:
                        pf = (self.emotions.joy + self.emotions.trust +
                            agent.emotions.joy + agent.emotions.trust)
                        if pf > 30:
                            # Should probs do more checking of stuff
                            self.pregnant = 1
                            self.partner = agent

                            agent.pregnant = 1
                            agent.partner = self
                        


        # Increase positive emotions
        c.emotions.joy += 1
        c.emotions.trust += 1
        co_c.emotions.joy += 1
        co_c.emotions.trust += 1

        self.emotions.joy += 1
        self.emotions.trust += 1

        agent.emotions.joy += 1
        agent.emotions.trust += 1

    def kill(self, agent):
        # Kill the person

        # Emotions
        self.anger /= 2
        self.fear += 10

        agent.die()

    def die(self):
        # Effect connections, then remove them
        for c in self.connections:
            c.agent.emotions.sadness += 1
            
            rm = c.agent.get_connection(self)
            del c.agent.connections[c.agent.connections.index(rm)]

        self.connections = None

    def sever(self, connection):
        # Sever connection
        agent = connection.agent
        index = self.connections.index(connection)
        del self.connections[index]

        c = agent.get_connection(self)
        index2 = agent.connections.index(c)
        del agent.connections[index2]

    def can_procreate(self):
        return self.pregnant == 0


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

        agent.age = random.randrange(0, 20 * 365)

        return agent






"""
DNA Spec:
    Sex (1 = Male, 0 = Female)
    Myer-Briggs

"""

if __name__ == '__main__':
    x = Society.generate_random(15)
    print x
    for _ in xrange(365 * 100):
        x.next_iteration()

    print x
