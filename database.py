from ast import Return
from optparse import Values
import sqlite3
from subprocess import CREATE_DEFAULT_ERROR_MODE
from threading import Thread
import threading
from typing import Self

class Database():
    def __init__(self):
        self.lock = threading.Lock()
        
        # self.create_table()
        # self.create_subtask_table()
        # self.create_user()

    def create_user(self):
        with self.lock:
            conn = sqlite3.connect('TODO.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name VARCHAR(255) NOT NULL ,
                    password TEXT NOT NULL)
                    '''
                )
            conn.commit()
    def add_user(self,user_name,password):
        conn = sqlite3.connect('TODO.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (user_name, password) VALUES(?,?)',(user_name, password))
        conn.commit()
        NEW_USER = cursor.execute('SELECT user_id, user_name FROM users').fetchall()
        return (NEW_USER[-1]) 
    
    #////////////////////// CREA TABELLA DEI COMPITIT \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # def create_table(self):
    #     self.cursor.execute(''' CREATE TABLE IF NOT EXISTS tasks (
    #             task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             titolo TEXT ,
    #             desc TEXT ,
    #             data TEXT ,
    #             completato BOOLEAN NOT NULL CHECK (completato IN (0,1)),
    #             id INTEGER ,
    #             FOREIGN KEY (id) REFERENCES users (user_id))''')
        
    #     self.conn.commit()
    

    # def add_task(self,tt,t,d):
    #     self.cursor.execute('INSERT INTO tasks (titolo, desc, data, completato) VALUES (?,?,?,?)',(tt,t,d,0))
    #     task = self.cursor.execute('SELECT id ,titolo,desc,data FROM tasks WHERE titolo =? and desc = ? and completato = 0',(tt,t)).fetchall()
    #     self.conn.commit()
    #     return task[-1]

    # def get_tasks(self):
    #     incompletati = self.cursor.execute("SELECT id ,titolo,desc,data FROM tasks WHERE completato = 0 ").fetchall()
    #     completati = self.cursor.execute("SELECT id ,titolo,desc,data FROM tasks WHERE completato = 1").fetchall()

    #     return incompletati ,completati
    # def mark_task_completi(self,taskID):
    #     self.cursor.execute('UPDATE tasks SET completato = 1 WHERE id = ?',(taskID,))# é necessario la -->(,) per renderlo una tupla 
    #     self.conn.commit()
    #     # value = self.cursor.execute('SELECT titolo,desc FROM tasks WHERE id =?',(taskID)).fetchall()

    #     # return value
    # def mark_task_incompleti(self,taskID):
    #     self.cursor.execute('UPDATE tasks SET completato = 0 WHERE id = ?',(taskID,))
    #     self.conn.commit()

    #     cr_ = ['[S]','[/S]']
    #     VALUES =self.cursor.execute("SELECT titolo,desc FROM tasks WHERE completato = 0 ").fetchall()
    #     for task in VALUES:
    #         print(list(''.join(task).removeprefix('[s]')))
    #         print(len(''.join(task)))
    
    # def modifiy(self,t,d,taskID):
    #     self.cursor.execute('UPDATE tasks SET titolo =? ,desc = ? WHERE id = ?',(t,d,taskID))
    #     self.conn.commit()
    #     modifyed_task = self.cursor.execute('SELECT titolo,desc FROM tasks WHERE id = ?',(taskID,)).fetchall()
    #     return modifyed_task

    
    # def delet_task (self,taskID):
    #     self.cursor.execute('DELETE FROM tasks WHERE id =?',(taskID,))
    #     self.conn.commit()

    # def delet_all_task (self):
    #     self.cursor.execute('DELETE FROM tasks ')
    #     self.conn.commit()
    #     # self.conn.close()
    
    # #////////////////////////////////// SUBT5ASK /////////////////////////////////////
    # def create_subtask_table(self):
    #     self.cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS subtasks (
    #             subtask_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    #             subtask VARCHAR(255) NOT NULL ,
    #             completato BOOLEAN NOT NULL CHECK (completato IN(0,1)),
    #             id INTEGER,
    #             FOREIGN KEY (id) REFERENCES tasks (id)
    #             )
    #                         ''')
    #     self.conn.commit()
    
    # def add_subtask(self,subtask,task_id,c):
    #     self.cursor.execute('INSERT INTO subtasks (subtask,completato,id) VALUES(?,?,?)',(subtask,task_id,c))
    #     self.conn.commit()

    #     subtask_value = self.cursor.execute('SELECT subtask,subtask_id,id FROM subtasks').fetchall()
    #     return subtask_value[-1]

    # def get_subtasks(self,task_id):
    #     ''' selezione tutti i sotto obiettivi dalla tabella '''
    #     get_all_subtasks = self.cursor.execute('SELECT subtask , subtask_id FROM subtasks WHERE id =?',(task_id,)).fetchall()
       
    #     get_all_subtasks.sort()
    #     return get_all_subtasks[-6:]
    
        
    # def get_market_sutasks_completati(self,id):
    #     ''' segna il sotto ibiettivo come comlpetato '''
    #     self.cursor.execute('UPDATE subtasks SET completato=1 WHERE id = ? AND completato=0'(id))
    #     self.conn.commit()

    #     #get subtask completati 
    #     completati = self.cursor.execute('SELECT subtask FROM subtasks WHERE completato = 1 AND WHERE id = ?'(id)).fetchall()
    #     return completati
    
    # def mark__sutasks_incompletati(self,id):
    #     ''' segna il sotto ibiettivo come incomlpetato '''
    #     self.cursor.execute('UPDATE subtasks SET completato=0 WHERE id = ? AND completato=1'(id))   
    #     self.conn.commit()
    #     #get subtask incompletati
       
    #     incompletati = self.cursor.execute('SELECT subtask FROM subtasks WHERE completato = 1 AND WHERE id = ?'(id)).fetchall()
    #     return incompletati

    # ''' cancella sooto biettivo dal database '''
    # def delet_subtask(self,task_id,id):
    #     ''' cancella il sotto obiettivo '''
    #     self.cursor.execute('DELETE  FROM subtasks WHERE id = ? AND subtask_id =?',(task_id,id))
    #     self.conn.commit()
    
    # ''' cancella tutti i sottoobiettivi quando l obiettivo principale é cancellato '''
    # def delet_all_subtask(self,task_id):
    #     self.cursor.execute('DELETE  FROM subtasks WHERE id =?',(task_id,)) #--- non dimenticare di mettere (,)
    #     self.conn.commit()
    #     return 'subtask cancellato!!'



        

db = Database()
# db.create_table()
# db.mark_task_incompleti()
# db.add_subtask('ciao',115)
# db.delet_all_task()
# db.delet_subtask(115,6)
# db.create_user()
# db.create_table()
# db.create_subtask_table
# db.add_user('khadim','23101999@')


