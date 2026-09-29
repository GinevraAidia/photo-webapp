import os
import sys

from config import settings

# Start Django
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Only attach debugpy in the actual server process (RUN_MAIN is set by
    # Django's autoreloader); otherwise the reloader's child re-runs this
    # script and fails with "Address already in use".
    if settings.DEBUG and os.environ.get('RUN_MAIN') == 'true':
        import debugpy  # noqa: T100

        # Use a dedicated port: runserver itself binds 5000
        debugpy.listen(("0.0.0.0", 5678))  # noqa: T100

        # Pause execution until debugger attaches
        if os.environ.get('WAIT_FOR_DEBUGGER', 'False') == 'True':
            print("⏳ Waiting for debugger to attach...")
            debugpy.wait_for_client()
            print("✅ Debugger attached!")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)