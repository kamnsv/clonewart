from flask_mysqldb import MySQL
class DB(MySQL):        
    def __init__(self, app):
        super().__init__(app)
        self.cursor = self.connection.cursor()
    
    def __call__(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()
        
        if self.cursor.lastrowid > 0:
            return self.cursor.lastrowid
            
        res = self.cursor.fetchall()   
        return res
        
    def __del__(self):
        self.cursor.close()
        