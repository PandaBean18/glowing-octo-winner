# id: integer, unique 
# username: string, unique 
# password_digest: string, unique*
# session_token: string
# created_on: string (date)

import pickle 
import secrets
import bcrypt
import time
from datetime import date 

class User: 

    # returns all the users in the users.dat file
    # all the objects returned by this method are instances of the User class
    def all():
        read_obj = open('users.dat', 'rb')
        data = [] 

        while True: 
            try: 
                rec = pickle.load(read_obj)
                data.append(rec)
            except: 
                break 
        read_obj.close()

        users = []

        for rec in data:
            id = rec['id']
            username = rec['username']
            password_digest = rec['password_digest']
            session_token = rec['session_token']
            created_on = rec['created_on']
            user = User(username, None, password_digest, session_token, created_on, id)
            users.append(user)

        return users 

    # updating an existing value in the users.dat file
    # attributes is a hash 
    def update(id, attributes): 
        read_obj = open('users.dat', 'rb')
        data = [] 
        record_updated = False 

        while True: 
            try: 
                rec = pickle.load(read_obj)

                if rec['id'] == id:
                    # if the field is there in attributes hash then it is to be updated (represented here by `attributes.get('username)`)
                    # else we will use the existing value (represented here by `rec.get('username)`))
                    rec['username'] = attributes.get('username') or rec.get('username') # using dict#get as it returns nil instead of error
                    rec['session_token'] = attributes.get('session_token') or rec.get('session_token')

                data.append(rec)
                record_updated = True 
            except:
                break 

        read_obj.close()
        # writing all the data back in the file 

        write_obj = open('users.dat', 'wb')

        for rec in data:
            pickle.dump(rec, write_obj)

        write_obj.close()

        return record_updated

    def destroy(id):
        read_obj = open('users.dat', 'rb')
        data = [] 

        while True: 
            try: 
                rec = pickle.load(read_obj)
                data.append(rec)
            except: 
                break 
        read_obj.close()

        write_obj = open('users.dat', 'wb')

        for rec in data: 
            if rec['id'] != id:
                pickle.dump(rec, write_obj)

        write_obj.close()


    # finding user with id
    def find_by_id(id):
        read_obj = open('users.dat', 'rb')

        while True: 
            try: 
                rec = pickle.load(read_obj)
                if rec['id'] == id: 
                    read_obj.close()
                    username = rec['username']
                    password_digest = rec['password_digest']
                    session_token = rec['session_token']
                    created_on = rec['created_on']
                    return User(username, None, password_digest, session_token, created_on, id)
            except:
                break 
        read_obj.close()
        return None

    def find_by_session_token(session_token):
        read_obj = open('users.dat', 'rb')

        while True: 
            try:
                rec = pickle.load(read_obj)
                if rec['session_token'] == session_token:
                    read_obj.close()
                    id = rec['id']
                    username = rec['username']
                    password_digest = rec['password_digest']
                    session_token = rec['session_token']
                    created_on = rec['created_on']
                    return User(username, None, password_digest, session_token, created_on, id)
            except: 
                break 
        
        read_obj.close()
        return None

    def find_by_credentials(username, password):
        read_obj = open('users.dat', 'rb')

        while True: 
            try: 
                rec = pickle.load(read_obj)
                if rec['username'] == username:
                    read_obj.close()
                    id = rec['id']
                    username = rec['username']
                    password_digest = rec['password_digest']
                    session_token = rec['session_token']
                    created_on = rec['created_on']
                    return User(username, None, password_digest, session_token, created_on, id)

                    if user.check_password(password):
                        return user 
                    else: 
                        return None 
            except: 
                break 
            
        read_obj.close()
        return None
                
    def __init__(self, username, password, password_digest=None, session_token=None, created_on=None, id=None):
        if id:
            self.id = int(id)
        else:
            self.id =  None

        self.username = username 
        self.password = password
        self.password_digest = password_digest or self.__create_password_digest(password) # if a password digest is sent through
                                                                                          # from User#all

        if type(self.password_digest) != bytes: # ensuring that the password digest is only sent through by a class function
            self.password_digest = None 

        self.session_token = session_token
        self.created_on = created_on
        self.errors = []

    def create(self):
        if not (self.valid()):
            return self.errors 
        else: 
            last_id = self.__get_last_user_id()
            id = last_id + 1
            username = self.username 
            password_digest = self.password_digest 
            session_token = self.__generate_session_token()
            created_on = date.today().strftime("%d %B, %Y")

            h = {
                'id': id,
                'username': username, 
                'password_digest': password_digest, 
                'session_token': session_token,
                'created_on': created_on
                }

            write_obj = open('users.dat', 'ab')

            pickle.dump(h, write_obj)

            write_obj.close()

            return User(username, None, password_digest, session_token, id)

    def reset_session_token(self):
        session_token = self.__generate_session_token() 
        User.update(self.id, {'session_token': session_token})
        return session_token

    # ensuring that all the values passed during the initialization of the class are valid
    def valid(self): 
        if type(self.username) != str: 
            self.errors.append('Invalid username.') 
            return False
        elif type(self.password) != str: 
            self.errors.append('Invalid password.')
            return False 
        elif len(self.password) < 6: 
            self.errors.append('Password is too short.')
            return False 
        elif not self.__ensure_unique_username(): 
            self.errors.append('Username already taken.')
            return False 
        
        self.errors = []
        return True 

    def check_password(self, password):
        return bcrypt.checkpw(bytes(password, 'utf-8'), self.password_digest)


    def __create_password_digest(self, password):
        b_password = bytes(password, 'utf-8') # encoding the password 
        hashed_password = bcrypt.hashpw(b_password, bcrypt.gensalt())
        return hashed_password

    def __ensure_unique_username(self): # returns false if username is taken 
        users = User.all() 

        for user in users: 
            if user.username == self.username: 
                return False 
        
        return True 

    def __get_last_user_id(self):
        read_obj = open('users.dat', 'rb')
        i = 0
        read_obj.seek(0, 2)

        while True: 
            try: 
                rec = pickle.load(read_obj)
                break 
            except: 
                try: 
                    i -= 1
                    read_obj.seek(i, 2)
                except: 
                    read_obj.close()
                    return 0

        read_obj.close() 
        print(rec)
        return rec['id']

    def __generate_session_token(self):
        return secrets.token_urlsafe(16)

# User('TestUser1', 'TestUser1Pass').create()
# time.sleep(0.1)
# User('TestUser2', 'TestUser2Pass').create()
# time.sleep(0.1)
# User('TestUser3', 'TestUser3Pass').create()
# time.sleep(0.1)
# User('TestUser4', 'TestUser4Pass').create()

u = User.all()

for x in u: 
    print(x.id)
    print(x.username)
    print(x.password_digest)
    print(x.session_token)
    print(x.created_on)
    print()
# User.destroy(1)
# User.destroy(2)
# User.destroy(3)
# User.destroy(4)
