# Retrocide

  Made for the UQCS 2016 Hackathon

## Premise

  Retrocide is a game where the goal is to make a species go extinct.
  But instead of using conventional methods of killing all the organisms
  you kill certain ancestors which result in the extinction in 100 years.

  No RNG is used except for pseudo-random generation of the initial conditions.
  This means that if you use the same seed and kill the same organisms, the
  same result will occur everytime.
  Another use of pseudo-random number generation is for genetic algorithms.
  This is because they are meant to be 'random', however the seed will be
  the iteration of the simulation which allows for it to be 'random', but
  will always be the same with the same conditions.

## More info

  No hard-coding of events. This means no 'if all males die then species is
  extinct'.

  Chaos theory - Same algorithm applied over the network over iterations.

  Evolutionary algorithms - Each organism has 'DNA', its offspring's 'DNA' is
  determined by the parents'.

  Highly customizable, this allows to easily apply the base concepts to 
  other things. For example somebody could dedicate a lot of time to make it
  realistic for humans.

  Agent-based social simulation. This means that the model is based off
  multiple intelligent agents (organisms).

  George Levinger's model of relationship is used for the connections between
  agents.

## Technical

  Each organism is an intelligent agent, which acts as a node in the social
  graph.

  An iteration is a day. Similar to cellular automata, changes over the
  iteration are based off the previous iteration, this means the graph is
  copied, checks are made on the copy, and updated on the live one.

  No leap years for simplicity, so 365 days in a year for 100 years means
  36,500 iterations over the simulation.

## Difficulties

  1. Organisms meeting new organisms
