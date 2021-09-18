from aiohttp import web

from passlib.utils import getrandstr, rng
from passlib.hash import pbkdf2_sha256
from string import hexdigits

from pymongo.collection import Collection
import aiohttp_jinja2

auth_app = web.Application()
routes = web.RouteTableDef()


def _get_random_str(number_ch=10):
    return getrandstr(rng,  charset=hexdigits, count=number_ch)


async def _example_todos():
    return [
        dict(title='Register in App', done=True, priority=0),
        dict(title='Plan next week', done=False, description='You doing great', priority=1),
        dict(
            title='Sleep more well',
            done=False,
            description='Sleep is very important for your health',
            priority=3,
        ),
        dict(
            title='Buy healthy food', done=False, priority=4),
    ]

@routes.post('/register', name='register')
@routes.get('/register', name='register')
@aiohttp_jinja2.template('auth.register')
async def register(request):
    db = request.config_dict['db']
    data = await request.post()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if username:
            user = db.user.find_one(
                {"username": username}
            )
            if user is not None:
                error = 'Already registered.'

        if error is None:
            collection_name = f'todo_list_{username}_{_get_random_str()}'
            db.user.insert_one(
                dict(
                    username=username,
                    password=pbkdf2_sha256.hash(password),
                    todo_collection=collection_name
                ),
            )
            user_todo: Collection = getattr(db, collection_name)
            user_todo.insert_many(_example_todos())
            location = request.app.router['login'].url_for()
            return web.Response(text=f"registered_{location}", )
            # return web.HTTPFound(location=location)

    # return aiohttp_jinja2.render_template('auth/register.html')



#
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None
#         user = db.user.find_one(
#             {"username": username}
#         )
#
#         if user is None:
#             error = 'Incorrect username.'
#         # TODO sync_to_async
#         elif not pbkdf2_sha256.verify(user['password'], password):
#             error = 'Incorrect password.'
#
#         if error is None:
#             session.clear()
#             session['user_id'] = str(user['_id'])
#             return redirect(url_for('index'))
#
#         flash(error)
#
#     return render_template('auth/login.html')
#
#
# @auth_bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')
#
#     if user_id is None:
#         g.user = None
#     else:
#         db = get_db()
#         g.user = db.user.find_one(
#             {"_id": ObjectId(user_id)}
#         )
#
#
# @auth_bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))
#
#  #TODO middleware
# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#
#         return view(**kwargs)
#     return wrapped_view

auth_app.add_routes(routes)
