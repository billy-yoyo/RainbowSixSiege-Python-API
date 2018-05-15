import asyncio
import r6sapi as api

@asyncio.coroutine
def run():
    auth = api.Auth("email", "password")
    
    player = yield from auth.get_player("billy_yoyo", api.Platforms.UPLAY)
    operator = yield from player.get_operator("sledge")
    print(operator.kills)
    
asyncio.get_event_loop().run_until_complete(run())