from .common import *

DEBUG = True

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}
