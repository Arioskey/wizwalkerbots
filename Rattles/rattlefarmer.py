import asyncio
from time import time

from wizwalker import XYZ
from wizwalker.errors import MemoryReadError
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter

from utils import decide_heal, logout_and_in, finished_combat


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

        #await p.send_key(Keycode.PAGE_DOWN, 0.1)

    Total_Count = 0
    total = time()
    combat_tasks = []
    for p in clients:
        combat_tasks.append(asyncio.create_task(managed_combat(p, Total_Count, total)))
    #await asyncio.sleep(500000000)
    while True:
        await asyncio.sleep(10)

async def attack(handler):
    await handler.wait_for_combat()

async def managed_combat(p, Total_Count, total):
    while True:
        start = time()

        
        await asyncio.sleep(1)
        await decide_heal(p)
        # Entering Boss Fight
        await p.teleport(XYZ(-16543.912109375, 19097.306640625, False))
        await p.send_key(Keycode.D, 0.1)
        await p.wait_for_zone_change()

        # Initial battle starter
        await p.tp_to_closest_mob()
        await p.send_key(Keycode.W, 0.1)
        

        # Battle:
        handler = SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=0.1))
        start = time()
        # enter fight
        # get a CombatHandler
        print(f"{p.title} Initiating combat\n")
        combat_task = []
        while True:
            try:
                combat_task.append(asyncio.create_task(attack(handler)))
                
                
            except (MemoryReadError, AttributeError):
                await asyncio.sleep(5)
            except ValueError:
                continue
            break
        await asyncio.sleep(25)
        await finished_combat(p)

        print(f"{p.title} Combat ended\n")
        # combat has ended at this point
        Total_Count += 1
        print(f"The Total Amount of Runs for {p.title}: ", Total_Count)
        print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
        print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
        print("Average time per run: ", round(((time() - total) / 60) / Total_Count, 2), "minutes")
        print()




# Error Handling
async def run():
  sprinter = WizSprinter() # Define thingys

  try:
    await main(sprinter)
  except:
    import traceback

    traceback.print_exc()

  await sprinter.close()

def run2():
    run()

# Start
if __name__ == "__main__":
    asyncio.run(run())
