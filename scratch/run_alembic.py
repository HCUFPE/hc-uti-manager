import os
import sys

# Prepend the 'src' directory to Python's search path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))

from alembic.config import main

if __name__ == '__main__':
    main()
