from flask import session, redirect
from db import *
from load import *
from pred import *
import os
import json

def registration(app, data): 
    db = DB(app)
    # Имя
    name = {
            "first_name": data.get('first_name',None),
            "last_name":  data.get('last_name', None),
            "username":   data.get('username', None),
           }
    jname = json.dumps(name)   
    
    # Поиск
    res = db("SELECT * FROM User WHERE id_soc=1 AND soc=%s;" % data['id'])
    
    with open('test.txt', 'a') as f:
        f.write("SELECT * FROM User WHERE id_soc=1 AND soc=%s;\n" % data['id'])
        f.write(f'{len(res)}\n')
        
    i = None #
    if not len(res): # Регистрация        
        sql = "INSERT INTO User (soc, name, id_soc) VALUES (%s, '%s', 1)"
        
        with open('test.txt', 'a') as f:
            f.write(sql % (data['id'], jname))
        
        i = db(sql % (data['id'], jname))
    else: # Обновление
        i = res[0]['id']
        if  jname != res[0]['name']:
            db("UPDATE User SET name='%s' WHERE id=%s" % (jname, i))
    
    # Каталог файлов клиента
    folder = f'{app.static_folder}/imgs/{i}'
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    # Сессия  
    session['userId']   = i
    session['userSoc']  = data['id']
    session['userName'] = data['username'] if data.get('username') else data.get('first_name')
    
    # Ава
    
    if data['photo_url'] is None: return redirect('/')
        
   
        # Поиск
        
    j = db(f"SELECT id FROM Img WHERE id_user={i} AND src='%s';" % data['photo_url'])
    if len(j):
        if (res[0]['ava'] is None) or (res[0]['ava'] != j[0]['id']):
            db(f"UPDATE User SET ava=%s WHERE id={i};" % j[0]['id'])
            return redirect('/')
        
        # Загрузка
        
    fname = load(data['photo_url'], i)
    xyz, path, hfile = predict(fname)
    os.remove(fname)
        
    sql = 'INSERT INTO Img (id_user, path, src, predx, predy, predz, `hash`) VALUES (%s, "%s", "%s", %s, %s, %s, "%s")'    
    j = db(sql % (i, path, data['photo_url'], *xyz, hfile))
    session['userImg'] = j
    db(f"UPDATE User SET ava={j} WHERE id={i};")
      
    return redirect('/')