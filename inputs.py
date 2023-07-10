import pandas as pd
import random
import math

def get_schedule(classes):
    topics = {}  # gives a dictionary with
    instructors = {}
    numClasses = 0
    for index, row in classes.iterrows():
        numClasses += 1
        temp_categories = row["Categories"].split(",")
        for i in temp_categories:
            if i in topics.keys():
                topics[i].append(index)
            else:
                topics[i] = [index]
        # for index,row in classes.iterrows():
        temp = row["InstructorPrint"]
        if temp in instructors.keys():
            instructors[temp].append(index)
        else:
            instructors[temp] = [index]

    schedule = {}  # dictionary of {class index: class time}
    slots = {}  # dictionary of {class index: time slot #}
    for index, row in classes.iterrows():
        schedule[index] = str(row["zc.days"]) + str(row["Mtg Time"])  # was previously indexed by row["Class Nbr"]
    slotList = list(set(schedule.values()))  # creates a list of every available slot time

    for i, j in enumerate(schedule.values()):
        slots[i] = slotList.index(j)

    return topics,instructors,numClasses,schedule, slots

def genStudent(m, cap, tops, profs, topics, instructors): #m: num, cap: num, tops: str[], profs: str[]
  S = [0 for n in range(m)] #class selection
  L = [] #list of possible wanted classes

  #add all classes from a preferred topic or professor
  for i in tops:
    for j in topics[i]:
      L.append(j)
  for i in profs:
    for j in instructors[i]:
      L.append(j)
  #note - if there is a overlap between a pref. professor/topic, double count the class (higher weight for random selection)
  #DONE: deduplicate results
  prefSet = list(set(L))
  #random selection
  #print("--")
  #print(prefSet)
  random.shuffle(prefSet)
  for i in range(min(cap,len(prefSet))):
    S[prefSet[i]] = 1 #pick random classes from list of classes until cap is reached
  return S


def genMany(n, topics, instructors, numClasses, seed):
  random.seed(seed)
  s = []
  allTops = list(topics.keys())
  allInstr = list(instructors.keys())
  for i in range(n):
    random.shuffle(allTops)
    random.shuffle(allInstr)
    #choose a topic
    numTops = math.floor(random.random()*3) + 1
    numInstr = math.floor(random.random()*3) + 1
    tops = []
    instr = []
    for j in range(numTops):
      tops.append(allTops[j])
    for j in range(numInstr):
      instr.append(allInstr[j])
    s.append(genStudent(numClasses, 3, tops, instr,topics, instructors))
  return s