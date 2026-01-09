# Gunicorn configuration file for production deployment
# This file configures Gunicorn for optimal performance on a 1GB RAM droplet

# Server socket
bind = "127.0.0.1:8000"

# Worker processes
# For 1GB RAM: 2 workers is safe (formula: 2 * CPU + 1 = 3, but 2 is safer)
# Each worker uses ~100-150MB RAM
workers = 2

# Worker class
worker_class = "sync"  # Use 'sync' for Django (not async)

# Worker connections (for async workers)
worker_connections = 1000

# Request handling
max_requests = 1000  # Restart workers after this many requests (prevents memory leaks)
max_requests_jitter = 100  # Add randomness to prevent all workers restarting simultaneously
timeout = 30  # Workers silent for more than this many seconds are killed
keepalive = 2  # Seconds to wait for requests on a Keep-Alive connection

# Logging
accesslog = "/var/www/learningplatform/logs/gunicorn-access.log"
errorlog = "/var/www/learningplatform/logs/gunicorn-error.log"
loglevel = "info"  # Options: debug, info, warning, error, critical

# Process naming
proc_name = "learningplatform"

# Server mechanics
daemon = False  # Run in foreground (systemd will manage daemonization)
pidfile = "/var/www/learningplatform/gunicorn.pid"
user = "deploy"
group = "deploy"

# Server hooks (optional - uncomment to use)
# def on_starting(server):
#     """Called just before the master process is initialized."""
#     pass
#
# def on_reload(server):
#     """Called to recycle workers during a reload via SIGHUP."""
#     pass
#
# def when_ready(server):
#     """Called just after the server is started."""
#     pass
#
# def pre_fork(server, worker):
#     """Called just before a worker is forked."""
#     pass
#
# def post_fork(server, worker):
#     """Called just after a worker has been forked."""
#     pass
