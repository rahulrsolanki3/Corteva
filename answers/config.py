from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'weather.db'
WX_DATA_DIR = BASE_DIR / 'wx_data'
