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
    "Jenell", "Fredda", "Teressa", "Clarisa", "Ainsley", "Marisa", "Rachel",
    "Astrid", "Hayley", "Felicia" ],
    ["Matthew", "Evan", "Simon", "Tom", "Logan", "Aidan", "Joseph", "Mitch",
    "Jack", "Dragan", "Kaamraan", "Cameron", "Dylan", "Joel", "Justin", "Matt",
    "Daniel", "James", "Max", "Alex", "Jim", "Joseph", "Dave", "Nicolaus",
    "Mark", "Tom", "Nicholas", "Max", "Lachlan", "Lewis", "Jake", "Chris",
    "Neil", "Elliot", "Cyrill", "Tylor", "Sameer", "Dave", "Nick", "Randall",
    "David", "Adam", "Ibraheem", "William", "Xander", "Ross", "Damian",
    "Harry", "Scott", "Blaid", "Ken", "Christopher", "Anthony"]
]

def get_random_name(sex):
    return random_names[sex][random.randrange(len(random_names[sex]))]

random_weapons = [
    "Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Spanner"
]

random_locations = [
    "Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall",
    "Kitchen", "Library", "Lounge", "Study"
]

class Society:
    def __init__(self, agents):
        self.agents = agents
        self.iteration = 0

    def __str__(self):
        if len(self.agents) == 0:
            return "They're all dead. Everybody's dead Dave."

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
        dead = []
        for agent in self.agents:
            agent.age += 1
            if agent.dead:
                dead.append(agent)
                continue

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

            # Old age
            if agent.age > random.randrange(30 * 365, 80 * 365):
                print "%s died of old age" % agent.name
                agent.die()

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
                print "%s killed themselves." % agent.name
                agent.kill(agent) # Suicide

            # General loss of emotions
            if random.random() < 0.01:
                agent.emotions.decrease_all()

        for d in dead:
            del self.agents[self.agents.index(d)]


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


        self.dead = False

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

        male = False
        personality = []
        if random.random() < 0.5:
            # Gets the first half of this agent and second of partner
            # XXX Don't hardcode
            male = self.sex
            personality = [self.personality[0], self.personality[1],
                            partner.personality[2], partner.personality[3]]
        else:
            male = self.sex
            personality = [partner.personality[0], partner.personality[1],
                            self.personality[2], self.personality[3]]

        personality_int = 0
        for i in xrange(4):
            if personality[i]:
                personality_int |= (1 << i)

        offspring_dna = "%c%c" % (male, personality_int)

        offspring_name = get_random_name(male)
        offspring = Agent(offspring_dna, offspring_name)

        # Make connections with parents
        offspring.add_connection(self)
        offspring.add_connection(partner)

        print "%s was born" % offspring.name

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
        diff_sex = self.sex != agent.sex

        s_emotions = self.emotions.get_abs_emotion()
        a_emotions = agent.emotions.get_abs_emotion()

        # Personality compatibility (greedy solution)
        pc = sum([self.personality[i] == agent.personality[i]
                    for i in xrange(4)])

        # Handle encounter

        # Murder (they can both die)
        if self.emotions.anger > 20 and self.emotions.fear == 0:
            self.kill(agent)
        if agent.emotions.anger > 20 and self.emotions.fear == 0:
            agent.kill(self)

        # Procreating
        if diff_sex:
            if self.age > 16 * 365 and agent.age > 16 * 365:
                if self.can_procreate() and agent.can_procreate():
                    if pc > 2:
                        pf = (self.emotions.joy + self.emotions.trust +
                            agent.emotions.joy + agent.emotions.trust)
                        pf += (c.emotions.joy + c.emotions.trust +
                            co_c.emotions.joy + co_c.emotions.trust)
                        if pf > 100:
                            # Should probs do more checking of stuff
                            self.pregnant = 1
                            self.partner = agent

                            agent.pregnant = 1
                            agent.partner = self
                            
                            # Regret
                            self.emotions.joy = 0
                            self.emotions.trust = 0

                            agent.emotions.joy = 0
                            agent.emotions.trust = 0

                            c.emotions.joy = 0
                            c.emotions.trust = 0

                            co_c.emotions.joy = 0
                            co_c.emotions.trust = 0
                        


        # Increase positive emotions
        if pc > 2:
            if random.random() < 0.02:
                c.emotions.joy += 1
                c.emotions.trust += 1
                co_c.emotions.joy += 1
                co_c.emotions.trust += 1

                self.emotions.joy += 1
                self.emotions.trust += 1

                agent.emotions.joy += 1
                agent.emotions.trust += 1

        if pc < 1:
            if random.random() < 0.02:
                c.emotions.anger += 1
                c.emotions.disgust += 1
                co_c.emotions.anger += 1
                co_c.emotions.disgust += 1

                self.emotions.anger += 1
                self.emotions.disgust += 1

                agent.emotions.anger += 1
                agent.emotions.disgust += 1

    def kill(self, agent):
        # Kill the person

        # Emotions
        self.emotions.anger = 0
        self.emotions.fear += 30

        print "%s killed %s in the %s with a %s!" % (self.name, agent.name,
                random_locations[random.randrange(len(random_locations))],
                random_weapons[random.randrange(len(random_weapons))])
        agent.die()

    def die(self):
        if self.dead: return
        print "%s Died." % self.name
        # Effect connections, then remove them
        for c in self.connections:
            c.agent.emotions.sadness += 1
            
            rm = c.agent.get_connection(self)
            del c.agent.connections[c.agent.connections.index(rm)]
            
        self.dead = True

        self.connections = []

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
        name = get_random_name(sex)
        agent = Agent(dna, name)

        agent.age = random.randrange(0, 20 * 365)

        return agent






"""
DNA Spec:
    Sex (1 = Male, 0 = Female)
    Myer-Briggs

"""

if __name__ == '__main__':
    x = Society.generate_random(26)
    print x
    while True:
        inp = raw_input("Select who to kill: ")
        if inp == "":
            break
        try:
            n = int(inp)
        except ValueError:
            print "Invalid number"
            continue
        if n >= 0 and n < len(x.agents):
            x.agents[n].die()
        else:
            print "Invalid number"

    for i in xrange(365 * 10):
        x.next_iteration()
        #if i % 50 == 0:
        #    print len(x.agents)

    print x
