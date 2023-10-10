from agent_functions import Agent, gen_random_agents
from item_functions import generate_items_from_schedule
from allocation_functions import yankee_swap, SPIRE_algorithm, round_robin
from metric_functions import utilitarian_welfare, nash_welfare, EF, leximin
import matplotlib.pyplot as plt
import random
import numpy as np
seed = 1
random.seed(seed)
np.random.seed(seed)


items=generate_items_from_schedule('fall2023schedule.xlsx')

YS_utilitarian=[]
YS_nash_zeros=[]
YS_nash=[]
YS_EF=[]

RR_utilitarian=[]
RR_nash_zeros=[]
RR_nash=[]
RR_EF=[]

SP_utilitarian=[]
SP_nash_zeros=[]
SP_nash=[]
SP_EF=[]

seeds=[0]

for seed in seeds:
    random.seed(seed)
    np.random.seed(seed)

    agents=gen_random_agents(200,items)
    for agent in agents:
        print(agent.id, 'cap:', agent.cap)
        print('desired items: ',agent.desired_items)


    X=yankee_swap(agents, items, plot_exchange_graph=False)
    YS_leximin=leximin(X,agents,items)
    print(YS_leximin)
    YS_utilitarian.append(utilitarian_welfare(X,agents,items))
    YS_nash_zeros.append(nash_welfare(X, agents,items)[0])
    YS_nash.append(nash_welfare(X, agents,items)[1])
    YS_EF.append(EF(X, agents,items))





    X=round_robin(agents,items)
    RR_leximin=leximin(X,agents,items)
    print(RR_leximin)
    RR_utilitarian.append(utilitarian_welfare(X,agents,items))
    RR_nash_zeros.append(nash_welfare(X, agents,items)[0])
    RR_nash.append(nash_welfare(X, agents,items)[1])
    RR_EF.append(EF(X, agents,items))




    X=SPIRE_algorithm(agents,items)
    SP_leximin=leximin(X,agents,items)
    print(SP_leximin)
    SP_utilitarian.append(utilitarian_welfare(X,agents,items))
    SP_nash_zeros.append(nash_welfare(X, agents,items)[0])
    SP_nash.append(nash_welfare(X, agents,items)[1])
    SP_EF.append(EF(X, agents,items))

fig = plt.figure(figsize = (10, 3))
 
# creating the bar plot
plt.bar([*range(0, 200, 1)], YS_leximin, color ='C0',
        width = 0.4)
#plt.xlabel("Courses offered")
# plt.ylabel("No. of students enrolled")
# plt.title("Students enrolled in different courses")


#fig = plt.figure(figsize = (10, 3))
plt.bar([*range(0, 200, 1)], RR_leximin, color ='C1',
        width = 0.4)


#fig = plt.figure(figsize = (10, 3))
plt.bar([*range(0, 200, 1)], SP_leximin, color ='C2',
        width = 0.4)
plt.savefig('lexvec.png')
plt.close()


# barWidth = 0.15
# fig = plt.subplots(figsize =(12, 8))
# br1 = np.arange(len(seeds))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]

# plt.bar(br1, YS_utilitarian, color ='C0', width = barWidth,
#         edgecolor ='C0', label ='Yankee Swap')
# plt.bar(br2, RR_utilitarian, color ='C1', width = barWidth,
#         edgecolor ='C1', label ='Round Robin')
# plt.bar(br3, SP_utilitarian, color ='C2', width = barWidth,
#         edgecolor ='C2', label ='SPIRE algorithm')

# plt.xlabel('Seed',  fontsize = 15)
# plt.ylabel('Utilitarian Welfare', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
# plt.ylim([0,5])
# plt.legend()
# plt.savefig('Utilitarian.png')
# plt.close()





# barWidth = 0.15
# fig = plt.subplots(figsize =(12, 4))
# br1 = np.arange(len(seeds))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]

# plt.bar(br1, YS_nash_zeros, color ='C0', width = barWidth,
#         edgecolor ='C0', label ='Yankee Swap')
# plt.bar(br2, RR_nash_zeros, color ='C1', width = barWidth,
#         edgecolor ='C1', label ='Round Robin')
# plt.bar(br3, SP_nash_zeros, color ='C2', width = barWidth,
#         edgecolor ='C2', label ='SPIRE algorithm')

# #plt.xlabel('Seed',  fontsize = 15)
# plt.ylabel('Nash Number of Zeros', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
# plt.ylim([0,5])
# plt.legend()
# plt.savefig('Nash_zeros.png')
# plt.close()



# barWidth = 0.15
# fig = plt.subplots(figsize =(12, 4))
# br1 = np.arange(len(seeds))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]

# plt.bar(br1, YS_nash, color ='C0', width = barWidth,
#         edgecolor ='C0', label ='Yankee Swap')
# plt.bar(br2, RR_nash, color ='C1', width = barWidth,
#         edgecolor ='C1', label ='Round Robin')
# plt.bar(br3, SP_nash, color ='C2', width = barWidth,
#         edgecolor ='C2', label ='SPIRE algorithm')

# plt.xlabel('Seed',  fontsize = 15)
# plt.ylabel('Nash Welfare', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
# plt.ylim([0,5])
# plt.legend()
# plt.savefig('Nash.png')
# plt.close()



# barWidth = 0.15
# fig = plt.subplots(figsize =(12, 4))
# br1 = np.arange(len(seeds))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]

# plt.bar(br1, YS_EF, color ='C0', width = barWidth,
#         edgecolor ='C0', label ='Yankee Swap')
# plt.bar(br2, RR_EF, color ='C1', width = barWidth,
#         edgecolor ='C1', label ='Round Robin')
# plt.bar(br3, SP_EF, color ='C2', width = barWidth,
#         edgecolor ='C2', label ='SPIRE algorithm')

# plt.xlabel('Seed',  fontsize = 15)
# plt.ylabel('EF', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)

# plt.legend()
# plt.savefig('EF.png')
# plt.close()



# plt.plot(seeds,YS_utilitarian,label='Yankee Swap', color='C0')
# plt.plot(seeds,RR_utilitarian,label='Round Robin', color='C1')
# plt.plot(seeds,SP_utilitarian,label='SPIRE algorithm', color='C2')
# plt.xlabel('Seed')
# plt.ylabel('Utilitarian Welfare')
# plt.legend()
# plt.xticks(seeds)
# plt.show()

# print('YS Allocation')
# X=yankee_swap(agents, items, plot_exchange_graph=False)
# print(X)
# print('utilitarian: ',utilitarian_welfare(X,agents,items))
# print('Nash:',nash_welfare(X, agents,items))
# print('EF:',EF(X, agents,items))

# X=round_robin(agents,items)
# print('RR allocation')
# print(X)
# print('utilitarian: ',utilitarian_welfare(X,agents,items))
# print('Nash:',nash_welfare(X, agents,items))
# print('EF:',EF(X, agents,items))

# X=SPIRE_algorithm(agents,items)
# print('SPIRE allocation')
# print(X)
# print('utilitarian: ',utilitarian_welfare(X,agents,items))
# print('Nash:',nash_welfare(X, agents,items))
# print('EF:',EF(X, agents,items))