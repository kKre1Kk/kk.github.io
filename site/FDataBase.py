import math, time, sqlite3, re
from flask import url_for

class FDataBase:
    
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res

        except:
            print('Ошибка чтения из БД')

        return []

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Статья с таким url уже существует")
                return False
            base = url_for('static', filename='images_html')

            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>)>",
            "\\g<tag>" + base + "/||g<url>>",
            text)

            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)', ( title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as err:
            print('Ошибка добавления статьи в базу данных ' + str(err))
            return False
        

        return True
    
    def getPost(self, alias):
        try: 
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE  '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res: 
                return res
        except sqlite3.Error as err:
            print('Ошибка получения статьи из БД ' + str(err))

        return (False, False)
    
    def getPostsAnonce(self):
        try: 
            self.__cur.execute(f'SELECT id, title, url, text FROM posts ORDER BY time DESC')
            res = self.__cur.fetchall()
            if res: 
                return res
        except sqlite3.Error as err:
            print('Ошибка получения статьи из БД ' + str(err))

        return []
    
    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email like '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False
            
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (name, email, hpsw, tm))
            self.__db.commit()

        except sqlite3.Error as e:
            print('Ошибка добавления в БД ' +str(e))
            return False
        return True
    
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            
            return res
        
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД ' + str(e))

        return False
    
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email like '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res: 
                print('Пользователь не найден')
                return False

            return res

        except sqlite3.Error as e:
            print('Ошибка получения данных из БД ' + str(e))

        return False
    
    
    
    def updateUserAvatar(self, avatar, user_id):
        if not avatar: return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка обновления аватара в БД ' + str(e))
            return False
        return True