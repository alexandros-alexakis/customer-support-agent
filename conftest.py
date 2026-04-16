# conftest.py
# This file makes pytest find the project root automatically.
# Without it, running pytest from the project root produces ModuleNotFoundError
# because Python does not know where to find the engine, rag, feedback modules.

import sys
from pathlib import Path

# Add the project root to sys.path so all modules resolve correctly
sys.path.insert(0, str(Path(__file__).parent))
