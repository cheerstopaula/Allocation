from agent_functions import Agent, gen_random_agents
from item_functions import generate_items_from_schedule
from allocation_functions import yankee_swap, SPIRE_algorithm, round_robin
from metric_functions import utilitarian_welfare, nash_welfare, EF, EF_1, EF_X, leximin
import matplotlib.pyplot as plt
import random
import numpy as np
from timeit import default_timer as timer
import time
seed = 1
random.seed(seed)
np.random.seed(seed)


items=generate_items_from_schedule('fall2023schedule-2.xlsx')

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
n=50

YS_runtime=[]
YS_process_runtime=[]
RR_runtime=[]
RR_process_runtime=[]
SP_runtime=[]
SP_process_runtime=[]

for seed in seeds:
    random.seed(seed)
    np.random.seed(seed)

    agents=gen_random_agents(n,items)
    for agent in agents:
        print(agent.id, 'cap:', agent.cap)
        print('desired items: ',agent.desired_items)
    start_process=time.process_time()
    start = timer()
    X=yankee_swap(agents, items, plot_exchange_graph=False)
    end_process=time.process_time()
    end = timer()
    YS_runtime.append(end-start)
    YS_process_runtime.append(end_process-start_process)
    
    YS_utilitarian.append(utilitarian_welfare(X,agents,items))
    YS_nash_zeros.append(nash_welfare(X, agents,items)[0])
    YS_nash.append(nash_welfare(X, agents,items)[1])
    YS_EF.append(EF(X, agents,items))
    YS_EF_1.append(EF_1(X, agents,items))
    YS_EF_X.append(EF_X(X, agents,items))


    start_process=time.process_time()
    start = timer()
    X=round_robin(agents,items)
    end_process=time.process_time()
    end = timer()
    RR_runtime.append(end-start)
    RR_process_runtime.append(end_process-start_process)
    
    RR_utilitarian.append(utilitarian_welfare(X,agents,items))
    RR_nash_zeros.append(nash_welfare(X, agents,items)[0])
    RR_nash.append(nash_welfare(X, agents,items)[1])
    RR_EF.append(EF(X, agents,items))
    RR_EF_1.append(EF_1(X, agents,items))
    RR_EF_X.append(EF_X(X, agents,items))


    start_process=time.process_time()
    start = timer()
    X=SPIRE_algorithm(agents,items)
    end_process=time.process_time()
    end = timer()
    SP_runtime.append(end-start)
    SP_process_runtime.append(end_process-start_process)
    
    SP_utilitarian.append(utilitarian_welfare(X,agents,items))
    SP_nash_zeros.append(nash_welfare(X, agents,items)[0])
    SP_nash.append(nash_welfare(X, agents,items)[1])
    SP_EF.append(EF(X, agents,items))
    SP_EF_1.append(EF_1(X, agents,items))
    SP_EF_X.append(EF_X(X, agents,items))


f= open("time_"+str(n)+".txt","w+")
f.write('Yanyee Swap processor runtime:')
for t in YS_process_runtime:
    f.write(str(t)+',')
f.write('\n')

f.write('Yanyee Swap runtime: ')
for t in YS_runtime:
    f.write(str(t)+',')
f.write('\n')

f.write('Round Robin processor runtime:')
for t in RR_process_runtime:
    f.write(str(t)+',')
f.write('\n')

f.write('Round Robin runtime: ')
for t in RR_runtime:
    f.write(str(t)+',')
f.write('\n')

f.write('SPIRE processor runtime:')
for t in SP_process_runtime:
    f.write(str(t)+',')
f.write('\n')

f.write('SPIRE runtime: ')
for t in SP_runtime:
    f.write(str(t)+',')
f.write('\n')


colors_list = ["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
            "#DEBB9B", "#FAB0E4", "#CFCFCF", "#FFFEA3", "#B9F2F0"]
colors=colors_list[:3]

barWidth = 0.15
fig = plt.subplots(figsize =(12, 8))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_utilitarian, color =colors[0], width = barWidth, alpha=1,  
        edgecolor =colors[0], label ='Yankee Swap')
plt.bar(br2, RR_utilitarian, color =colors[1], width = barWidth, alpha=1, 
        edgecolor =colors[1], label ='Round Robin')
plt.bar(br3, SP_utilitarian, color =colors[2], width = barWidth, alpha=1,  
        edgecolor =colors[2], label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('Utilitarian Welfare', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)
plt.ylim([0,5])
plt.legend()
plt.savefig('./Figures/Utilitarian_'+str(n)+'.png')
plt.close()





barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_nash_zeros, color =colors[0], width = barWidth, alpha=1,  
        edgecolor =colors[0], label ='Yankee Swap')
plt.bar(br2, RR_nash_zeros, color =colors[1], width = barWidth, alpha=1,  
        edgecolor =colors[1], label ='Round Robin')
plt.bar(br3, SP_nash_zeros, color =colors[2], width = barWidth, alpha=1,  
        edgecolor =colors[2], label ='SPIRE algorithm')

#plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('Nash Number of Zeros', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)
plt.ylim([0,5])
plt.legend()
plt.savefig('./Figures/Nash_zeros_'+str(n)+'.png')
plt.close()



barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_nash, color =colors[0], width = barWidth, alpha=1,  
        edgecolor =colors[0], label ='Yankee Swap')
plt.bar(br2, RR_nash, color =colors[1], width = barWidth, alpha=1,  
        edgecolor =colors[1], label ='Round Robin')
plt.bar(br3, SP_nash, color =colors[2], width = barWidth, alpha=1,  
        edgecolor =colors[2], label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('Nash Welfare', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)
plt.ylim([0,5])
plt.legend()
plt.savefig('./Figures/Nash_'+str(n)+'.png')
plt.close()



barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_EF, color =colors[0], width = barWidth, alpha=1,  
        edgecolor =colors[0], label ='Yankee Swap')
plt.bar(br2, RR_EF, color =colors[1], width = barWidth, alpha=1,  
        edgecolor =colors[1], label ='Round Robin')
plt.bar(br3, SP_EF, color =colors[2], width = barWidth, alpha=1,  
        edgecolor =colors[2], label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('EF', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)

plt.legend()
plt.savefig('./Figures/EF_'+str(n)+'.png')
plt.close()



barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_EF_1, color =colors[0], width = barWidth, alpha=1,  
        edgecolor =colors[0], label ='Yankee Swap')
plt.bar(br2, RR_EF_1, color =colors[1], width = barWidth, alpha=1,  
        edgecolor =colors[1], label ='Round Robin')
plt.bar(br3, SP_EF_1, color =colors[2], width = barWidth, alpha=1,  
        edgecolor =colors[2], label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('EF_1', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)

plt.legend()
plt.savefig('./Figures/EF_1_'+str(n)+'.png')
plt.close()

barWidth = 0.15
fig = plt.subplots(figsize =(12, 4))
br1 = np.arange(len(seeds))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, YS_EF_X, color =colors[0], width = barWidth, alpha=1,  
        edgecolor =colors[0], label ='Yankee Swap')
plt.bar(br2, RR_EF_X, color =colors[1], width = barWidth, alpha=1,  
        edgecolor =colors[1], label ='Round Robin')
plt.bar(br3, SP_EF_X, color =colors[2], width = barWidth, alpha=1,  
        edgecolor =colors[2], label ='SPIRE algorithm')

plt.xlabel('Seed',  fontsize = 15)
plt.ylabel('EF_X', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(seeds))],
        seeds)

plt.legend()
plt.savefig('./Figures/EF_X_'+str(n)+'.png')
plt.close()