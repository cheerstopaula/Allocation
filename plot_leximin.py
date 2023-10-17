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
n=50

for seed in seeds:
    random.seed(seed)
    np.random.seed(seed)

    agents=gen_random_agents(n,items)
    for agent in agents:
        print(agent.id, 'cap:', agent.cap)
        print('desired items: ',agent.desired_items)

    X=yankee_swap(agents, items, plot_exchange_graph=False)
    YS_leximin=leximin(X,agents,items)
    YS_utilitarian.append(utilitarian_welfare(X,agents,items))
    YS_nash_zeros.append(nash_welfare(X, agents,items)[0])
    YS_nash.append(nash_welfare(X, agents,items)[1])
    YS_EF.append(EF(X, agents,items))

    X=round_robin(agents,items)
    RR_leximin=leximin(X,agents,items)
    RR_utilitarian.append(utilitarian_welfare(X,agents,items))
    RR_nash_zeros.append(nash_welfare(X, agents,items)[0])
    RR_nash.append(nash_welfare(X, agents,items)[1])
    RR_EF.append(EF(X, agents,items))

    X=SPIRE_algorithm(agents,items)
    SP_leximin=leximin(X,agents,items)
    SP_utilitarian.append(utilitarian_welfare(X,agents,items))
    SP_nash_zeros.append(nash_welfare(X, agents,items)[0])
    SP_nash.append(nash_welfare(X, agents,items)[1])
    SP_EF.append(EF(X, agents,items))


# Implementation of matplotlib function

colors = ['C0','C1','C2']

plt.hist([YS_leximin,RR_leximin,SP_leximin], bins=[1,2,3,4,5,6,7,8,9,10],  alpha=0.4, rwidth=0.7,
         histtype ='bar',
         color = colors,
         cumulative=True,
         #label = ['Yanyee Swap','Round Robin', 'SPIRE algorithm']
         )
#plt.xticks([1,2,3,4,5,6,7,8,9,10])

plt.hist([YS_leximin,RR_leximin,SP_leximin], bins=[1,2,3,4,5,6,7,8,9,10],  rwidth=0.7,
         histtype ='bar',
         color = colors,
         #cumulative=True,
         label = ['Yanyee Swap','Round Robin', 'SPIRE algorithm'])
plt.xticks([1,2,3,4,5,6,7,8,9,10])

plt.axvline(sum(YS_leximin)/len(YS_leximin), color='C0', linestyle='dashed', linewidth=1)
plt.axvline(sum(RR_leximin)/len(RR_leximin), color='C1', linestyle='dashed', linewidth=1)
plt.axvline(sum(SP_leximin)/len(SP_leximin), color='C2', linestyle='dashed', linewidth=1)

plt.legend(prop ={'size': 10})
plt.show()
# plt.title('Leximin Vector Histogram, N='+str(n),
#           fontweight = "bold")
# plt.savefig('leximin_'+str(n)+'.png')
# plt.close()





# (nYS, bins2, patches) = plt.hist(YS_leximin, bins=[1,2,3,4,5,6,7,8,9,10], label='hst')
# (nRR, bins2, patches) = plt.hist(RR_leximin, bins=[1,2,3,4,5,6,7,8,9,10], label='hst')
# (nSP, bins2, patches) = plt.hist(SP_leximin, bins=[1,2,3,4,5,6,7,8,9,10], label='hst')
# plt.close()

# plt.hist([YS_leximin,RR_leximin,SP_leximin], bins=[1,2,3,4,5,6,7,8,9,10], alpha=0.6,  rwidth=0.7,
#          histtype ='bar',
#          color = colors,
#          label = ['Yanyee Swap','Round Robin', 'SPIRE algorithm'])
# plt.xticks([1,2,3,4,5,6,7,8,9,10])
# plt.plot([1.25,2.25,3.25,4.25,5.25,6.25,7.25,8.25,9.25],nYS, color='C0', linewidth=2.5)
# plt.plot([1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5],nRR, color='C1', linewidth=2.5)
# plt.plot([1.75,2.75,3.75,4.75,5.75,6.75,7.75,8.75,9.75],nSP, color='C2', linewidth=2.5)

# plt.axvline(sum(YS_leximin)/len(YS_leximin), color='C0', linestyle='dashed', linewidth=1)
# plt.axvline(sum(RR_leximin)/len(RR_leximin), color='C1', linestyle='dashed', linewidth=1)
# plt.axvline(sum(SP_leximin)/len(SP_leximin), color='C2', linestyle='dashed', linewidth=1)

# plt.legend(prop ={'size': 10})
# plt.title('Leximin Vector Histogram, N='+str(n),
#           fontweight = "bold")
# plt.savefig('leximin_curve_'+str(n)+'.png')
# plt.close()
