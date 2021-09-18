import os

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiomisc import entrypoint
from aiomisc.service import Profiler

from module_12.todo_app.auth import auth_app
from module_12.todo_app.db import init_app
from module_12.todo_app.todo import todo_app

from aiohttp_session import setup, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

# in real world applications DEBUG_APP should be default False
_DEBUG = os.environ.get('DEBUG_APP', True)


def _create_app(config: dict, loop=None):
    app = web.Application(loop=loop)
    for key, value in config.items():
        app[key] = value
    directory_path = os.getcwd()
    init_app(app)
    aiohttp_jinja2.setup(
        app,
        # TODO check if works
        loader=jinja2.FileSystemLoader(
            os.path.join(directory_path, 'templates')
        )
    )
    app.add_subapp('/auth/', auth_app)
    app.add_subapp('/todo/', todo_app)
    # backward link
    auth_app['parent_app'] = app
    todo_app['parent_app'] = app
    # forward link
    app['auth_app'] = auth_app
    app['todo_app'] = todo_app
    # from aiohttp_debugtoolbar import toolbar_middleware_factory
    # aiohttp_debugtoolbar.setup(app)
    app.middlewares.append(
        session_middleware(EncryptedCookieStorage(app['secret_key']))
    )
    return app


if __name__ == '__main__':
    # adev runserver todo_app
    # app = create_app()
    # with entrypoint(Profiler(interval=0.1, top_results=10), debug=_DEBUG) as et:
    app = _create_app(
        dict(
            db_name='todo_db',
            secret_key=b"s}\x19\xf0\xa2\x0b\x86\x12\xb8\n'\xa38\x02Z\x1aB\x85>\xd6\x0b\x90%\x95\xe6\x7f\x17q\xa8\xd4^;",
        ),
        # loop=et,
    )

    web.run_app(app)
