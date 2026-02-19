"""
Entry point for the drowsiness detector application.

This module is intentionally very small: it only creates the Tkinter
root window and instantiates the main application class defined in
``app.py``. All business logic and UI behavior live in that module.
"""

import sys
import tkinter as tk

from app import DetectorSonoApp


if __name__ == "__main__":
    # Wrap the main loop in a try/except so that a Ctrl+C in the
    # terminal exits cleanly without printing a long traceback.
    try:
        root = tk.Tk()
        DetectorSonoApp(root, "Detector de Sonolência v1.0")
    except KeyboardInterrupt:
        sys.exit()
