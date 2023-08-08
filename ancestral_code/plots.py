# %%
import pandas as pd
import numpy as np
from inputs import  get_schedule, genMany
from allocation_utils import YankeeSwap,RoundRobin,SpireAlloc
from metrics import getNash, getUtilitarian
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

def plot_instances(classes, topics,instructors,numClasses,schedule,slots, n,nseeds):
    utilSP=[]
    utilRR=[]
    utilYS=[]
    nashSP=[]
    nashRR=[]
    nashYS=[]
    nashZerosSP=[]
    nashZerosRR=[]
    nashZerosYS=[]
    count_util_RR=0
    count_util_YS=0
    count_nash_RR=0
    count_nash_YS=0

    for i in range(nseeds):
        students = genMany(n, topics, instructors, numClasses,i)
        spire = SpireAlloc([3 for x in students], students, [x for x in students], [3 for y in students[0]])
        ## Three students,3 classes, student 1: wants a,b, 2: wants a,c, 3: wants a,c
        roundRobin = RoundRobin([3 for x in students], students, [x for x in students], list(classes["Enrl Capacity"]),
                                slots)
        yankee = YankeeSwap([3 for x in students], students, list(classes["Enrl Capacity"]), slots)

        util_SP=getUtilitarian(spire)
        util_RR=getUtilitarian(roundRobin)
        util_YS=getUtilitarian(yankee)

        utilSP.append(util_SP)
        utilRR.append(util_RR)
        utilYS.append(util_YS)

        nash_SP=np.log(float(getNash(spire)[1]))
        nash_RR=np.log(float(getNash(roundRobin)[1]))
        nash_YS=np.log(float(getNash(yankee)[1]))

        nashSP.append(nash_SP)
        nashRR.append(nash_RR)
        nashYS.append(nash_YS)

        nashZerosSP.append(getNash(spire)[0])
        nashZerosRR.append(getNash(roundRobin)[0])
        nashZerosYS.append(getNash(yankee)[0])

        if util_SP>util_RR:
            count_util_RR+=1

        if util_SP>util_YS:
            count_util_YS+=1

        if nash_SP>nash_RR:
            count_nash_RR+=1

        if nash_SP>nash_YS:
            count_nash_YS+=1


    x=range(nseeds)
    x=np.array(x)

    plt.plot(x, utilSP, color='C0', label='SPIRE')
    plt.plot(x, utilRR, color='C1', label='Round Robin')
    plt.plot(x, utilYS, color='C2', label='Yankee Swap')
    plt.legend()
    textstr = '\n'.join((
        f"SPIRE exceeding RR: {count_util_RR}/{nseeds}",
        f"SPIRE exceeding YS: {count_util_YS}/{nseeds}"))

    plt.text(0.5, 2.47, textstr, fontsize = 10, bbox = dict(facecolor = 'white', alpha = 0.5))
    plt.xlim([0,nseeds-1])
    plt.xticks(x)
    plt.xlabel('Seed')
    plt.ylabel('Utilitarian Welfare')
    plt.title('Utilitarian Social Welfare')
    plt.gcf().set_size_inches(14, 4)
    plt.savefig(f"util_{nseeds}.png")
    plt.close()

    plt.plot(x, nashSP, color='C0', label='SPIRE')
    plt.plot(x, nashRR, color='C1', label='Round Robin')
    plt.plot(x, nashYS, color='C2', label='Yankee Swap')
    plt.legend()
    textstr = '\n'.join((
        f"SPIRE exceeding RR: {count_nash_RR}/{nseeds}",
        f"SPIRE exceeding YS: {count_nash_YS}/{nseeds}"))

    plt.text(0.5, 43, textstr, fontsize = 10, bbox = dict(facecolor = 'white', alpha = 0.5))
    plt.xlim([0,nseeds-1])
    plt.xticks(x)
    plt.xlabel('Seed')
    plt.ylabel('Nash Welfare Logarithm')
    plt.title('Nash Social Welfare')
    plt.gcf().set_size_inches(14, 4)
    plt.savefig(f"nash_{nseeds}.png")
    plt.close()
    plt.close()

    plt.plot(x, nashZerosSP, color='C0', label='SPIRE')
    plt.plot(x, nashZerosRR, color='C1', label='Round Robin')
    plt.plot(x, nashZerosYS, color='C2', label='Yankee Swap')
    plt.legend()
    plt.xlim([0,nseeds-1])
    plt.xticks(x)
    plt.xlabel('Seed')
    plt.ylabel('Number of Zeros')
    plt.title('Nash Social Welfare')
    plt.gcf().set_size_inches(14, 4)
    plt.savefig(f"nashZeros_{nseeds}.png")
    plt.close()

# %%