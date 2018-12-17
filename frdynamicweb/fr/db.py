import pymysql

class DB:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost', port=3306, user='row', password='row',
                                          db='WebApp')
        self.cursor = self.connection.cursor()

    def _get_id(self):
        id = self._get("SELECT MAX(id) FROM  fr")[0]
        if id is None:
            return 1
        else:
            return id + 1
        
    
    def add_face(self, path):
        id = self._get_id()
        def_path = path + str(id)
        self.cursor.execute("INSERT INTO fr (id, path) VALUES ('" + str(id) + "', '" + def_path + "')")
        self.connection.commit()
        return id

    def _get(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

