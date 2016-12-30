# r6sapi

r6sapi is an easy-to-use asynchronous API for rainbow six siege, written in python. To use it you'll need to obtain your `Ubi-AppId` and your `Basic Authorization`, I'll go through step-by-step how to get these:

  - Go to https://game-rainbow6.ubi.com/en-us/home
  - Open up your inspector, and go to the network tab, enable only XHR
  - Clear your network tab so it's easier to see when you log in
  - Now log in on the website
  - Loads of requests probably just popped up, so scroll to the top and look for the first `POST` request to `https://connect.ubi.com/ubiservices/v2/profiles/sessions`
  - Look at the request headers for this request, you should see one header called `Ubi-AppId`, copy this and remember it. 
  - You should also see one called `Authorization`, the value for this should look like `Basic token` where `token` is just a load of random characters. If it doesn't start with `Basic` you're looking at the wrong request. Once you've found the correct header, copy just the `token` part and remember it.

Now you can use the API, just use the `token` part you remembered as the token parameter and the `Ubi-AppId` part you remembers as the appid parameter when you create your Auth object, e.g.:
```py
auth = Auth("token", "appid")
```

### Quick Example

```py
import asyncio
import r6sapi as api

@asyncio.coroutine
def run():
    auth = api.Auth("token", "appid")
    
    player = yield from auth.get_player("billy_yoyo", api.Platforms.UPLAY)
    operator = yield from player.get_operator("sledge")
    print(operator.kills)
    
asyncio.get_event_loop().run_until_complete(run())
```

### TODO

  -  document everything
  -  handle error messages
  -  implement terrorist hunt statistics

### License


MIT


