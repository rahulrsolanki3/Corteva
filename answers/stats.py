from .db import init_stats_table

def compute_and_store_yearly_stats(conn):
    init_stats_table(conn)
    c=conn.cursor()
    c.execute('''
    INSERT OR REPLACE INTO weather_yearly_stats
    (station_id,year,avg_max_temp_c,avg_min_temp_c,total_precip_cm)
    SELECT
        station_id,
        CAST(substr(date,1,4) AS INTEGER) AS year,
        AVG(CASE WHEN max_temp_tenth_c != -9999 THEN max_temp_tenth_c END) / 10.0,
        AVG(CASE WHEN min_temp_tenth_c != -9999 THEN min_temp_tenth_c END) / 10.0,
        SUM(CASE WHEN precip_tenth_mm != -9999 THEN precip_tenth_mm END) / 100.0
    FROM weather_observation
    GROUP BY
        station_id,
    CAST(substr(date,1,4) AS INTEGER);
    ''')

    conn.commit()
