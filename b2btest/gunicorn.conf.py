import os

worker_class = 'uvicorn.workers.UvicornWorker'
workers = os.environ['WORKERS']
timeout = os.environ['TIMEOUT']
user = os.environ['USER']
bind = f'{os.environ["HOST"]}:{os.environ["PORT"]}'
