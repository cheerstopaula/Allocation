# %%
from agent_utils import Agent
from item_utils import generate_items_from_schedule
from allocation_utils import Allocation


items=generate_items_from_schedule('fall2023schedule.xlsx')
agent1=Agent('student1',[items[0].item_id,  items[20].item_id, items[25].item_id,items[30].item_id,items[50].item_id, items[40].item_id], 4)
agent2=Agent('student2',[items[1].item_id,  items[33].item_id, items[43].item_id,items[45].item_id,items[49].item_id], 4)
agent3=Agent('student3',[items[0].item_id,  items[23].item_id, items[31].item_id,items[42].item_id,items[48].item_id], 4)
agents=[agent1, agent2,agent3]
bundle=[items[0],items[20], items[25], items[30], items[24], items[40]]
print(agent1.valuation(bundle))
print(agent1.marginalContribution(bundle, items[50]))
X=Allocation(items, agents, [])
print(X.allocation)
X.initialize_exchange_graph()
