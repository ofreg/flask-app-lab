# tests/conftest.py
import sys
import os

# Додати кореневу папку проєкту до PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
