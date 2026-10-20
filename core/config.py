
import os
import sys

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CORE_DIR)

sys.path.insert(0, CORE_DIR)

DATA_FILENAME = "P8. UTS_Business Intelligence.xlsx"
DATA_PATH = os.path.join(PROJECT_DIR, DATA_FILENAME)

OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
