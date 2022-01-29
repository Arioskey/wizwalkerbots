import asyncio
from time import time

from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter

from utils import decide_heal, finished_combat


async def attack(handler):
    await handler.wait_for_combat()

async def managed_combat(p, Total_Count, total):
    while True:
                # enter fight
        await p.goto(9725.8330078125, 944.7974853515625)
        print(f"{p.title} Initiating combat")
        handler = SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=0.35))
        start = time()

        # get a CombatHandler
      
        while True:
            try:
                asyncio.create_task(attack(handler))
            except (MemoryReadError, AttributeError, ValueError):
                continue
            break
        await asyncio.sleep(25)

        # combat has ended at this point
        await finished_combat(p)
        print(f"{p.title} Combat ended\n")
        
        Total_Count += 1
        print(f"The Total Amount of Runs for {p.title}: ", Total_Count)
        print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
        print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
        print("Average time per run: ", round(((time() - total) / 60) / Total_Count, 2), "minutes")
        await p.use_potion_if_needed(health_percent=10, mana_percent=21)




async def main(sprinter):
    # Register clients
    sprinter.get_new_clients()
    clients = sprinter.get_ordered_clients()
    p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
    for i, p in enumerate(clients, 1):
        p.title = "p" + str(i)

    # Hook activation
    for p in clients: 
        print(f"[{p.title}] Activating Hooks")
        await p.activate_hooks()
        await p.mouse_handler.activate_mouseless()

    Total_Count = 0
    total = time()

    combat_tasks = []
    #create combat tasks
    for p in clients:
        combat_tasks.append(asyncio.create_task(managed_combat(p, Total_Count, total)))
    while True:
        await asyncio.sleep(10)


# Error Handling
async def run():
  sprinter = WizSprinter() 

  try:
    await main(sprinter)
  except:
    import traceback

    traceback.print_exc()

  await sprinter.close()


# Start
if __name__ == "__main__":
    asyncio.run(run())
