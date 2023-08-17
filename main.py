# %%
from agent_utils import Agent
from data_utils import Schedule
from item_utils import generate_items_from_schedule


items=generate_items_from_schedule('fall2023schedule.xlsx')
agent=Agent('student1',[items[0].item_id,  items[20].item_id, items[25].item_id,items[30].item_id,items[50].item_id, items[40].item_id], 4)
bundle=[items[0],items[20], items[25], items[30], items[24], items[40]]
print(agent.valuation(bundle))
print(agent.marginalContribution(bundle, items[50]))
