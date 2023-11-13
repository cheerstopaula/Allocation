from allocation.agent_functions import Agent, gen_random_agents
from allocation.item_functions import generate_items_from_schedule
from allocation.allocation_functions import yankee_swap, SPIRE_algorithm, round_robin
from allocation.metric_functions import utilitarian_welfare, nash_welfare, EF, EF_1, EF_X, leximin
import matplotlib.pyplot as plt
import random
import numpy as np
from timeit import default_timer as timer
import time

n=2000

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

YS_runtime=[]
RR_runtime=[]
SP_runtime=[]
seeds=[0,1,2,3,4,5,6,7,8,9]

for seed in seeds:
    random.seed(seed)
    np.random.seed(seed)
    agents=gen_random_agents(n,items)
    data=np.load(f'YS_{n}_{seed}.npz')
    X=data['X']
    time_steps=data['time_steps']
    YS_runtime.append(time_steps)
    print('YS')
    YS_utilitarian.append(utilitarian_welfare(X,agents,items))
    YS_nash_zeros.append(nash_welfare(X, agents,items)[0])
    YS_nash.append(nash_welfare(X, agents,items)[1])
    YS_EF.append(EF(X, agents,items))
    YS_EF_1.append(EF_1(X, agents,items))
    YS_EF_X.append(EF_X(X, agents,items))
    print("RR")
    start_process=time.process_time()
    X=round_robin(agents,items)
    end_process=time.process_time()
    RR_runtime.append(end_process-start_process)
    
    RR_utilitarian.append(utilitarian_welfare(X,agents,items))
    RR_nash_zeros.append(nash_welfare(X, agents,items)[0])
    RR_nash.append(nash_welfare(X, agents,items)[1])
    RR_EF.append(EF(X, agents,items))
    RR_EF_1.append(EF_1(X, agents,items))
    RR_EF_X.append(EF_X(X, agents,items))

    print('SP')
    start_process=time.process_time()
    X=SPIRE_algorithm(agents,items)
    end_process=time.process_time()
    SP_runtime.append(end_process-start_process)
    
    SP_utilitarian.append(utilitarian_welfare(X,agents,items))
    SP_nash_zeros.append(nash_welfare(X, agents,items)[0])
    SP_nash.append(nash_welfare(X, agents,items)[1])
    SP_EF.append(EF(X, agents,items))
    SP_EF_1.append(EF_1(X, agents,items))
    SP_EF_X.append(EF_X(X, agents,items))

print(YS_utilitarian)
print(sum(YS_utilitarian)/len(YS_utilitarian))

print(RR_utilitarian)
print(sum(RR_utilitarian)/len(RR_utilitarian))

print(SP_utilitarian)
print(sum(SP_utilitarian)/len(SP_utilitarian))

colors_list = ["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
            "#DEBB9B", "#FAB0E4", "#CFCFCF", "#FFFEA3", "#B9F2F0"]
colors=colors_list[:3]
# fig = plt.subplots(figsize =(5, 5))

# x = [1, 2, 3]
# y = [sum(YS_utilitarian)/len(YS_utilitarian), sum(RR_utilitarian)/len(RR_utilitarian), sum(SP_utilitarian)/len(SP_utilitarian)]

 
# # creating error
# y_errormin = [sum(YS_utilitarian)/len(YS_utilitarian)-min(YS_utilitarian),sum(RR_utilitarian)/len(RR_utilitarian)- min(RR_utilitarian), sum(SP_utilitarian)/len(SP_utilitarian)-min(SP_utilitarian)]
# y_errormax = [max(YS_utilitarian)-sum(YS_utilitarian)/len(YS_utilitarian), max(RR_utilitarian)-sum(RR_utilitarian)/len(RR_utilitarian), max(SP_utilitarian)-sum(SP_utilitarian)/len(SP_utilitarian)]
# print(y_errormin)
# print(y_errormax)
 
# y_error = [y_errormin, y_errormax]
 
# # plotting graph
# plt.bar(x,y)
 
# plt.errorbar(x, y,
#              yerr=y_error,
#              fmt='o', color="k")  # you can use color ="r" for red or skip to default as blue
# plt.show()

# f= open("time_"+str(n)+".txt","w+")
# f.write('Yanyee Swap processor runtime:')
# for t in YS_process_runtime:
#     f.write(str(t)+',')
# f.write('\n')

# f.write('Yanyee Swap runtime: ')
# for t in YS_runtime:
#     f.write(str(t)+',')
# f.write('\n')

# f.write('Round Robin processor runtime:')
# for t in RR_process_runtime:
#     f.write(str(t)+',')
# f.write('\n')

# f.write('Round Robin runtime: ')
# for t in RR_runtime:
#     f.write(str(t)+',')
# f.write('\n')

# f.write('SPIRE processor runtime:')
# for t in SP_process_runtime:
#     f.write(str(t)+',')
# f.write('\n')

# f.write('SPIRE runtime: ')
# for t in SP_runtime:
#     f.write(str(t)+',')
# f.write('\n')

barWidth = 0.1
br1 = np.arange(1)
br2 = [x + barWidth+0.05 for x in br1]
br3 = [x + barWidth+0.05 for x in br2]

##Plot Utilitarian Welfare
fig = plt.subplots(figsize =(4, 6))
plt.bar(br1, [sum(YS_utilitarian)/len(YS_utilitarian)], color =colors[0], width = barWidth, alpha=0.8,  
        edgecolor ='C0', label ='Yankee Swap')

plt.errorbar(br1, [sum(YS_utilitarian)/len(YS_utilitarian)],
             yerr=[[sum(YS_utilitarian)/len(YS_utilitarian)-min(YS_utilitarian)], [max(YS_utilitarian)-sum(YS_utilitarian)/len(YS_utilitarian)]],
             fmt='o', color="C0") 

plt.bar(br2, [sum(RR_utilitarian)/len(RR_utilitarian)], color =colors[1], width = barWidth, alpha=0.8, 
        edgecolor ='C1', label ='Round Robin')

plt.errorbar(br2, [sum(RR_utilitarian)/len(RR_utilitarian)],
             yerr=[[sum(RR_utilitarian)/len(RR_utilitarian)-min(RR_utilitarian)], [max(RR_utilitarian)-sum(RR_utilitarian)/len(RR_utilitarian)]],
             fmt='o', color="C1") 

plt.bar(br3, [sum(SP_utilitarian)/len(SP_utilitarian)], color =colors[2], width = barWidth, alpha=0.8,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.errorbar(br3, [sum(SP_utilitarian)/len(SP_utilitarian)],
             yerr=[[sum(SP_utilitarian)/len(YS_utilitarian)-min(SP_utilitarian)], [max(SP_utilitarian)-sum(SP_utilitarian)/len(SP_utilitarian)]],
             fmt='o', color="C2") 

# plt.xlabel('Seed',  fontsize = 15)
plt.title('Utilitarian Welfare', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
plt.xticks([])
#plt.ylim([0,7])
plt.legend()
plt.savefig('./Figures/Utilitarian_'+str(n)+'.png')
plt.close()

##Plot Nash welfare

fig = plt.subplots(figsize =(4, 6))
plt.bar(br1, [sum(YS_nash)/len(YS_nash)], color =colors[0], width = barWidth, alpha=0.8,  
        edgecolor ='C0', label ='Yankee Swap')

plt.errorbar(br1, [sum(YS_nash)/len(YS_nash)],
             yerr=[[sum(YS_nash)/len(YS_nash)-min(YS_nash)], [max(YS_nash)-sum(YS_nash)/len(YS_nash)]],
             fmt='o', color="C0") 

plt.bar(br2, [sum(RR_nash)/len(RR_nash)], color =colors[1], width = barWidth, alpha=0.8, 
        edgecolor ='C1', label ='Round Robin')

plt.errorbar(br2, [sum(RR_nash)/len(RR_nash)],
             yerr=[[sum(RR_nash)/len(RR_nash)-min(RR_nash)], [max(RR_nash)-sum(RR_nash)/len(RR_nash)]],
             fmt='o', color="C1") 

plt.bar(br3, [sum(SP_nash)/len(SP_nash)], color =colors[2], width = barWidth, alpha=0.8,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.errorbar(br3, [sum(SP_nash)/len(SP_nash)],
             yerr=[[sum(SP_nash)/len(SP_nash)-min(SP_nash)], [max(SP_nash)-sum(SP_nash)/len(SP_nash)]],
             fmt='o', color="C2") 

# plt.xlabel('Seed',  fontsize = 15)
plt.title('Nash Welfare', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
plt.xticks([])
#plt.ylim([0,7])
plt.legend()
plt.savefig('./Figures/Nash_'+str(n)+'.png')
plt.close()

fig = plt.subplots(figsize =(4, 6))
plt.bar(br1, [sum(YS_nash_zeros)/len(YS_nash_zeros)], color =colors[0], width = barWidth, alpha=0.8,  
        edgecolor ='C0', label ='Yankee Swap')

plt.errorbar(br1, [sum(YS_nash_zeros)/len(YS_nash_zeros)],
             yerr=[[sum(YS_nash_zeros)/len(YS_nash_zeros)-min(YS_nash_zeros)], [max(YS_nash_zeros)-sum(YS_nash_zeros)/len(YS_nash_zeros)]],
             fmt='o', color="C0") 

plt.bar(br2, [sum(RR_nash_zeros)/len(RR_nash_zeros)], color =colors[1], width = barWidth, alpha=0.8, 
        edgecolor ='C1', label ='Round Robin')

plt.errorbar(br2, [sum(RR_nash_zeros)/len(RR_nash_zeros)],
             yerr=[[sum(RR_nash_zeros)/len(RR_nash_zeros)-min(RR_nash_zeros)], [max(RR_nash_zeros)-sum(RR_nash_zeros)/len(RR_nash_zeros)]],
             fmt='o', color="C1") 

plt.bar(br3, [sum(SP_nash_zeros)/len(SP_nash_zeros)], color =colors[2], width = barWidth, alpha=0.8,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.errorbar(br3, [sum(SP_nash_zeros)/len(SP_nash_zeros)],
             yerr=[[sum(SP_nash_zeros)/len(SP_nash_zeros)-min(SP_nash_zeros)], [max(SP_nash_zeros)-sum(SP_nash_zeros)/len(SP_nash_zeros)]],
             fmt='o', color="C2") 

# plt.xlabel('Seed',  fontsize = 15)
plt.title('Nash Zeros', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
plt.xticks([])
#plt.ylim([0,7])
plt.legend(loc='upper left')
plt.savefig('./Figures/Nash_zeros_'+str(n)+'.png')
plt.close()


##Plot EF
fig = plt.subplots(figsize =(4, 6))
plt.bar(br1, [sum(YS_EF)/len(YS_EF)], color =colors[0], width = barWidth, alpha=0.8,  
        edgecolor ='C0', label ='Yankee Swap')

plt.errorbar(br1, [sum(YS_EF)/len(YS_EF)],
             yerr=[[sum(YS_EF)/len(YS_EF)-min(YS_EF)], [max(YS_EF)-sum(YS_EF)/len(YS_EF)]],
             fmt='o', color="C0") 

plt.bar(br2, [sum(RR_EF)/len(RR_EF)], color =colors[1], width = barWidth, alpha=0.8, 
        edgecolor ='C1', label ='Round Robin')

plt.errorbar(br2, [sum(RR_EF)/len(RR_EF)],
             yerr=[[sum(RR_EF)/len(RR_EF)-min(RR_EF)], [max(RR_EF)-sum(RR_EF)/len(RR_EF)]],
             fmt='o', color="C1") 

plt.bar(br3, [sum(SP_EF)/len(SP_EF)], color =colors[2], width = barWidth, alpha=0.8,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.errorbar(br3, [sum(SP_EF)/len(SP_EF)],
             yerr=[[sum(SP_EF)/len(SP_EF)-min(SP_EF)], [max(SP_EF)-sum(SP_EF)/len(SP_EF)]],
             fmt='o', color="C2") 

# plt.xlabel('Seed',  fontsize = 15)
plt.title('EF', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
plt.xticks([])
#plt.ylim([0,7])
plt.legend(loc='upper left')
plt.savefig('./Figures/EF_'+str(n)+'.png')
plt.close()


##Plot EF-1
fig = plt.subplots(figsize =(4, 6))
plt.bar(br1, [sum(YS_EF_1)/len(YS_EF_1)], color =colors[0], width = barWidth, alpha=0.8,  
        edgecolor ='C0', label ='Yankee Swap')

plt.errorbar(br1, [sum(YS_EF_1)/len(YS_EF_1)],
             yerr=[[sum(YS_EF_1)/len(YS_EF_1)-min(YS_EF_1)], [max(YS_EF_1)-sum(YS_EF_1)/len(YS_EF_1)]],
             fmt='o', color="C0") 

plt.bar(br2, [sum(RR_EF_1)/len(RR_EF_1)], color =colors[1], width = barWidth, alpha=0.8, 
        edgecolor ='C1', label ='Round Robin')

plt.errorbar(br2, [sum(RR_EF_1)/len(RR_EF_1)],
             yerr=[[sum(RR_EF_1)/len(RR_EF_1)-min(RR_EF_1)], [max(RR_EF_1)-sum(RR_EF_1)/len(RR_EF_1)]],
             fmt='o', color="C1") 

plt.bar(br3, [sum(SP_EF_1)/len(SP_EF_1)], color =colors[2], width = barWidth, alpha=0.8,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.errorbar(br3, [sum(SP_EF_1)/len(SP_EF_1)],
             yerr=[[sum(SP_EF_1)/len(SP_EF_1)-min(SP_EF_1)], [max(SP_EF_1)-sum(SP_EF_1)/len(SP_EF_1)]],
             fmt='o', color="C2") 

# plt.xlabel('Seed',  fontsize = 15)
plt.title('EF-1', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
plt.xticks([])
#plt.ylim([0,7])
plt.legend(loc='upper left')
plt.savefig('./Figures/EF_1_'+str(n)+'.png')
plt.close()


##Plot EF
fig = plt.subplots(figsize =(4, 6))
plt.bar(br1, [sum(YS_EF_X)/len(YS_EF_X)], color =colors[0], width = barWidth, alpha=0.8,  
        edgecolor ='C0', label ='Yankee Swap')

plt.errorbar(br1, [sum(YS_EF_X)/len(YS_EF_X)],
             yerr=[[sum(YS_EF_X)/len(YS_EF_X)-min(YS_EF_X)], [max(YS_EF_X)-sum(YS_EF_X)/len(YS_EF_X)]],
             fmt='o', color="C0") 

plt.bar(br2, [sum(RR_EF_X)/len(RR_EF_X)], color =colors[1], width = barWidth, alpha=0.8, 
        edgecolor ='C1', label ='Round Robin')

plt.errorbar(br2, [sum(RR_EF_X)/len(RR_EF_X)],
             yerr=[[sum(RR_EF_X)/len(RR_EF_X)-min(RR_EF_X)], [max(RR_EF_X)-sum(RR_EF_X)/len(RR_EF_X)]],
             fmt='o', color="C1") 

plt.bar(br3, [sum(SP_EF_X)/len(SP_EF_X)], color =colors[2], width = barWidth, alpha=0.8,  
        edgecolor ='C2', label ='SPIRE algorithm')

plt.errorbar(br3, [sum(SP_EF_X)/len(SP_EF_X)],
             yerr=[[sum(SP_EF_X)/len(SP_EF_X)-min(SP_EF_X)], [max(SP_EF_X)-sum(SP_EF_X)/len(SP_EF_X)]],
             fmt='o', color="C2") 

# plt.xlabel('Seed',  fontsize = 15)
plt.title('EF-X', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
plt.xticks([])
#plt.ylim([0,7])
plt.legend(loc='upper left')
plt.savefig('./Figures/EF_X_'+str(n)+'.png')
plt.close()






# barWidth = 0.15
# fig = plt.subplots(figsize =(12, 4))
# br1 = np.arange(len(seeds))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]

# plt.bar(br1, YS_nash_zeros, color =colors[0], width = barWidth, alpha=1,  
#         edgecolor =colors[0], label ='Yankee Swap')
# plt.bar(br2, RR_nash_zeros, color =colors[1], width = barWidth, alpha=1,  
#         edgecolor =colors[1], label ='Round Robin')
# plt.bar(br3, SP_nash_zeros, color =colors[2], width = barWidth, alpha=1,  
#         edgecolor =colors[2], label ='SPIRE algorithm')

# #plt.xlabel('Seed',  fontsize = 15)
# plt.ylabel('Nash Number of Zeros', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
# # plt.ylim([0,5])
# plt.legend()
# plt.savefig('./Figures/Nash_zeros_'+str(n)+'.png')
# plt.close()



# barWidth = 0.15
# fig = plt.subplots(figsize =(12, 4))
# br1 = np.arange(len(seeds))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]

# plt.bar(br1, YS_nash, color =colors[0], width = barWidth, alpha=1,  
#         edgecolor =colors[0], label ='Yankee Swap')
# plt.bar(br2, RR_nash, color =colors[1], width = barWidth, alpha=1,  
#         edgecolor =colors[1], label ='Round Robin')
# plt.bar(br3, SP_nash, color =colors[2], width = barWidth, alpha=1,  
#         edgecolor =colors[2], label ='SPIRE algorithm')

# plt.xlabel('Seed',  fontsize = 15)
# plt.ylabel('Nash Welfare', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)
# # plt.ylim([0,5])
# plt.legend()
# plt.savefig('./Figures/Nash_'+str(n)+'.png')
# plt.close()



# barWidth = 0.15
# fig = plt.subplots(figsize =(12, 4))
# br1 = np.arange(len(seeds))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]

# plt.bar(br1, YS_EF, color =colors[0], width = barWidth, alpha=1,  
#         edgecolor =colors[0], label ='Yankee Swap')
# plt.bar(br2, RR_EF, color =colors[1], width = barWidth, alpha=1,  
#         edgecolor =colors[1], label ='Round Robin')
# plt.bar(br3, SP_EF, color =colors[2], width = barWidth, alpha=1,  
#         edgecolor =colors[2], label ='SPIRE algorithm')

# plt.xlabel('Seed',  fontsize = 15)
# plt.ylabel('EF', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)

# plt.legend()
# plt.savefig('./Figures/EF_'+str(n)+'.png')
# plt.close()



# barWidth = 0.15
# fig = plt.subplots(figsize =(12, 4))
# br1 = np.arange(len(seeds))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]

# plt.bar(br1, YS_EF_1, color =colors[0], width = barWidth, alpha=1,  
#         edgecolor =colors[0], label ='Yankee Swap')
# plt.bar(br2, RR_EF_1, color =colors[1], width = barWidth, alpha=1,  
#         edgecolor =colors[1], label ='Round Robin')
# plt.bar(br3, SP_EF_1, color =colors[2], width = barWidth, alpha=1,  
#         edgecolor =colors[2], label ='SPIRE algorithm')

# plt.xlabel('Seed',  fontsize = 15)
# plt.ylabel('EF_1', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)

# plt.legend()
# plt.savefig('./Figures/EF_1_'+str(n)+'.png')
# plt.close()

# barWidth = 0.15
# fig = plt.subplots(figsize =(12, 4))
# br1 = np.arange(len(seeds))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]

# plt.bar(br1, YS_EF_X, color =colors[0], width = barWidth, alpha=1,  
#         edgecolor =colors[0], label ='Yankee Swap')
# plt.bar(br2, RR_EF_X, color =colors[1], width = barWidth, alpha=1,  
#         edgecolor =colors[1], label ='Round Robin')
# plt.bar(br3, SP_EF_X, color =colors[2], width = barWidth, alpha=1,  
#         edgecolor =colors[2], label ='SPIRE algorithm')

# plt.xlabel('Seed',  fontsize = 15)
# plt.ylabel('EF_X', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(seeds))],
#         seeds)

# plt.legend()
# plt.savefig('./Figures/EF_X_'+str(n)+'.png')
# plt.close()
