from flask import Flask, jsonify, request, g
from flasgger import Swagger
from math import ceil
from .db import get_connection
from .config import DB_PATH

def create_app():
    app=Flask(__name__); Swagger(app)
    @app.before_request
    def bef(): g.db=get_connection(str(DB_PATH))
    @app.teardown_appcontext
    def aft(e): db=g.pop('db',None); db and db.close()
    def get_db(): return g.db
    def pag():
        p=int(request.args.get('page',1)); s=int(request.args.get('page_size',50)); return max(p,1), max(1,min(s,200))
    @app.get('/api/weather')
    def weather():
        c=get_db().cursor()
        st=request.args.get('station_id'); d=request.args.get('date')
        w=[]; p=[]
        if st: w.append('station_id=?'); p.append(st)
        if d: w.append('date=?'); p.append(d)
        ws=('WHERE '+ ' AND '.join(w)) if w else ''
        page,ps=pag()
        c.execute(f'SELECT COUNT(*) FROM weather_observation {ws}', p); tot=c.fetchone()[0]
        off=(page-1)*ps
        c.execute(f'''SELECT station_id,date,max_temp_tenth_c,min_temp_tenth_c,precip_tenth_mm FROM weather_observation {ws} ORDER BY station_id,date LIMIT ? OFFSET ?''', p+[ps,off])
        rows=c.fetchall()
        return jsonify({'data':[{'station_id':r[0],'date':r[1],'max':r[2],'min':r[3],'precip':r[4]} for r in rows],'pagination':{'page':page,'page_size':ps,'total':tot,'total_pages':ceil(tot/ps)}})
    @app.get('/api/weather/stats')
    def stats():
        c=get_db().cursor()
        st=request.args.get('station_id')
        y=request.args.get('year')
        w=[]; p=[]
        if st: w.append('station_id=?'); p.append(st)
        if y: w.append('year=?'); p.append(int(y))
        ws=('WHERE '+ ' AND '.join(w)) if w else ''
        page,ps=pag()
        c.execute(f'SELECT COUNT(*) FROM weather_yearly_stats {ws}', p); tot=c.fetchone()[0]
        off=(page-1)*ps
        c.execute(f'''SELECT station_id,year,avg_max_temp_c,avg_min_temp_c,total_precip_cm FROM weather_yearly_stats {ws} ORDER BY station_id,year LIMIT ? OFFSET ?''', p+[ps,off])
        rows=c.fetchall()
        return jsonify({'data':[{'station_id':r[0],'year':r[1],'avg_max':r[2],'avg_min':r[3],'precip_cm':r[4]} for r in rows],'pagination':{'page':page,'page_size':ps,'total':tot,'total_pages':ceil(tot/ps)}})
    return app

if __name__=='__main__': create_app().run(debug=True)
