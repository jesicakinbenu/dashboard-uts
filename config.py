import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Folder utama repository dashboard-uts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# File Excel berada di folder utama repository
DATA_PATH = os.path.join(
    PROJECT_DIR,
    "P8. UTS_Business Intelligence.xlsx"
)

# Folder untuk menyimpan hasil pemrosesan
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
