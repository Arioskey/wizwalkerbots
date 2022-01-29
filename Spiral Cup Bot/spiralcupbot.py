import asyncio
from time import time

from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from wizwalker.extensions.scripting.utils import teleport_to_friend_from_list

from utils import decide_heal, spiral_start, teleport_to_npc, go_through_dialog

doors = [
    XYZ(-1498.0885009765625, -1.1095490455627441, 20.9642333984375),
    XYZ(-1021.3975830078125, -1076.1234130859375, 82.51651000976562),
    XYZ(1033.3948974609375, -1072.616455078125, 82.51416015625),
    XYZ(1490.5804443359375, 14.138046264648438, 20.962921142578125)
    ]

class SpiralError(Exception):
    """A Spiral Cup Error"""
    
async def attack(handler):
    try:
        print("initialising combat")
        await handler.wait_for_combat()
    except ValueError:
        print("ValueError get")
        await attack(handler)
    
async def attack_mob(p):
    await p.send_key(Keycode.D, 0.1)
    await p.wait_for_zone_change()
    handler = SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=0.40))
    await p.tp_to_closest_mob()
    await asyncio.sleep(2)

    await attack(handler)
        
    #await go_through_dialog(p)
    await p.teleport(XYZ(619.8995361328125, 1484.72314453125, 0.20001220703125))
    await p.wait_for_zone_change()
    
async def speak_to_ben(p):
    await teleport_to_npc(p, "SC-GiantTower-NPC01")
    await p.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1)
    if await p.is_in_dialog():
        await go_through_dialog(p)

    
async def spiral_cup(p, clients):
    counter = 1
    
    while True:
        if len(await p.get_base_entities_with_name("PA_SpiralCupGauntlet")) == 0:
            #change <name> to your friend's name that is afk spinning at gauntlet house
            #e.g. teleport_to_friend_from_list(p, name="James StormSmith")
            await teleport_to_friend_from_list(p, name="James StormSmith")
            await p.wait_for_zone_change()
        await spiral_start(p)
        await speak_to_ben(p)
        for i, door in enumerate(doors):
            await decide_heal(p)
            await p.teleport(door)
            await attack_mob(p)
            if i != 3:
                await speak_to_ben(p)
        await go_through_dialog(p) 
        print(f"{p.title} finished dungeon - {counter}")
        await decide_heal(p)
        counter += 1
        
        



# Error Handling
async def run():
    sprinter = WizSprinter() # Define sprinter
    try:
# Register clients
        sprinter.get_new_clients()
        clients = sprinter.get_ordered_clients()[:2] #<---- Change this number based on how many 
                                                     #clients you are playing with
                                                     #excluding the 'friend' client
                                                     #e.g. for 3 clients fighting do [:3]
        p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
        for i, p in enumerate(clients, 1):
            p.title = "p" + str(i)

        # Hook activation
        for p in clients:
            print(f"[{p.title}] Activating Hooks")
            await p.activate_hooks()
            await p.mouse_handler.activate_mouseless()
            for i in range(3):
                await p.send_key(Keycode.F, 0.1)
        Total_Count = 0
        total = time()
        combat_tasks = []
        for p in clients:
            combat_tasks.append(asyncio.create_task(spiral_cup(p, clients)))
        while True:
            await asyncio.sleep(1000)
    except:
        import traceback

        traceback.print_exc()

        await sprinter.close()


# Start
if __name__ == "__main__":
    asyncio.run(run())
