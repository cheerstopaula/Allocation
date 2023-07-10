
import networkx as nx
import numpy as np

def value(i, S, cap, preferences, slots):
    m = len(preferences[0]) # number of classes
    utility = 0
    # Use a simple for loop to compute the value of a bundle of goods. Stop counting if the value of the goods exceeds the cap
    flag = [0]*m
    for j in range(m):
        gain = preferences[i][j]*S[j]*(1 - flag[slots[j]])
        if(gain == 1):
            flag[slots[j]] = 1
        utility += gain
        if(utility == cap[i]):
            break
    return utility


def SpireAlloc(cap, preferences, priority, availClasses):
  #find number of students n and number of classes m
  n = len(preferences)
  m = len(preferences[0])

  X = [[0]*m for i in range(n)] # Initialize the allocation as a binary matrix (n x m)
  playerInd = list(range(n)) # list of player indicies to iterate through
  playerInd = [x for _, x in sorted(zip(priority, playerInd))] #reorder players by priority (lowest goes first)

  # availClasses = [1 for i in range(m)] #list of available classes #Put enrollment cap on this

  for i in playerInd:
    #add each class in the preference if available
    curClasses = 0
    for j in range(len(preferences[i])):
      if (availClasses[j] > 0 and preferences[i][j] == 1):
        #print(j,preferences[i][j],availClasses[j])
        availClasses[j] -= 1 #remove 1 class from avail
        X[i][j] = 1
        curClasses += 1
      if curClasses >= cap[i]: #stop adding classes after cap
        break
    #print(f"Player {i} preferred:", preferences[i])
    #print(f"Player {i} classes  :", X[i])
    #print("-----")
  return X


def RoundRobin(cap, preferences, priority, availClasses, slots):
  n = len(preferences) #number of students
  m = len(preferences[0]) #number of classes

  X = [[0]*m for i in range(n)] # Initialize the allocation as a binary matrix (n x m)
  playerInd = list(range(n)) # list of player indicies to iterate through
  playerInd = [x for _, x in sorted(zip(priority, playerInd))] #reorder players by priority (lowest goes first)

  # availClasses = [spots for i in range(m)] #list of available classes
  counter = 0 # Keeps track of the number of stiudents who have the max no. of classes
  while availClasses.count(0) < len(availClasses) and counter < n: #loop as long as there are classes left and not all students hit the cap
    #go through a full cycle
    incUtil = False # checks if any utility is increased
    for i in playerInd:
      #add each class in the preference if available
      curClasses = X[i].count(1) #count number of filled slots
      if curClasses >= cap[i]: #stop adding classes after cap
        counter +=1
        continue
      for j in range(len(preferences[i])):
        S = X[i].copy()
        S[j] = 1
        if (value(i, S, cap, preferences, slots) > value(i, X[i], cap, preferences, slots) and availClasses[j] != 0): #new good must add value for it to be kept
          availClasses[j] -= 1
          X[i][j] = 1
          incUtil = True
          break
    if (incUtil == False):
      break

  #print results
  # for i in playerInd:
  #   print(f"Player {i} preferred:", preferences[i])
  #   print(f"Player {i} classes  :", X[i])
  #   print("-----")
  #print("Final output of RR:",X)
  return X

def expandPrefs(preferences, availClasses):
  n = len(preferences)
  m = len(preferences[0])

  newPref = [[] for i in range(n)]
  for i in range(len(preferences)): # for each student
    for j in range(m): # for each class type
      for k in range(availClasses[j]):
        if (preferences[i][j] == 1): #generate an expanded preference list to include every single seat
          newPref[i].append(1)
        else:
          newPref[i].append(0)

  return newPref

def expandSlots(slots, availClasses):
  m = len(slots)

  newSlots = {}
  i = 0
  for j in range(m): # for each class type
    for k in range(availClasses[j]):
      #generate an expanded time slot list to include every single seat
      newSlots[i] = slots[j]
      i += 1
  return newSlots


def allSeats(availClasses):
    return sum(availClasses) # total # of seats

##YANKEE SWAP

def pickAgent(X, P):
  v = len(X[0]) + 15
  theagent = -5
  for i in P:
    v_i = sum(X[i])
    if v_i < v:
      v = v_i
      theagent = i
  return theagent

def cleanAllocation(X, classes,n,m):
  Y = {}
  for i in range(n):
    z = []
    for g in range(m):
      if (X[i][g] == 1):
        z.append(classes[g])
    Y[i] = z
  return Y


def listFormatter(l, sep=','):
  list_string = ''
  for i in range(len(l)):
    list_string += l[i]
    if (i != len(l) - 1):
      list_string += sep + ' '
  return list_string



def InitializeExchangeGraph(i, X, m, n, preferences, cap, slots):
  exchange_graph = nx.DiGraph()
  for j in range(m):
    # iprime is the agent who owns the item j. Initialized to be n - the empty agent.
    iprime = n
    for ii in range(n):
      if X[ii][j] == 1:
        # ii is the agent who owns j
        iprime = ii  # PROBLEM: ONLY adds the first agent to own this class
        break
    exchange_graph.add_node(j, subset=iprime)

  # next, create edges
  for g in range(m):
    for gprime in range(m):
      if (gprime == g):
        continue
      for j in range(n):
        # j owns g, swap it out with gprime
        if (X[j][g] == 1):
          S = X[j].copy()
          S[g] = 0
          S[gprime] = 1
          # if j likes gprime as much as g, then we draw an edge from g to gprime
          if (value(j, S, cap, preferences, slots) == value(j, X[j], cap, preferences, slots)):
            exchange_graph.add_edge(g, gprime)

  # Need to add a new source node to find the shortest paths to the pool of unallocated goods
  exchange_graph.add_node(-1, subset=-1)
  # add an edge from the -1 node to every item that has a marginal gain of 1 to i
  for g in range(m):
    if (X[i][g] == 1):
      continue
    S = X[i].copy()
    S[g] = 1
    if (value(i, S, cap, preferences, slots) > value(i, X[i], cap, preferences, slots)):
      exchange_graph.add_edge(-1, g)
  return exchange_graph


def YankeeSwap(cap, preferences, availClasses, slots):  # WIP: allow for each class to hold x seats
  n = len(preferences)  # number of students
  m = len(preferences[0])  # number of classes
  X = [[0] * m for i in range(n)]  # Initialize the allocation as a binary matrix
  P = list(np.arange(n))  # The set of people playing the game

  unallocated_goods = list(np.arange(m))
  count = 1
  num_enrolled = {}

  # number_seats = availClasses, this is paramaterized from: classes["Enrl Capacity"]
  for i in range(m):
    num_enrolled[i] = 0

  while (len(P) != 0):
    # print("Iteration %d" % count)
    # print('-------------')
    count += 1
    # Need to pick an agent in P
    i = pickAgent(X, P)
    #print("Student Picked: %s" % i)

    # Need to construct the exchange graph and find a path
    exchange_graph = InitializeExchangeGraph(i, X, m, n, preferences, cap, slots)

    # Compute all single source shortest paths
    paths = nx.single_source_shortest_path(exchange_graph, -1)

    # Check if there is a path from g to the pool of unallocated goods
    final_good = -1
    path_len = float('inf')
    for g in range(m):
      if g not in unallocated_goods:
        continue
      if g in paths and len(paths[g]) < path_len:
        final_good = g
        path_len = len(paths[g])
        # break

    # If no path exists, the chosen player is out
    if (final_good == -1):
      #print("No path found. Removing player %d." % i)
      P.remove(i)
      continue

    # If path exists, print path and transfer goods along the path

    path = paths[final_good]
    num_enrolled[final_good] += 1
    if num_enrolled[final_good] >= availClasses[final_good]:
      unallocated_goods.remove(final_good)

    X[i][path[1]] = 1  # add the class
    # print("Path found: " + str(listFormatter([classes[item] for item in path], sep = ' ->')))

    for iter in range(1, len(path) - 1):  # swaps the class out with any student, and gives them the wrong one
      for j in range(n):
        if X[j][path[iter]] == 1 and preferences[j][path[iter + 1]]:
          X[j][path[iter]] = 0
          X[j][path[iter + 1]] = 1
          break
    # print("Transfer Successful")
    '''Y = cleanAllocation(X)
    print("Allocation after transfer: ")
    for i in range(n):
        print(students[i] + ": " + str(listFormatter(Y[i])))
    print()'''
    # print(X)

  #print("No agent left in P. Algorithm terminates.")
  #print("The final output of YS: ", X)
  return X  # return the unformatted version

def maxMatch(i, S, preferences, slots, cap): #agent i, given classes S
  B = [0 for n in range(len(S))] #Best class selection
  for c in range(len(S)):
    valid = True

    if not (S[c] == 1 and preferences[i][c] == 1): #skip if S is not assigned or is not a preference
      valid = False
    for j in range(len(B)):
      if B[j] == 1 and slots[j] == slots[c]: #skip if time slot matches a previously existing time slot
        valid = False

    if valid:
      B[c] = 1 #add the class
  return min(B.count(1), cap[i]) #return number of classes in B, but capped

