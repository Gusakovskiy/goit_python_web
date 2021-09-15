import pymongo
from bson import ObjectId
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from pymongo.collection import Collection, ReturnDocument
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

todo_bp = Blueprint('todo', __name__)


def _load_collection() -> Collection:
    db = get_db()
    return getattr(db, g.user['todo_collection'])


@todo_bp.route('/', methods=['GET'])
@login_required
def index():
    todo_collection = _load_collection()
    cursor = todo_collection.find(
            dict(),
        ).sort(
            [
                ("done", pymongo.ASCENDING),
                ("priority", pymongo.DESCENDING),
            ]
        )
    tasks = [
        {
            **{
                'id': str(todo['_id']),  # to be able to create redirect
                'index': index,
                'task': f'{todo["title"]}; {todo.get("description", "")}',
                'done': todo['done']
            }
        }
        for index, todo in enumerate(cursor, 1)
    ]
    return render_template('todo/index.html', tasks=tasks)


@todo_bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        error = None
        task = request.form['task']
        if not task:
            error = 'Tasks is required.'

        if error is not None:
            flash(error)
        else:
            splitted_task = task.split(';')
            if len(splitted_task) == 2:
                title, description = splitted_task
            elif len(splitted_task) > 2:
                title, *description = splitted_task
                description = ';'.join([el for el in description])
            else:
                title = splitted_task[0]
                description = ''
            todo_collection = _load_collection()
            latest_order = todo_collection.aggregate(
                [
                    {
                        "$group": {
                            "_id": None,
                            "max_priority": {"$max": "$priority"}
                        }
                    },
                ]
            )
            todo_collection.insert_one(
                dict(
                    title=title,
                    description=description,
                    done=False,
                    priority=list(latest_order)[0]['max_priority'] + 1
                )
            )
            return redirect(url_for('todo.index'))
    # return render_template('todo/create.html')


@todo_bp.route('/<todo_id>/mark_done', methods=('POST',))
@login_required
def mark_done(todo_id: str):
    todo_collection = _load_collection()
    query = {'_id': ObjectId(todo_id)}
    todo = todo_collection.find_one(query)
    if not list(todo):
        abort(404, f'Not found todo {todo_id}')

    _updated_todo = todo_collection.find_one_and_update(
        query, {"$set": {"done": True}},
        return_document=ReturnDocument.AFTER
    )
    return redirect(url_for('todo.index'))


@todo_bp.route('/<todo_id>/delete', methods=('POST',))
@login_required
def delete(todo_id: str):

    todo_collection = _load_collection()
    query = {'_id': ObjectId(todo_id)}
    todo = todo_collection.find_one(query)
    if not list(todo):
        abort(404, f'Not found todo {todo_id}')
    todo_collection.delete_one(query)
    return redirect(url_for('todo.index'))