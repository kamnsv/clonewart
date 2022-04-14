from flask import session, redirect, url_for, request, render_template, make_response
import os
import datetime
from db import *
import json
from pred import predict

def put(app):
     
  @app.route('/put', methods=['GET', 'POST'])
  def put_file():
      if 'GET' == request.method or session.get('userId') is None: 
          return render_template('error.html', title=404)	
         
      f = request.files['file'] 
      _, ext = os.path.splitext(f.filename)
      ext = ext.lower()[1:]
      if ext not in ('jpg', 'png', 'bmp'):
      	return json.dumps({'success': False}), 415, {'ContentType':'application/json'}
        
      name = f"{datetime.datetime.now():%Y%m%d-%H%M%S}.{ext}"
      fname = os.path.join('imgs', str(session.get('userId')), name)
         
      f.save(os.path.join(app.static_folder, fname))
      xyz, path, hfile = predict(fname)
      
      db = DB(app)
      
      sql = 'SELECT * FROM Img WHERE id_user=%s AND predx=%s AND predy=%s AND predz=%s AND `hash`="%s";'
      r = db(sql % (session.get('userId'), *xyz, hfile))
      if len(r): return json.dumps({'success': False}), 422, {'ContentType':'application/json'}
      
      sql = 'INSERT INTO Img (id_user, path, src, predx, predy, predz, `hash`) VALUES (%s, "%s", "%s", %s, %s, %s, "%s")'
      i = db(sql % (session.get('userId'), path, fname, *xyz, hfile))
      x,y,z = xyz
      return json.dumps({'success':True, 'i': i, 'x': x, 'y': y, 'z': z}), 200, {'ContentType':'application/json'}