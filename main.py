# %%
from agent_utils import Agent
from item_utils import generate_items_from_schedule
from allocation_utils import Allocation


items=generate_items_from_schedule('fall2023schedule.xlsx')
# agent1=Agent('student1',[items[0].item_id,  items[20].item_id, items[30].item_id,items[25].item_id,items[40].item_id, items[50].item_id], 10)
# agent2=Agent('student2',[items[1].item_id,  items[20].item_id, items[30].item_id,items[45].item_id,items[48].item_id, items[50].item_id], 10)
# agent3=Agent('student3',[items[0].item_id,  items[20].item_id, items[30].item_id,items[45].item_id,items[48].item_id, items[50].item_id], 10)
agent1=Agent('student1',[items[0].item_id,  items[20].item_id, items[30].item_id,items[25].item_id,items[40].item_id,[50]], 10)
agent2=Agent('student2',[items[1].item_id,  items[20].item_id, items[30].item_id,items[25].item_id], 10)
agent3=Agent('student3',[items[0].item_id,  items[20].item_id, items[30].item_id,items[40].item_id], 10)
agents=[agent1, agent2,agent3]
items2=[items[0], items[1],items[20],items[25], items[30], items[40]]
bundle=[items[0], items[20]]
print(agent1.exchange_contribution(bundle, items[20], items[40]))

#for i in range(len(items2)):
#    print(items2[i].item_id)
#    print(items2[i].timeslot)
#X=Allocation(items2, agents, [[items[1],items[40]],[items[0],items[20]],[items[25]],[items[30]]])
#print(X.allocation)

#print(X.find_owner(items[0]))
