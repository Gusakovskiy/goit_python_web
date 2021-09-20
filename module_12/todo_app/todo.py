import aiohttp_jinja2
import pymongo
from aiohttp import web
from aiohttp_session_flash import flash
from asgiref.sync import sync_to_async
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection, ReturnDocument

routes = web.RouteTableDef()


class InvalidRequestException(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg


def _create_query(todo_id):
    try:
        query = {"_id": ObjectId(todo_id)}
    except InvalidId:
        raise InvalidRequestException("Invalid ID")
    return query


def _load_collection(db, user) -> Collection:
    todo_collection: str = user["todo_collection"]
    return getattr(db, todo_collection)


@sync_to_async
def get_user_tasks(db, user):
    todo_collection = _load_collection(db, user)
    cursor = todo_collection.find(dict(),).sort(
        [
            ("done", pymongo.ASCENDING),
            ("priority", pymongo.DESCENDING),
        ]
    )
    tasks = [
        {
            **{
                "id": str(todo["_id"]),  # to be able to create redirect
                "index": _id,
                "task": f'{todo["title"]}; {todo.get("description", "")}',
                "done": todo["done"],
            }
        }
        for _id, todo in enumerate(cursor, 1)
    ]
    return tasks


@sync_to_async
def create_task(db, user, title, description):
    todo_collection = _load_collection(db, user)
    latest_order = todo_collection.aggregate(
        [
            {"$group": {"_id": None, "max_priority": {"$max": "$priority"}}},
        ]
    )
    todo_collection.insert_one(
        dict(
            title=title,
            description=description,
            done=False,
            priority=list(latest_order)[0]["max_priority"] + 1,
        )
    )


@routes.get("/", name="index")
async def index(request):
    db = request.config_dict["db"]
    user = request.config_dict["user"]
    tasks = await get_user_tasks(db, user)

    return aiohttp_jinja2.render_template(
        "todo/index.html",
        request=request,
        context=dict(tasks=tasks),
    )
    # return render_template('todo/index.html', tasks=tasks)


@sync_to_async
def todo_exists(db, user, todo_id) -> bool:
    try:
        query = _create_query(todo_id)
    except InvalidRequestException:
        return False
    todo_collection = _load_collection(db, user)
    todo = todo_collection.find_one(query)
    return todo is not None


@sync_to_async
def mark_todo_done(db, user, todo_id):
    query = _create_query(todo_id)
    todo_collection = _load_collection(db, user)
    _updated_todo = todo_collection.find_one_and_update(
        query, {"$set": {"done": True}}, return_document=ReturnDocument.AFTER
    )


@sync_to_async
def delete_todo(db, user, todo_id):
    query = _create_query(todo_id)
    todo_collection = _load_collection(db, user)
    todo_collection.delete_one(query)


@routes.post("/create", name="create")
async def create(request):
    data = await request.post()
    task = data["task"]
    error = None
    if not task:
        error = "Tasks is required."

    if error is not None:
        flash(request, error)
    splitted_task = task.split(";")
    if len(splitted_task) == 2:
        title, description = splitted_task
    elif len(splitted_task) > 2:
        title, *description = splitted_task
        description = ";".join([el for el in description])
    else:
        title = splitted_task[0]
        description = ""
    await create_task(
        db=request.config_dict["db"],
        user=request.config_dict["user"],
        title=title,
        description=description,
    )
    index_url = request.app.router["index"].url_for()
    return web.HTTPFound(location=index_url)


@routes.post("/{todo_id}/mark_done", name="mark_done")
async def mark_done(request):
    todo_id = request.match_info["todo_id"]
    db = request.config_dict["db"]
    user = request.config_dict["user"]
    exists = await todo_exists(
        db,
        user,
        todo_id,
    )
    if not exists:
        return web.HTTPNotFound(text=f"Not found todo {todo_id}")
    await mark_todo_done(
        db,
        user,
        todo_id,
    )
    index_url = request.app.router["index"].url_for()
    return web.HTTPFound(location=index_url)


@routes.post("/{todo_id}/delete", name="delete")
async def delete(request):
    todo_id = request.match_info["todo_id"]
    db = request.config_dict["db"]
    user = request.config_dict["user"]
    exists = await todo_exists(
        db,
        user,
        todo_id,
    )
    if not exists:
        return web.HTTPNotFound(text=f"Not found todo {todo_id}")
    await delete_todo(db, user, todo_id)
    index_url = request.app.router["index"].url_for()
    return web.HTTPFound(location=index_url)


def create_todo_app(config=None):
    app = web.Application()
    if config:
        app["config"] = None
    app.add_routes(routes)
    return app
