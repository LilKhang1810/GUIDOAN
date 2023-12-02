import numpy as np
import random
from copy import deepcopy
try:
    from itertools import izip
except ImportError:
    izip = zip
startTimePoint = 12
class Calendar:
  def __init__(self, list_task = []):
    super().__init__()
    self.state = list_task
    self.value = self.calValue()

  def add_task(self, task):
    self.state.append(task)
    self.value = self.calValue()

  def calValue(self):
    value = 0
    for i in range(len(self.state)):
      if self.state[i]['deadline'] >= (i + 1 + startTimePoint):
        value += self.state[i]['satisfy']
    return value

  def __lt__(self, other):
    return -self.value < -other.value
class CalendarProblem:
  def __init__(self, tasks_init):
      assert tasks_init and type(tasks_init) is list
      self.initial_state = tasks_init

  def generate_random_state(self):
    random_state = random.sample(self.initial_state, len(self.initial_state))
    return random_state

  def crossover(self, state_father, state_mother):
    state_fatherClone = deepcopy(state_father)
    state_motherClone = deepcopy(state_mother)

    halfMother = state_motherClone[len(state_motherClone)//2:]
    halfFather = list(filter(lambda task : task['name'] not in  [task['name'] for task in halfMother], state_fatherClone))

    return halfMother + halfFather

  def mutate(self, state):
    tempState = deepcopy(state)
    middle = len(tempState)//2
    positionRand1 = random.randrange(0, middle)
    positionRand2 = random.randrange(middle, len(state))
    tempState[positionRand1], tempState[positionRand2] = tempState[positionRand2], tempState[positionRand1]
    return tempState

  def value(self, schedule_state):
    stateValue = 0
    for i in range(len(schedule_state)):
      if schedule_state[i]['deadline'] >= (i + 1 + startTimePoint):
        stateValue += schedule_state[i]['satisfy']
    return stateValue
  def __init__(self, tasks_init):
      assert tasks_init and type(tasks_init) is list
      self.initial_state = tasks_init
      # super().__init__(initial_state = tasks_init)

  def generate_random_state(self):
    random_state = random.sample(self.initial_state, len(self.initial_state))
    return random_state

  def crossover(self, state_father, state_mother):
    state_fatherClone = deepcopy(state_father)
    state_motherClone = deepcopy(state_mother)

    halfMother = state_motherClone[len(state_motherClone)//2:]
    halfFather = list(filter(lambda task : task['name'] not in  [task['name'] for task in halfMother], state_fatherClone))

    return halfMother + halfFather

  def mutate(self, state):
    tempState = deepcopy(state)
    middle = len(tempState)//2
    positionRand1 = random.randrange(0, middle)
    positionRand2 = random.randrange(middle, len(state))
    tempState[positionRand1], tempState[positionRand2] = tempState[positionRand2], tempState[positionRand1]
    return tempState

  def value(self, schedule_state):
    stateValue = 0
    for i in range(len(schedule_state)):
      if schedule_state[i]['deadline'] >= (i + 1 + startTimePoint):
        stateValue += schedule_state[i]['satisfy']
    return stateValue

'''--------------------------------'''    
class GeneticSearch:
  def __init__(self, problem):
    assert type(problem) is CalendarProblem
    self.problem = problem

  def _random_parents(self, fringe):
    assert fringe
    ''' x is Calendar Object type '''
    weights = [x.value for x in fringe]
    total = float(sum(weights))
    probs = [w / total for w in weights]

    return np.random.choice(fringe, 2, p = probs, replace = False)

  def _genetic_expander(self, fringe_size, mutation_chance, keep_old_generation):
    def expander(fringe):
      new_generation = []
      for _ in range(fringe_size):
        randomParent = self._random_parents(fringe)
        father, mother = randomParent[0], randomParent[1]
        ''' Generate new child from 2 parents '''
        child_state = self.problem.crossover(father.state, mother.state)

        ''' Decide this child is mutated '''
        if random.random() < mutation_chance:
          child_state = self.problem.mutate(child_state)
        child = Calendar(child_state)
        new_generation.append(child)

      if keep_old_generation:
        fringe = fringe[:keep_old_generation]
      else:
        fringe.clear()

      for next_gen in new_generation:
        fringe.append(next_gen)

      fringe.sort()
      fringe = fringe[:fringe_size]
    return expander

  def execute(self, num_generation = 100, fringe_size = 100, mutation_chance = 0.1, keep_old_generation = 0):
    assert type(num_generation) is int and type(fringe_size) is int
    assert (0 <= mutation_chance <= 1) and type(keep_old_generation) is int and (0 <= keep_old_generation <= num_generation)

    fringe = []
    expander = self._genetic_expander(fringe_size, mutation_chance, keep_old_generation)
    count_generation = 0

    for _ in range(fringe_size):
      temp = self.problem.generate_random_state()
      fringe.append(Calendar(temp))

    count_generation += 1
    fringe.sort()
    best_invidual = fringe[0]

    while count_generation <= num_generation:
      expander(fringe)
      cur_best_invidual = fringe[0]
      best_invidual = max(best_invidual, cur_best_invidual)
      count_generation += 1
    self.result = best_invidual

# myProblem = CalendarProblem(tasks)

# genetic1 = GeneticSearch(myProblem)

# genetic1.execute(fringe_size = 200, num_generation = 100)

# print(genetic1.result.state)
# print(genetic1.result.value)