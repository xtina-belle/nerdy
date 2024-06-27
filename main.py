import os
from typing import Callable, Awaitable

from aiohttp import web
import redis


r = redis.Redis(host=os.environ.get("REDISHOST"), port=os.environ.get("REDISPORT"),
                password=os.environ.get("REDISPASSWORD"), username=os.environ.get("REDISUSER"))

routes = web.RouteTableDef()


@web.middleware
async def check_header(
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
) -> web.StreamResponse:
    amit = request.headers.get("Amit", "")
    if amit != "Sexy":
        return web.Response(text="required header is missing", status=400)
    return await handler(request)


@routes.get("/")
async def handle(request: web.Request):
    return web.Response(text="you've got me", status=200)


@routes.post("/hello")
async def greet_user(request: web.Request) -> web.Response:
    # get data from the BODY of request
    data = await request.post()
    name = data.get("name", "")
    city = r.get("Bahamas").decode("utf-8")
    return web.Response(text=f"hello, {name} in {city}")


@routes.get("/{username}")
async def greet_user(request: web.Request) -> web.Response:
    user = request.match_info.get("username", "")
    # get from params
    page_num = request.rel_url.query.get("page", "")
    return web.Response(text=f"Hello, {user}, {page_num}")


if __name__ == "__main__":
    app = web.Application(middlewares=[check_header])

    app.add_routes(routes)
    web.run_app(app)
