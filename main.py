"""Firebase Cloud Functions entry point that serves the Django app.

Firebase Hosting rewrites every request that isn't a static file to the
`samslist` function below (see firebase.json), which hands it to Django's
WSGI application.
"""

import os
import shutil
from pathlib import Path

from firebase_functions import https_fn, options
from werkzeug.wrappers import Response

BASE_DIR = Path(__file__).resolve().parent

# The deployed source directory is read-only, so SQLite has to live in /tmp.
# NOTE: /tmp is per-instance and wiped when the instance shuts down, so data
# written in production does not persist. See README for details.
SQLITE_PATH = Path(os.environ.get("DJANGO_SQLITE_PATH", "/tmp/db.sqlite3"))

_application = None


def _get_application():
    """Set up Django once per instance (lazily, so `firebase deploy` can
    inspect this module without touching the database)."""
    global _application
    if _application is None:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject.settings")
        os.environ.setdefault("DJANGO_DEBUG", "False")
        os.environ["DJANGO_SQLITE_PATH"] = str(SQLITE_PATH)

        bundled_db = BASE_DIR / "db.sqlite3"
        if not SQLITE_PATH.exists() and bundled_db.exists():
            shutil.copy(bundled_db, SQLITE_PATH)

        from django.core.management import call_command
        from django.core.wsgi import get_wsgi_application

        _application = get_wsgi_application()
        call_command("migrate", interactive=False, verbosity=0)
    return _application


@https_fn.on_request(
    memory=options.MemoryOption.MB_512,
    # A single instance keeps every request on the same SQLite file.
    max_instances=1,
)
def samslist(req: https_fn.Request) -> https_fn.Response:
    return Response.from_app(_get_application(), req.environ)
