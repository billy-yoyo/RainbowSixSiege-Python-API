# r6sapi

r6sapi is an easy-to-use asynchronous API for rainbow six siege, written in python. To use it you'll need use your ubisoft email and password

### Installation

To install this module, simply run

    pip install r6sapi

### Documentation

http://rainbowsixsiege-python-api.readthedocs.io/en/latest/

### Quick Example

```py
import asyncio
import r6sapi as api

async def run():
    auth = api.Auth("email", "password")
    
    player = await auth.get_player("billy_yoyo", api.Platforms.UPLAY)
    operator = await player.get_operator("sledge")
    print(operator.kills)

    await auth.close()
    
asyncio.get_event_loop().run_until_complete(run())
```

### TODO

  -  implement the ability to fetch data for multiple players at once in order to reduce the amount of api calls required when handling lots of players simultaneously.

### License


MIT


