""" Miscellaneous helper functions.
"""

import sys

def graceful_exit() -> None:
    """ Gracefully exits the program with a 0 exit code.
    """
    print("Exiting...")
    sys.exit(0)
