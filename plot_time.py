import matplotlib.pyplot as plt
import random
import numpy as np

n=500
seeds=[0,1,2,3,4,5,6,7,8,9]


fig, axs = plt.subplots(2, 5, sharex=True,sharey=True,figsize =(16, 8))
for seed in seeds:
    data=np.load(f'YS_{n}_{seed}.npz')
    time_steps=data['time_steps']
    num_agents_involved=data['num_agents_involved']
    colors = np.diff(time_steps)
    area = (2 * colors)**3 
    axs[seed//5,seed%5].scatter(num_agents_involved[1:],np.diff(time_steps),s=area,c=colors, alpha=0.5)

fig.supylabel('Run time (e-03 seconds)')
fig.supxlabel('Number of Agents involved in the Path')
fig.suptitle('Time vs agents involved')
fig.tight_layout()
plt.savefig('./Figures/time_scatter_'+str(n)+'.png')
plt.close()



fig, axs = plt.subplots(2, 5, sharex=True,sharey=True,figsize =(16, 8))
for seed in seeds:
    data=np.load(f'YS_{n}_{seed}.npz')
    time_steps=data['time_steps']
    num_agents_involved=data['num_agents_involved']
    axs[seed//5,seed%5].plot(range(0,len(time_steps)),time_steps, alpha=0.5, linewidth=2)
    num_agents_involved=np.asarray(num_agents_involved)
    first_transfer_index=np.nonzero(num_agents_involved-1)[0][0]
    last_transfer_index=np.nonzero(num_agents_involved)[0][-1]
    axs[seed//5,seed%5].axvline(x = first_transfer_index, color = 'k', label = 'First transfer', linestyle='--')
    axs[seed//5,seed%5].axvline(x = last_transfer_index, color = 'k', label = 'Last transfer', linestyle='--')


fig.supylabel('Time (seconds)')
fig.supxlabel('Time step')
fig.suptitle('Time vs Time step')
fig.tight_layout()
plt.savefig('./Figures/time_'+str(n)+'.png')
plt.show()



fig, axs = plt.subplots(2, 5, sharex=True,sharey=True,figsize =(16, 8))
for seed in seeds:
    data=np.load(f'YS_{n}_{seed}.npz')
    time_steps=data['time_steps']
    num_agents_involved=data['num_agents_involved']
    axs[seed//5,seed%5].plot(range(0,len(time_steps)-1),np.diff(time_steps), alpha=0.5, linewidth=2)
    num_agents_involved=np.asarray(num_agents_involved)
    first_transfer_index=np.nonzero(num_agents_involved-1)[0][0]
    last_transfer_index=np.nonzero(num_agents_involved)[0][-1]
    axs[seed//5,seed%5].axvline(x = first_transfer_index, color = 'k', label = 'First transfer', linestyle='--', alpha=0.5)
    axs[seed//5,seed%5].axvline(x = last_transfer_index, color = 'k', label = 'Last transfer', linestyle='--', alpha=0.5)

fig.supylabel('Run time per time step (e-03 seconds)')
fig.supxlabel('Time step')
fig.suptitle('Run time per time step vs time')
fig.tight_layout()
plt.savefig('./Figures/runtime_'+str(n)+'.png')
plt.show()


