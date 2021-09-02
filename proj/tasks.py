from .celery_app import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def process_results(results):
    for result in results:
        process_single_result.delay(result)


@app.task
def process_single_result(result):
    print('Got result', result)
    return result * 2
