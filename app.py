"""
Application entry point alias for main.py.
Allows running the application via either `streamlit run main.py` or `streamlit run app.py`.
"""
import os
import sys
import runpy

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    main_file = os.path.join(current_dir, "main.py")
    runpy.run_path(main_file, run_name="__main__")
