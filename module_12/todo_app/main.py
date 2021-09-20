import asyncio
from typing import Optional, Dict, Union

import aiohttp_jinja2
import aiohttp_session_flash
import jinja2
from aiohttp import web
from aiohttp_jinja2.helpers import url_for, _Context
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

# from module_12.todo_app.auth import auth_app
from aiomisc import entrypoint
from aiomisc.service import Profiler
from jinja2 import Environment

from module_12.todo_app.auth import (
    user_auth_middleware,
    login_required_middleware,
    create_auth_app,
)
from module_12.todo_app.db import init_app
from module_12.todo_app.settings import TEMPLATE_PATH, SECRET_KEY, DEBUG, STATIC_PATH
from module_12.todo_app.todo import index, create_todo_app

# from module_12.todo_app.todo import todo_app
_SUB_APPS_FACTORY = {
    "auth": create_auth_app,
    "todo": create_todo_app,
}
_REGISTERED_SUB_APPS = {key for key in _SUB_APPS_FACTORY}


def _sub_application(config=None):
    for app_name, app_factory in _SUB_APPS_FACTORY.items():
        yield app_name, app_factory(config)


async def request_context(request):
    return {"current_user": request.app.get("user")}


@jinja2.pass_context
def nested_url_for(
    context: _Context,
    __route_name: str,
    query_: Optional[Dict[str, str]] = None,
    **parts: Union[str, int],
):
    """Unforunatly jinja doesn't work with nested apps"""
    subapp_route = any(
        __route_name.startswith(subapp) for subapp in _REGISTERED_SUB_APPS
    )
    if subapp_route:
        # <editor-fold desc="jinja clean logic">
        # copied from original Jinja
        parts_clean: Dict[str, str] = {}
        for key in parts:
            val = parts[key]
            if isinstance(val, str):
                # if type is inherited from str expilict cast to str makes sense
                # if type is exactly str the operation is very fast
                val = str(val)
            elif type(val) is int:
                # int inherited classes like bool are forbidden
                val = str(val)
            else:
                raise TypeError(
                    "argument value should be str or int, "
                    "got {} -> [{}] {!r}".format(key, type(val), val)
                )
            parts_clean[key] = val
        # </editor-fold>
        app_name, *path = __route_name.split(".")
        path = ".".join(path)
        nested_app = context["app"][f"{app_name}_app"]
        url = nested_app.router[path].url_for(**parts_clean)
        if query_:
            url = url.with_query(query_)
        return url
    return url_for(context, __route_name, query_, **parts)


def create_app(config: dict, loop=None):
    secret_key = config.get("secret_key", SECRET_KEY)
    app = web.Application(
        loop=loop,
        middlewares=[
            session_middleware(EncryptedCookieStorage(secret_key)),
            aiohttp_session_flash.middleware,
            user_auth_middleware,
            login_required_middleware,
        ],
    )
    app["config"] = config
    init_app(app)
    env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
        context_processors=[
            aiohttp_session_flash.context_processor,
            request_context,
        ],
    )
    env.globals.update({"nested_url_for": nested_url_for, "url_for": url_for})

    app.add_routes([web.static("/static", STATIC_PATH, name="static")])
    app.add_routes(
        [
            web.get(
                "/",
                index,
                name="index",
            )
        ]
    )
    for name, sub_app in _sub_application(config=None):
        app.add_subapp(f"/{name}/", sub_app)
        # backward link
        sub_app["parent_app"] = app
        # forward link
        app[f"{name}_app"] = sub_app
    return app


if __name__ == "__main__":
    # <editor-fold desc="with profiler">
    # with entrypoint(Profiler(interval=0.1, top_results=10), debug=DEBUG) as et:
    #     app = _create_app(
    #         dict(db_name='todo_db'),
    #         loop=et,
    #     )
    #     web.run_app(app)
    # </editor-fold>
    # without profiler
    app = create_app(
        dict(db_name="todo_db"),
    )
    web.run_app(app)
