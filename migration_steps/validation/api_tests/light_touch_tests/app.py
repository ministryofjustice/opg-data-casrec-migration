# import asyncio
# import requests
# from aiohttp import ClientSession
#
#
# def get_session(base_url, user, password):
#     response = requests.get(base_url)
#     cookie = response.headers["Set-Cookie"]
#     xsrf = response.headers["X-XSRF-TOKEN"]
#     headers_dict = {"Cookie": cookie, "x-xsrf-token": xsrf}
#     data = {"email": user, "password": password}
#     with requests.Session() as s:
#         p = s.post(f"{base_url}/auth/login", data=data, headers=headers_dict)
#         print(f"Login returns: {p.status_code}")
#         return s, headers_dict, p.status_code
#
#
# def create_a_session(base_url, user, password):
#     sess, headers_dict, status_code = get_session(base_url, user, password)
#
#     session_info = {
#         "sess": sess,
#         "headers_dict": headers_dict,
#         "base_url": base_url,
#     }
#
#     return session_info
#
#
# base_url = 'http://localhost:8080'
# user = 'case.manager@opgtest.com'
# password = 'Password1'
#
# session_info = create_a_session(base_url, user, password)
#
#
# async def fetch(url, session):
#     async with session.get(url) as response:
#         return await response.read()
#
#
# async def run(r, authorised_session):
#     url = "http://localhost:8080/api/v1/clients/311"
#     tasks = []
#
#     # Fetch all responses within one Client session,
#     # keep connection alive for all requests.
#     async with authorised_session as session:
#         for i in range(r):
#             task = asyncio.ensure_future(fetch(url, session))
#             tasks.append(task)
#
#         responses = await asyncio.gather(*tasks)
#         # you now have all response bodies in this variable
#         print(responses)
#
#
# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(run(4, session_info["sess"]))
# loop.run_until_complete(future)


#!/usr/local/bin/python3.5
import asyncio
from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        print(response.status)
        return await response.read()

async def run(r):
    url = "https://google.co.uk"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses)


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(4))
loop.run_until_complete(future)