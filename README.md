# r6sapi

r6sapi is an easy-to-use asynchronous API for rainbow six siege, written in python. To use it you'll need use your ubisoft email and password

### Documentation

http://rainbowsixsiege-python-api.readthedocs.io/en/latest/

### Quick Example

```py
import asyncio
import r6sapi as api

@asyncio.coroutine
def run():
    auth = api.Auth("email", "password")
    
    player = yield from auth.get_player("billy_yoyo", api.Platforms.UPLAY)
    operator = yield from player.get_operator("sledge")
    print(operator.kills)
    
asyncio.get_event_loop().run_until_complete(run())
```

### TODO

  -  implement terrorist hunt statistics

### License


MIT


