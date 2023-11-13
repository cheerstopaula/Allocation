from allocation.agent_functions import Agent, gen_random_agents
from allocation.item_functions import generate_items_from_schedule
from allocation.allocation_functions import yankee_swap, SPIRE_algorithm, round_robin
from allocation.metric_functions import utilitarian_welfare, nash_welfare, EF, leximin
import matplotlib.pyplot as plt
import random
import numpy as np
import seaborn as sns



items=generate_items_from_schedule('fall2023schedule-2.xlsx')
YS_leximin=[]
RR_leximin=[]
SP_leximin=[]


seeds=[0,1,2,3,4,5,6,7,8,9]
seeds=[0,1,2]
n=1000

for seed in seeds:
    random.seed(seed)
    np.random.seed(seed)

    agents=gen_random_agents(n,items)
    data=np.load(f'YS_{n}_{seed}.npz')
    X=data['X']
    YS_lex=leximin(X,agents,items)
    (nYS, bins2, patches) = plt.hist(YS_lex, bins=[0,1,2,3,4,5,6,7,8,9,10,11])
    plt.close()
    print(YS_lex)
    print(nYS)
    YS_leximin.append(YS_lex)
    X=round_robin(agents,items)
    RR_lex=leximin(X,agents,items)
    RR_leximin.append(RR_lex)
    X=SPIRE_algorithm(agents,items)
    SP_lex=leximin(X,agents,items)
    SP_leximin.append(SP_lex)

YS_lex_mean=sum(np.asarray(YS_leximin))/len(seeds)
RR_lex_mean=sum(np.asarray(RR_leximin))/len(seeds)
SP_lex_mean=sum(np.asarray(SP_leximin))/len(seeds)

colors_list = ["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
            "#DEBB9B", "#FAB0E4", "#CFCFCF", "#FFFEA3", "#B9F2F0"]
colors=colors_list[:3]

(nYS, bins2, patches) = plt.hist(YS_lex_mean, bins=[0,1,2,3,4,5,6,7,8,9,10,11])
(nRR, bins2, patches) = plt.hist(RR_lex_mean, bins=[0,1,2,3,4,5,6,7,8,9,10,11])
(nSP, bins2, patches) = plt.hist(SP_lex_mean, bins=[0,1,2,3,4,5,6,7,8,9,10,11])
plt.close()

plt.figure(figsize=(10,6))
plt.hist([YS_lex_mean,RR_lex_mean,SP_lex_mean], bins=[0,1,2,3,4,5,6,7,8,9,10], alpha=0.7,  rwidth=0.7,
         histtype ='bar',
         color = colors,
         label = ['Yanyee Swap','Round Robin', 'SPIRE algorithm'])
         
plt.xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5],[0,1,2,3,4,5,6,7,8,9,10])

plt.plot([0.75,1.75,2.75,3.75,4.75,5.75,6.75,7.75,8.75,9.75,10.75],nSP, color='C2', linewidth=3, alpha=0.65)
plt.plot([0.5, 1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5],nRR, color='C1', linewidth=3, alpha=0.65)
plt.plot([0.25, 1.25,2.25,3.25,4.25,5.25,6.25,7.25,8.25,9.25,10.25],nYS, color='C0', linewidth=3, alpha=0.65)
plt.legend(prop ={'size': 12})
plt.title('Leximin Vector Histogram, N='+str(n),
          fontweight = "bold")
plt.xlabel('Number of assigned classes', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.savefig('./Figures/leximin_hist_'+str(n)+'.png')
plt.close()


(nYS, bins2, patches) = plt.hist(YS_lex_mean, bins=[0,1,2,3,4,5,6,7,8,9,10,11], cumulative=True)
(nRR, bins2, patches) = plt.hist(RR_lex_mean, bins=[0,1,2,3,4,5,6,7,8,9,10,11], cumulative=True)
(nSP, bins2, patches) = plt.hist(SP_lex_mean, bins=[0,1,2,3,4,5,6,7,8,9,10,11], cumulative=True)
plt.close()

plt.figure(figsize=(10,6))
plt.hist([YS_lex_mean,RR_lex_mean,SP_lex_mean], bins=[0,1,2,3,4,5,6,7,8,9,10],  alpha=0.4, rwidth=0.7,
         histtype ='bar',
         color = colors,
         cumulative=True,
         #label = ['Yanyee Swap','Round Robin', 'SPIRE algorithm']
         )
plt.xticks([1,2,3,4,5,6,7,8,9,10])

plt.hist([YS_lex_mean,RR_lex_mean,SP_lex_mean], bins=[0,1,2,3,4,5,6,7,8,9,10],  rwidth=0.7,
         histtype ='bar',
         color = colors,
         #cumulative=True,
         label = ['Yanyee Swap','Round Robin', 'SPIRE algorithm'])
plt.xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5],[0,1,2,3,4,5,6,7,8,9,10])

plt.plot([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5],nSP, color='C2', linewidth=3, alpha=0.65)
plt.plot([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5],nRR, color='C1', linewidth=3, alpha=0.65)
plt.plot([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5],nYS, color='C0', linewidth=3, alpha=0.65)

# # plt.axvline(sum(YS_leximin)/len(YS_leximin), color='C0', linestyle='dashed', linewidth=1)
# # plt.axvline(sum(RR_leximin)/len(RR_leximin), color='C1', linestyle='dashed', linewidth=1)
# # plt.axvline(sum(SP_leximin)/len(SP_leximin), color='C2', linestyle='dashed', linewidth=1)

# plt.axvline(YS_leximin[int(len(YS_leximin)/2)]+0.5, color=colors[0], linestyle='dashed', linewidth=1.6, label='YS Median')
# plt.axvline(RR_leximin[int(len(RR_leximin)/2)]+0.5, color=colors[1], linestyle='dashed', linewidth=1.7, label='RR Median')
# plt.axvline(SP_leximin[int(len(SP_leximin)/2)]+0.5, color=colors[2], linestyle='dashed', linewidth=1.5, label='SP Median')

plt.legend(prop ={'size': 12})
plt.title('Leximin Vector Cumulative, N='+str(n),
          fontweight = "bold")
plt.xlabel('Number of assigned classes', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
#plt.show()
plt.savefig('./Figures/leximin_cumulative_'+str(n)+'.png')
plt.close()




# ##Plotting leximin vector

# #Define color palette
# #colors = sns.color_palette("husl", 9)[4::2]
# # colors.append(sns.color_palette("husl", 9)[4::2])
# colors=sns.color_palette("Set3",10)[4:7]
# colors_list = ["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
#             "#DEBB9B", "#FAB0E4", "#CFCFCF", "#FFFEA3", "#B9F2F0"]
# colors=colors_list[:3]
# #colors=sns.color_palette("flare",3)

# #Plot histogram
# (nYS, bins2, patches) = plt.hist(YS_leximin, bins=[0,1,2,3,4,5,6,7,8,9,10])
# (nRR, bins2, patches) = plt.hist(RR_leximin, bins=[0,1,2,3,4,5,6,7,8,9,10])
# (nSP, bins2, patches) = plt.hist(SP_leximin, bins=[0,1,2,3,4,5,6,7,8,9,10])
# plt.close()

# plt.figure(figsize=(10,6))
# plt.hist([YS_leximin,RR_leximin,SP_leximin], bins=[0,1,2,3,4,5,6,7,8,9,10], alpha=0.7,  rwidth=0.7,
#          histtype ='bar',
#          color = colors,
#          label = ['Yanyee Swap','Round Robin', 'SPIRE algorithm'])
# plt.xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5],[0,1,2,3,4,5,6,7,8,9,10])

# plt.plot([0.75,1.75,2.75,3.75,4.75,5.75,6.75,7.75,8.75,9.75],nSP, color='C2', linewidth=3, alpha=0.65)
# plt.plot([0.5, 1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5],nRR, color='C1', linewidth=3, alpha=0.65)
# plt.plot([0.25, 1.25,2.25,3.25,4.25,5.25,6.25,7.25,8.25,9.25],nYS, color='C0', linewidth=3, alpha=0.65)
# plt.axvline(YS_leximin[int(len(YS_leximin)/2)]+0.5, color=colors[0], linestyle='dashed', linewidth=1.6, label='YS Median')
# plt.axvline(RR_leximin[int(len(RR_leximin)/2)]+0.5, color=colors[1], linestyle='dashed', linewidth=1.7, label='RR Median')
# plt.axvline(SP_leximin[int(len(SP_leximin)/2)]+0.5, color=colors[2], linestyle='dashed', linewidth=1.5, label='SP Median')

# plt.legend(prop ={'size': 12})
# plt.title('Leximin Vector Histogram, N='+str(n),
#           fontweight = "bold")
# plt.xlabel('Number of assigned classes', fontsize=14)
# plt.ylabel('Frequency', fontsize=14)
# plt.savefig('./Figures/leximin_hist_'+str(n)+'.png')
# #plt.show()


# #Plot cumulative 
# (nYS, bins2, patches) = plt.hist(YS_leximin, bins=[0,1,2,3,4,5,6,7,8,9,10], cumulative=True)
# (nRR, bins2, patches) = plt.hist(RR_leximin, bins=[0,1,2,3,4,5,6,7,8,9,10], cumulative=True)
# (nSP, bins2, patches) = plt.hist(SP_leximin, bins=[0,1,2,3,4,5,6,7,8,9,10], cumulative=True)
# plt.close()

# plt.figure(figsize=(10,6))
# plt.hist([YS_leximin,RR_leximin,SP_leximin], bins=[0,1,2,3,4,5,6,7,8,9,10],  alpha=0.4, rwidth=0.7,
#          histtype ='bar',
#          color = colors,
#          cumulative=True,
#          #label = ['Yanyee Swap','Round Robin', 'SPIRE algorithm']
#          )
# #plt.xticks([1,2,3,4,5,6,7,8,9,10])

# plt.hist([YS_leximin,RR_leximin,SP_leximin], bins=[0,1,2,3,4,5,6,7,8,9,10],  rwidth=0.7,
#          histtype ='bar',
#          color = colors,
#          #cumulative=True,
#          label = ['Yanyee Swap','Round Robin', 'SPIRE algorithm'])
# plt.xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5],[0,1,2,3,4,5,6,7,8,9,10])

# plt.plot([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5],nSP, color='C2', linewidth=3, alpha=0.65)
# plt.plot([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5],nRR, color='C1', linewidth=3, alpha=0.65)
# plt.plot([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5],nYS, color='C0', linewidth=3, alpha=0.65)

# # plt.axvline(sum(YS_leximin)/len(YS_leximin), color='C0', linestyle='dashed', linewidth=1)
# # plt.axvline(sum(RR_leximin)/len(RR_leximin), color='C1', linestyle='dashed', linewidth=1)
# # plt.axvline(sum(SP_leximin)/len(SP_leximin), color='C2', linestyle='dashed', linewidth=1)

# plt.axvline(YS_leximin[int(len(YS_leximin)/2)]+0.5, color=colors[0], linestyle='dashed', linewidth=1.6, label='YS Median')
# plt.axvline(RR_leximin[int(len(RR_leximin)/2)]+0.5, color=colors[1], linestyle='dashed', linewidth=1.7, label='RR Median')
# plt.axvline(SP_leximin[int(len(SP_leximin)/2)]+0.5, color=colors[2], linestyle='dashed', linewidth=1.5, label='SP Median')

# plt.legend(prop ={'size': 12})
# plt.title('Leximin Vector Cumulative, N='+str(n),
#           fontweight = "bold")
# plt.xlabel('Number of assigned classes', fontsize=14)
# plt.ylabel('Frequency', fontsize=14)
# #plt.show()
# plt.savefig('./Figures/leximin_cumulative_'+str(n)+'.png')
# # plt.close()




