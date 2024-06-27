from aiohttp import web
from typing import Callable, Awaitable


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
    return web.Response(text=f"hello, {name}")


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
