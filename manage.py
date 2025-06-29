#!/usr/bin/env python
"""
manage.py

Django's command-line utility for administrative tasks in the Cycle Tracker project.
"""

import os
import sys

def main():
    """
    Sets the default Django settings module for the project and
    executes the command-line utility for various administrative tasks,
    including running the server, migrations, shell access, etc.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cycle_tracker_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
