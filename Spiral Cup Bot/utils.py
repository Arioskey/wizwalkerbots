import asyncio

from wizwalker import XYZ
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter.sprinty_client import MemoryReadError

async def go_through_dialog(client):
    while not await client.is_in_dialog():
        await asyncio.sleep(0.1)
    while await client.is_in_dialog():
        await client.send_key(Keycode.SPACEBAR, 0.1)

async def safe_tp_to_mana(client):
  try:
    await client.tp_to_closest_mana_wisp()
  except MemoryReadError:
    await safe_tp_to_mana(client)
async def safe_tp_to_health(client):
  try:
    await client.tp_to_closest_health_wisp()
  except MemoryReadError:
    await safe_tp_to_health(client)

async def decide_heal(client):
    while True:
        while not await client.is_in_dialog():
            while await client.stats.current_hitpoints() < await client.stats.max_hitpoints():
                await safe_tp_to_health(client)
                await asyncio.sleep(0.4)
            #while await client.stats.current_mana() < await client.stats.max_mana():
             #   await safe_tp_to_mana(client)
              #  await asyncio.sleep(0.4)
            return
        else:
            await go_through_dialog(client)
            continue
        
async def spiral_start(client):
    for entity in await client.get_base_entities_with_name("PA_SpiralCupGauntlet"):
        spiral_loc = await entity.location()
    await client.teleport(spiral_loc)
    await asyncio.sleep(1.25)
    if not await client.is_in_npc_range():
        try:
            await client.goto(spiral_loc.x, spiral_loc.y)
        except ZeroDivisionError:
            pass
    while not await client.is_in_npc_range():
        continue
    await client.send_key(Keycode.X, 0.1)
    await client.wait_for_zone_change()
        
async def teleport_to_npc(client, npc_str: str):
    for entity in await client.get_base_entities_with_name(npc_str):
        npc = await entity.location()
    await client.teleport(npc)
    while not await client.is_in_npc_range():
        pass


