import sys
import logging
from pathlib import Path

# Add parent directory to Python path for package imports
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from .main import main

if __name__ == "__main__":
    sys.exit(main()) 