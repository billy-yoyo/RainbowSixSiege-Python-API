import asyncio
import r6sapi as api

async def run():
    auth = api.Auth("email", "password")

    player_batch = await auth.get_player_batch(["billy_yoyo", "another_user"], api.Platforms.UPLAY)
    ranks = await player_batch.get_rank(api.RankedRegions.EU)

    for player in player_batch:
        rank = ranks[player.id]

        print("player %s has %s mmr" % (player.name, rank.mmr))

    await auth.close()
        
asyncio.get_event_loop().run_until_complete(run())