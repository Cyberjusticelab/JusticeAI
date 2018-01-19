import sqlite3
from uuid import uuid4


class DbGateway:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS responses (
            id text,
            question text,
            email text,
            is_subscribed integer,
            is_legal_professional integer
        )''')
        self.conn.commit()

    def insert_anonymous_question(self, question):
        c = self.conn.cursor()
        # prevent SQL injection with DB-API param substitution
        id = str(uuid4())
        insert = (id, str(question),)
        c.execute('''INSERT INTO responses (id, question) VALUES (?,?)''', insert)
        self.conn.commit()
        return id

    def insert_anonymous_email(self, email):
        c = self.conn.cursor()
        # prevent SQL injection with DB-API param substitution
        id = str(uuid4())
        insert = (id, str(email),)
        c.execute('''INSERT INTO responses (id, email) VALUES (?,?)''', insert)
        self.conn.commit()
        return id

    def insert_anonymous_subscription(self, is_subscribed):
        c = self.conn.cursor()
        # prevent SQL injection with DB-API param substitution
        id = str(uuid4())
        insert = (id, str(is_subscribed),)
        c.execute('''INSERT INTO responses (id, is_subscribed) VALUES (?,?)''', insert)
        self.conn.commit()
        return id

    def insert_anonymous_legal_professional(self, is_legal_professional):
        c = self.conn.cursor()
        # prevent SQL injection with DB-API param substitution
        id = str(uuid4())
        insert = (id, str(is_legal_professional),)
        c.execute('''INSERT INTO responses (id, is_legal_professional) VALUES (?,?)''', insert)
        self.conn.commit()
        return id

    def update_email_by_id(self, id, email):
        c = self.conn.cursor()
        # prevent SQL injection with DB-API param substitution
        insert = (str(email), str(id),)
        c.execute('''UPDATE responses SET email=? WHERE id=?''', insert)
        self.conn.commit()
        return id

    def update_subscription_by_id(self, id, is_subscribed):
        c = self.conn.cursor()
        # prevent SQL injection with DB-API param substitution
        insert = (int(is_subscribed), str(id),)
        c.execute('''UPDATE responses SET is_subscribed=? WHERE id=?''', insert)
        self.conn.commit()
        return id

    def update_legal_professional_by_id(self, id, is_legal_professional):
        c = self.conn.cursor()
        # prevent SQL injection with DB-API param substitution
        insert = (int(is_legal_professional), str(id),)
        c.execute('''UPDATE responses SET is_legal_professional=? WHERE id=?''', insert)
        self.conn.commit()
        return id
