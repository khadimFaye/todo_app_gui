from optparse import Values
import sqlite3
from subprocess import CREATE_DEFAULT_ERROR_MODE

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('TODO.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    
    def create_table(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titolo TEXT ,
                desc TEXT ,
                data TEXT ,
                completato BOOLEAN NOT NULL CHECK (completato IN (0,1)))''')

        self.conn.commit()
    def add_task(self,tt,t,d):
        self.cursor.execute('INSERT INTO tasks (titolo, desc, data, completato) VALUES (?,?,?,?)',(tt,t,d,0))
        task = self.cursor.execute('SELECT id ,titolo,desc,data FROM tasks WHERE titolo =? and desc = ? and completato = 0',(tt,t)).fetchall()
        self.conn.commit()
        return task[-1]

    def get_tasks(self):
        incompletati = self.cursor.execute("SELECT id ,titolo,desc,data FROM tasks WHERE completato = 0 ").fetchall()
        completati = self.cursor.execute("SELECT id ,titolo,desc,data FROM tasks WHERE completato = 1").fetchall()

        return incompletati ,completati
    def mark_task_completi(self,taskID):
        self.cursor.execute('UPDATE tasks SET completato = 1 WHERE id = ?',(taskID,))# é necessario la -->(,) per renderlo una tupla 
        self.conn.commit()
        # value = self.cursor.execute('SELECT titolo,desc FROM tasks WHERE id =?',(taskID)).fetchall()

        # return value
    def mark_task_incompleti(self,taskID):
        self.cursor.execute('UPDATE tasks SET completato = 0 WHERE id = ?',(taskID,))
        self.conn.commit()

        cr_ = ['[S]','[/S]']
        VALUES =self.cursor.execute("SELECT titolo,desc FROM tasks WHERE completato = 0 ").fetchall()
        for task in VALUES:
            print(list(''.join(task).removeprefix('[s]')))
            print(len(''.join(task)))
    
    def modifiy(self,t,d,taskID):
        self.cursor.execute('UPDATE tasks SET titolo =? ,desc = ? WHERE id = ?',(t,d,taskID))
        self.conn.commit()
        modifyed_task = self.cursor.execute('SELECT titolo,desc FROM tasks WHERE id = ?',(taskID,)).fetchall()
        return modifyed_task

    
    def delet_task (self,taskID):
        self.cursor.execute('DELETE FROM tasks WHERE id =?',(taskID,))
        self.conn.commit()

    def delet_all_task (self):
        self.cursor.execute('DELETE FROM tasks ')
        self.conn.commit()
        # self.conn.close()

db = Database()
db.create_table()
db.mark_task_incompleti(3)
# db.delet_all_task()


