import asyncio
import r6sapi as api

async def run():
    auth = api.Auth("email", "password")
    
    player = await auth.get_player("billy_yoyo", api.Platforms.UPLAY)
    operator = await player.get_operator("sledge")

    print(operator.kills)

    await auth.close()
    
asyncio.get_event_loop().run_until_complete(run())