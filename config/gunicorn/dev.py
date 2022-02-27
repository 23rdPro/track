from tempfile import mkstemp


def ready(server):
    # open('/tmp/app-initialized', 'w').close()
    fd, path = mkstemp(prefix='/tmp/app-initialized')
    open(path, 'w').close()

# from multiprocessing import cpu_count
# from os import environ
#
#
# def max_workers():
#     return cpu_count()
#
#
# wsgi_app = "track.wsgi:application"
#
# loglevel = "debug"
#
# workers = max_workers()
#
# # worker_class = 'gevent'
#
# bind = 'localhost:' + environ.get('PORT', '8000')
#
# reload = True
#
# max_requests = 1000
#
# # accesslog = errorlog = "/var/log/gunicorn/dev.log"
#
# capture_output = True
#
# # pidfile = "/var/run/gunicorn/dev.pid"
#
# daemon = True
