Getting Starting
================

Introduction
------------
r6sapi.py is a module for easily getting information from the unofficial rainbow six siege api. It allows you to get things such as a players rank and specific stats for operators, gamemodes and queues
The api requires authentication to process any api requests, so r6sapi requires your ubisoft login email and password.

Quick Example
-------------

.. code-block:: python

    import asyncio
    import r6sapi as api
    
    @asyncio.coroutine
    def run():
        auth = api.Auth("email", "password")
      
        player = yield from auth.get_player("billy_yoyo", api.Platforms.UPLAY)
        operator = yield from player.get_operator("sledge")
		
        print(operator.kills)
        
    asyncio.get_event_loop().run_until_complete(run())


License
-------
MIT
