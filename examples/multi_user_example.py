import asyncio
import r6sapi as api

@asyncio.coroutine
def run():
    auth = api.Auth("email", "password")
    
    usernames = ["billy_yoyo", "another_user"]

    for username in usernames:
        player = yield from auth.get_player(username, api.Platforms.UPLAY)
        operator = yield from player.get_operator("sledge")
        print("player %s has %s kills with sledge" % (username, operator.kills))
        
asyncio.get_event_loop().run_until_complete(run())