from django.db import transaction
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from todo.models import Todo  # NOQA


@login_required(login_url='auth:login')
def index_view(request):
    tasks = Todo.objects.filter(
        user=request.user
    ).only(
        'id',
        'done',
        'title',
        'description',
        'priority',
    ).order_by(
        'done',
        # ascending/descending
        '-priority',
    )
    return render(request, 'todo/index.html', context=dict(tasks=tasks))


@login_required(login_url='auth:login')
def create_view(request):
    if request.method != 'POST':
        return redirect(reverse('todo:index'))
    task = request.POST['task']
    error = None
    if not task:
        error = "Tasks is required."

    if error is not None:
        messages.add_message(request, messages.ERROR, error)
        return

    splitted_task = task.split(";")
    if len(splitted_task) == 2:
        title, description = splitted_task
    elif len(splitted_task) > 2:
        title, *description = splitted_task
        description = ";".join([el for el in description])
    else:
        title = splitted_task[0]
        description = ""
    user = request.user
    with transaction.atomic():
        max_priority = Todo.objects.filter(
            user=user
        ).aggregate(
            max_priority=Max('priority')
        )

        task = Todo(
            title=title,
            description=description,
            user=request.user,
            priority=max_priority['max_priority'] + 1,
        )
        task.save()
    return redirect(reverse('todo:index'))


@login_required(login_url='auth:login')
def delete_view(request, task_id):
    task = get_object_or_404(Todo, pk=task_id, user=request.user)
    task.delete()
    return redirect(reverse('todo:index'))


@login_required(login_url='auth:login')
def mark_done_view(request, task_id):
    task = get_object_or_404(Todo, pk=task_id, user=request.user)
    task.done = True
    task.save()
    # CHECK UPDATE
    return redirect(reverse('todo:index'))

