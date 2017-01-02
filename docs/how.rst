How It Works
============

Introduction
------------

Most of the API endpoints can be fairly easily retrieved by going on to the network tab and monitoring the requests sent. 
Your browser, as usual, will send a load of unnecessary headers with the request, and a quick bit of testing will show that the only two required are
the "Authorization" header and the "Ubi-AppId" header. (Also the request must have content-type set to application/json)


Experimenting
-------------

When you're logged in to your account on the website, your "Authorization" header looks like :code:`Ubi_v1 t=[token]` where :code:`[token]` is a load of random characters.
Your Ubi-AppId is a string of characters split by "-", so if we attempt to simply copy/paste these two and use them in our code, it will work but this type of token is called a "ticket"
and is only temporary. Eventually you'll get a response telling you your token is invalid, meaning you need to resend the information you used to recieve your ticket in the first place.


Logging In
----------

So clearly some sort of auth login logic is required, where you recieve a new ticket every time your current one runs out.
So if you monitor the requests sent when you log in, you'll see the very first request sent has the authorization header set to :code:`Basic [token]`.
This time :code:`[token]` appears to be constant, and the response you get from this endpoint gives you a valid ticket, along with some other things.
Great, now there's two things left to do: figure out how to generate this token from username/id and figure out how to get you appid


Generating The Token
--------------------

To do this I read through the javascript on the login page until I found the bit that converts your username and password in to a base64 number. 
This is actually, very simply, :code:`base64.encode(email + ":" + password)`. Nice and simple, this solves our first problem.


Getting the AppId
-----------------

Turns out the AppId doesn't seem to matter at all, after reading through the code I couldn't figure out where the AppId gets decided.
I believe it's generated server-side by ubisoft based on your IP, but either way I did manage to find a default AppId in the code, so unless one is specified, just using that one seems to work.


Conclusion
----------

That's basically the end of it, I convert the username and password in to a basic token, then every time a request gets an unauthorized I try and fetch a new one.
Then using the default appid, I can access any of the endpoints easily.