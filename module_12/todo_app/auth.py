from string import hexdigits

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from aiohttp_session_flash import flash
from asgiref.sync import sync_to_async
from bson import ObjectId
from passlib.hash import pbkdf2_sha256
from passlib.utils import getrandstr, rng
from pymongo.collection import Collection


routes = web.RouteTableDef()


# <editor-fold desc="sync_to_async functions">
@sync_to_async
def _get_random_str(number_ch=10):
    return getrandstr(rng, charset=hexdigits, count=number_ch)


@sync_to_async
def _hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


@sync_to_async
def _verify_password(password: str, hashed_password: str) -> bool:
    try:
        return pbkdf2_sha256.verify(password, hashed_password)
    except ValueError:
        pass
    return False


@sync_to_async
def insert_user(db, user_dict):
    return db.user.insert_one(user_dict)


@sync_to_async
def get_user_by_id(db, user_id: str):
    query = {"_id": ObjectId(user_id)}
    return db.user.find_one(query)


@sync_to_async
def get_user_by_name(db, username: str):
    query = {"username": username}
    return db.user.find_one(query)


@sync_to_async
def insert_todos(db, collection_name):
    user_todo: Collection = getattr(db, collection_name)
    return user_todo.insert_many(_example_todos())


@sync_to_async
def user_exists(db, username) -> bool:
    user = db.user.find_one({"username": username})
    return user is not None


# </editor-fold>


# <editor-fold desc="helper functions">
def _example_todos():
    return [
        dict(title="Register in App", done=True, priority=0),
        dict(
            title="Plan next week",
            done=False,
            description="You doing great",
            priority=1,
        ),
        dict(
            title="Sleep more well",
            done=False,
            description="Sleep is very important for your health",
            priority=3,
        ),
        dict(title="Buy healthy food", done=False, priority=4),
    ]


# </editor-fold>


# <editor-fold desc="views">
@routes.post("/register", name="register")
@routes.get("/register", name="register")
@aiohttp_jinja2.template("auth/register.html")
async def register(request):
    if request.method == "GET":
        # already rendered see template decorator
        return

    db = request.config_dict["db"]
    data = await request.post()
    username = data["username"]
    password = data["password"]
    error = None

    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."

    if username:
        exists = await user_exists(db, username)
        if exists:
            error = "Already registered."

    flash(request, error)
    if error is not None:
        # show errors
        return

    rand_str = await _get_random_str()
    collection_name = f"todo_list_{username}_{rand_str}"
    user_dict = dict(
        username=username,
        password=await _hash_password(password),
        todo_collection=collection_name,
    )
    await insert_user(db, user_dict)
    await insert_todos(db, collection_name)
    location = request.app.router["login"].url_for()
    return web.HTTPFound(location=location)


@routes.post("/login", name="login")
@routes.get("/login", name="login")
@aiohttp_jinja2.template("auth/login.html")
async def login(request):
    if request.method == "GET":
        # already rendered
        return
    data = await request.post()
    username = data["username"]
    password = data["password"]
    db = request.config_dict["db"]
    error = None
    user = await get_user_by_name(db, username)
    if user is None:
        error = "Incorrect username."
    else:
        correct_password = await _verify_password(password, user["password"])
        if not correct_password:
            error = "Incorrect password."

    if error is None:
        session = await get_session(request)
        session.clear()
        session["user_id"] = str(user["_id"])
        parent_app = request.app["parent_app"]
        location = parent_app["todo_app"].router["index"].url_for()
        return web.HTTPFound(location=location)

    flash(request, error)
    location = request.app.router["login"].url_for()
    return web.HTTPFound(location=location)


@routes.post("/logout", name="logout")
@routes.get("/logout", name="logout")
async def logout(request):
    # TODO Check if working
    session = await get_session(request)
    session.clear()
    request.app.pop("user", None)
    request.app["parent_app"].pop("user", None)
    location = request.app.router["login"].url_for()
    return web.HTTPFound(location=location)


# </editor-fold>


# <editor-fold desc="middleware for apps">
@web.middleware
async def user_auth_middleware(request, handler):
    session = await get_session(request)
    user_id = session.get("user_id")
    db = request.config_dict["db"]

    # TODO maybe save in global app
    if user_id is None:
        request.app["user"] = None
    else:
        user = await get_user_by_id(db, user_id)
        request.app["user"] = user
    return await handler(request)


@web.middleware
async def login_required_middleware(request, handler):
    user = request.app.get("user")
    if user is not None:
        return await handler(request)
    auth_app = request.app["auth_app"]
    login = auth_app.router["login"].url_for()
    register = auth_app.router["register"].url_for()
    if request.rel_url == login or request.rel_url == register:
        return await handler(request)
    # user is None redirect to login page
    # session = await get_session(request)
    return web.HTTPFound(location=login)


# </editor-fold>


def create_auth_app(config=None):
    app = web.Application()
    if config:
        app["config"] = config
    app.add_routes(routes)
    return app
