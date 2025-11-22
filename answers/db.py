import sqlite3
from .config import DB_PATH

def get_connection(db_path=None):
    db_file=str(db_path or DB_PATH)
    conn=sqlite3.connect(db_file)
    conn.execute('PRAGMA foreign_keys=ON;')
    return conn

def init_db(conn):
    c=conn.cursor()
    c.executescript('''
CREATE TABLE IF NOT EXISTS weather_station(id INTEGER PRIMARY KEY AUTOINCREMENT,station_id TEXT NOT NULL UNIQUE,name TEXT,state TEXT);
CREATE TABLE IF NOT EXISTS weather_observation(id INTEGER PRIMARY KEY AUTOINCREMENT,station_id TEXT NOT NULL,date TEXT NOT NULL,max_temp_tenth_c INTEGER,min_temp_tenth_c INTEGER,precip_tenth_mm INTEGER,UNIQUE(station_id,date),FOREIGN KEY(station_id) REFERENCES weather_station(station_id));
''')
    conn.commit()

def init_stats_table(conn):
    c=conn.cursor()
    c.executescript('''
CREATE TABLE IF NOT EXISTS weather_yearly_stats(id INTEGER PRIMARY KEY AUTOINCREMENT,station_id TEXT NOT NULL,year INTEGER NOT NULL,avg_max_temp_c REAL,avg_min_temp_c REAL,total_precip_cm REAL,UNIQUE(station_id,year),FOREIGN KEY(station_id) REFERENCES weather_station(station_id));
''')
    conn.commit()
