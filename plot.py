from agent_functions import Agent, gen_random_agents
from item_functions import generate_items_from_schedule
from allocation_functions import yankee_swap, SPIRE_algorithm, round_robin
from metric_functions import utilitarian_welfare, nash_welfare, EF, EF_1, EF_X, leximin
import matplotlib.pyplot as plt
import random
import numpy as np
from timeit import default_timer as timer
seed = 1
random.seed(seed)
np.random.seed(seed)


items=generate_items_from_schedule('fall2023schedule.xlsx')

YS_utilitarian=[]
YS_nash_zeros=[]
YS_nash=[]
YS_EF=[]
YS_EF_1=[]
YS_EF_X=[]

RR_utilitarian=[]
RR_nash_zeros=[]
RR_nash=[]
RR_EF=[]
RR_EF_1=[]
RR_EF_X=[]

SP_utilitarian=[]
SP_nash_zeros=[]
SP_nash=[]
SP_EF=[]
SP_EF_1=[]
SP_EF_X=[]

seeds=[0,1,2,3,4,5,6,7,8,9]
n=500

YS_runtime=[]

for seed in seeds:
    random.seed(seed)
    np.random.seed(seed)

    agents=gen_random_agents(n,items)
    for agent in agents:
        print(agent.id, 'cap:', agent.cap)
        print('desired items: ',agent.desired_items)

    start = timer()
    X=yankee_swap(agents, items, plot_exchange_graph=False)
    end = timer()
    YS_runtime.append(end-start)
    
    YS_utilitarian.append(utilitarian_welfare(X,agents,items))
    YS_nash_zeros.append(nash_welfare(X, agents,items)[0])
    YS_nash.append(nash_welfare(X, agents,items)[1])
    YS_EF.append(EF(X, agents,items))
    YS_EF_1.append(EF_1(X, agents,items))
    YS_EF_X.append(EF_X(X, agents,items))

    X=round_robin(agents,items)
    
    RR_utilitarian.append(utilitarian_welfare(X,agents,items))
    RR_nash_zeros.append(nash_welfare(X, agents,items)[0])
    RR_nash.append(nash_welfare(X, agents,items)[1])
    RR_EF.append(EF(X, agents,items))
    RR_EF_1.append(EF_1(X, agents,items))
    RR_EF_X.append(EF_X(X, agents,items))

    X=SPIRE_algorithm(agents,items)
    
    SP_utilitarian.append(utilitarian_welfare(X,agents,items))
    SP_nash_zeros.append(nash_welfare(X, agents,items)[0])
    SP_nash.append(nash_welfare(X, agents,items)[1])
    SP_EF.append(EF(X, agents,items))
    SP_EF_1.append(EF_1(X, agents,items))
    SP_EF_X.append(EF_X(X, agents,items))




print(YS_runtime)
print(sum(YS_runtime)/len(YS_runtime))

barWidth = 0.15
fig = plt.subplots(figsize =(12, 8))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_utilitarian, color ='C0', width = barWidth, alpha=0.75,  
        edgecolor ='C0', label ='Yankee Swap')
plt.bar(br2, RR_utilitarian, color ='C1', width = barWidth, alpha=0.75, 
        edgecolor ='C1', label ='Round Robin')
plt.bar(br3, SP_utilitarian, color ='C2', width = barWidth, alpha=0.75,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('Utilitarian Welfare', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)
plt.ylim([0,5])
plt.legend()
plt.savefig('Utilitarian_'+str(n)+'.png')
plt.close()





barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_nash_zeros, color ='C0', width = barWidth, alpha=0.75,  
        edgecolor ='C0', label ='Yankee Swap')
plt.bar(br2, RR_nash_zeros, color ='C1', width = barWidth, alpha=0.75,  
        edgecolor ='C1', label ='Round Robin')
plt.bar(br3, SP_nash_zeros, color ='C2', width = barWidth, alpha=0.75,  
        edgecolor ='C2', label ='SPIRE algorithm')

#plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('Nash Number of Zeros', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)
plt.ylim([0,5])
plt.legend()
plt.savefig('Nash_zeros_'+str(n)+'.png')
plt.close()



barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_nash, color ='C0', width = barWidth, alpha=0.75,  
        edgecolor ='C0', label ='Yankee Swap')
plt.bar(br2, RR_nash, color ='C1', width = barWidth, alpha=0.75,  
        edgecolor ='C1', label ='Round Robin')
plt.bar(br3, SP_nash, color ='C2', width = barWidth, alpha=0.75,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('Nash Welfare', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)
plt.ylim([0,5])
plt.legend()
plt.savefig('Nash_'+str(n)+'.png')
plt.close()



barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_EF, color ='C0', width = barWidth, alpha=0.75,  
        edgecolor ='C0', label ='Yankee Swap')
plt.bar(br2, RR_EF, color ='C1', width = barWidth, alpha=0.75,  
        edgecolor ='C1', label ='Round Robin')
plt.bar(br3, SP_EF, color ='C2', width = barWidth, alpha=0.75,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('EF', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)

plt.legend()
plt.savefig('EF_'+str(n)+'.png')
plt.close()



barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_EF_1, color ='C0', width = barWidth, alpha=0.75,  
        edgecolor ='C0', label ='Yankee Swap')
plt.bar(br2, RR_EF_1, color ='C1', width = barWidth, alpha=0.75,  
        edgecolor ='C1', label ='Round Robin')
plt.bar(br3, SP_EF_1, color ='C2', width = barWidth, alpha=0.75,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('EF_1', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)

plt.legend()
plt.savefig('EF_1_'+str(n)+'.png')
plt.close()

barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_EF_X, color ='C0', width = barWidth, alpha=0.75,  
        edgecolor ='C0', label ='Yankee Swap')
plt.bar(br2, RR_EF_X, color ='C1', width = barWidth, alpha=0.75,  
        edgecolor ='C1', label ='Round Robin')
plt.bar(br3, SP_EF_X, color ='C2', width = barWidth, alpha=0.75,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('EF_X', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)

plt.legend()
plt.savefig('EF_X_'+str(n)+'.png')
plt.close()