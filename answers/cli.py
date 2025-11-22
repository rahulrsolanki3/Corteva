import logging
from .config import WX_DATA_DIR
from .db import get_connection, init_db
from .ingest import ingest_all
from .stats import compute_and_store_yearly_stats

def main():
    conn=get_connection()
    init_db(conn)
    ingest_all(conn, str(WX_DATA_DIR))
    compute_and_store_yearly_stats(conn)
    conn.close()

if __name__=='__main__': main()
