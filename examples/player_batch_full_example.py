import r6sapi
import asyncio
import json

async def run_rank(player_batch):
    ranks = await player_batch.get_rank(r6sapi.RankedRegions.EU)

    print("current season wins:")
    for player in player_batch:
        rank = ranks[player.id]
        
        print("  %s: %s" % (player.name, rank.wins))


async def run_ops(player_batch):
    ops = await player_batch.get_operator("ash")
    
    print("ash wins:")
    for player in player_batch:
        op = ops[player.id]
        print("  %s: %s" % (player.name, op.wins))

    await player_batch.load_all_operators()

    print("sledge kills:")
    for player in player_batch:
        op = await player.get_operator("sledge")
        print("  %s: %s" % (player.name, op.kills))


async def run_weapons(player_batch):
    player_weapons = await player_batch.load_weapons()

    print("submachine gun shots:")
    for player in player_batch:
        weapons = player_weapons[player.id]
        weapon = weapons[r6sapi.WeaponTypes.SUBMACHINE_GUN]

        print("  %s: %s" % (player.name, weapon.shots))


async def run_gamemodes(player_batch):
    player_gamemodes = await player_batch.load_gamemodes()

    print("defuse bomb wins:")
    for player in player_batch:
        gamemodes = player_gamemodes[player.id]
        gamemode = gamemodes["plantbomb"]

        print("  %s: %s" % (player.name, gamemode.wins))


async def run_general(player_batch):
    await player_batch.load_general()

    print("player deaths:")
    for player in player_batch:
        print("  %s: %s" % (player.name, player.deaths))


async def run_queues(player_batch):
    await player_batch.load_queues()

    print("casual wins:")
    for player in player_batch:
        print("  %s: %s" % (player.name, player.casual.wins))


async def run_terrohunt(player_batch):
    await player_batch.load_terrohunt()

    print("terrorist hunt kills:")
    for player in player_batch:
        print("  %s: %s" % (player.name, player.terrorist_hunt.kills))


async def run():
    auth = r6sapi.Auth("email", "password")

    player_batch = await auth.get_player_batch(names=["player_1", "player_2", "player_3"], platform=r6sapi.Platforms.UPLAY)
    
    await run_rank(player_batch)
    await run_ops(player_batch)
    await run_weapons(player_batch)
    await run_gamemodes(player_batch)
    await run_general(player_batch)
    await run_queues(player_batch)
    await run_terrohunt(player_batch)

    await auth.close()

asyncio.get_event_loop().run_until_complete(run())

