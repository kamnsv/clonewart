from flask import render_template, redirect, session, send_from_directory, jsonify, request, send_file
from db import DB  
import os

def img(app):
    #Ава
    @app.route('/img')
    def get_imgself():
        if session.get('userId') is None:
            return render_template('error.html', title=401)	
        
        db = DB(app)
        res = db(f'SELECT path FROM Img INNER JOIN User ON Img.id=User.ava WHERE User.id=%s;' % session.get('userId'))
        if len(res): 
            fname = os.path.join(app.static_folder, res[0]['path'])
            if os.path.isfile(fname):
                return send_file(fname)
                
        return render_template('error.html', title=404)
        

    #Фото по id
    @app.route('/img/<int:i>')
    def get_img(i):
        db = DB(app)
        res = db(f'SELECT id, id_user, path FROM Img WHERE id={i};')
        
        if 0 == len(res):
            return render_template('error.html', title=404)

        if  res[0]['id_user']<0 or res[0]['id_user'] == session.get('userId', None):
            fname = os.path.join(app.static_folder, res[0]['path'])
            if os.path.isfile(fname):
                return send_file(fname)
           
            
        return render_template('error.html', title=403)    
    
    #Все демо фото
    @app.route('/imgs')
    def get_imgs():
        db = DB(app)
        imgs = db(f'SELECT id as i, predx as x, predy as y, predz as z FROM Img WHERE id_user < 1;')
        return jsonify(imgs)
    
    #Случайные демо актеры 
    @app.route('/demo/<int:i>')
    def get_demo(i):
        db = DB(app)
        actors = db(f'SELECT id_user as c FROM `Img` GROUP BY id_user ORDER BY rand() LIMIT {i};');
        imgs = []
        for actor in actors:
           imgs += db(f'SELECT -id_user as c, id as i, predx as x, predy as y, predz as z FROM Img WHERE id_user=%s;' % actor['c'])
        return jsonify(imgs)
        
    #Случайное окружение из фото 
    @app.route('/rnd')
    def get_rnds():
        db = DB(app)
        res = db(f'SELECT id as i, predx as x, predy as y, predz as z FROM Img WHERE id_user < 1 ORDER BY rand() LIMIT 1;')
        if not len(res): return jsonify(res)  
        i = res[0]['i']
        s = 'img_%s as i, predx as x, predy as y, predz as z'
        f = 'Dist INNER JOIN Img ON Dist.img_%s = Img.id'
        w = f'Dist.img_%s = {i} AND dist < 100 AND id_user < 1'
        imgs = db(f'SELECT {s % "b"} FROM {f % "b"} WHERE {w % "a"} UNION SELECT {s % "a"} FROM {f % "a"} WHERE {w % "b"} LIMIT 1000;')
        return jsonify({'center': res[0], 'imgs': imgs})   
    
    #Загрузка мира
    @app.route('/imgs/<int:page>')
    def get_imgs_batch(page):
        if session.get('userId') is None:
            return render_template('error.html', title=401)	
        db = DB(app)
        i = session.get('userImg')
        if i is None: return jsonify({'center': {}, 'imgs': []})  
        res = db(f'SELECT id as i, predx as x, predy as y, predz as z FROM Img WHERE id={i};')
        d = 5
        s = 'img_%s as i, predx as x, predy as y, predz as z'
        f = 'Dist INNER JOIN Img ON Dist.img_%s = Img.id'
        f = f'({f}) INNER JOIN User ON Img.id=User.ava'
        w = f'Dist.img_%s = {i} AND dist >= {(page-1)*d} AND dist < {page*d}'
                        
        imgs = db(f'SELECT {s % "b"} FROM {f % "b"} WHERE {w % "a"} UNION SELECT {s % "a"} FROM {f % "a"} WHERE {w % "b"}')

        return jsonify({'center': res[0], 'imgs': imgs}) 
     
    #Мои фото
    @app.route('/my')
    def get_my_imgs():
        if session.get('userId') is None:
            return render_template('error.html', title=401)	
        db = DB(app)
        res = db(f'SELECT id as i, predx as x, predy as y, predz as z FROM Img WHERE id_user=%s;' % session.get('userId'))
        return jsonify(res)