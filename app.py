from flask import render_template, redirect, session, send_file
from auth import auth  
from db import DB  
from img import img
import os
from put import put

def start(app):

    app.config.from_object('config')
    app.secret_key = app.config['SECRET_KEY']     
    
    @app.route('/')
    def home():
        if session.get('userId'):
            db = DB(app)
            res = db('SELECT id FROM User WHERE id=%s' % session['userId'])
            if not len(res):
                 return redirect('/logout')
                 
        if session.get('userId'):         
            return render_template('home.html', title='home', load=True,
                               name=session.get('userName'),
                               userId=session.get('userId')) 
                               
        return render_template('main.html', title='index',
                               name=session.get('userName'),
                               userId=session.get('userId')) 
    @app.route('/w')
    def world():
        if session.get('userId'):
            db = DB(app)
            res = db('SELECT id FROM User WHERE id=%s' % session['userId'])
            if not len(res):
                 return redirect('/logout')
        if session.get('userId'):         
            return render_template('world.html', title='world',
                               name=session.get('userName'),
                               userId=session.get('userId'))
        return render_template('error.html', title=401)                       
    auth(app)
    img(app)
    put(app)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', title=404)
        
    @app.route('/stat/<string:name>')
    def get_static(name): 
        fname = os.path.join(app.static_folder, 'stat', name)
        if os.path.isfile(fname):
        	return send_file(fname)
        return render_template('error.html', title=404)
    