import os, logging, sqlite3
from datetime import datetime
from typing import Tuple

def parse_line(line):
    p=line.strip().split()
    return p[0], int(p[1]), int(p[2]), int(p[3])

def ingest_file(conn, filepath):
    fn=os.path.basename(filepath)
    station_id,_=os.path.splitext(fn)
    c=conn.cursor()
    c.execute('INSERT OR IGNORE INTO weather_station(station_id) VALUES(?)',(station_id,))
    ins=0
    with open(filepath) as f:
        for line in f:
            if not line.strip(): continue
            d,ma,mi,pr=parse_line(line)
            c.execute('''INSERT OR IGNORE INTO weather_observation(station_id,date,max_temp_tenth_c,min_temp_tenth_c,precip_tenth_mm) VALUES(?,?,?,?,?)''',(station_id,d,ma,mi,pr))
            if c.rowcount==1: ins+=1
    conn.commit()
    return ins

def ingest_all(conn, data_dir):
    tot=0; fc=0
    for r,_,fs in os.walk(data_dir):
        for f in fs:
            if f.endswith('.txt'):
                fc+=1
                tot+=ingest_file(conn, os.path.join(r,f))
    print('Files:',fc,'Records:',tot)
