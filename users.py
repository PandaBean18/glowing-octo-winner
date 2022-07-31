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
from posts import Post 
class User: 
    def create_user_object(attributes):
        try: 
            id = attributes['id']
            username = attributes['username']
            password_digest = attributes['password_digest']
            session_token = attributes['session_token']
            created_on = attributes['created_on']
            return User(username, None, password_digest, session_token, created_on, id)
        except (KeyError, EOFError): 
            #raise Exception("Missing one or more attributes.")
            print("Missing one or more attributes.")

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
            user = User.create_user_object(rec)
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

    # deleting a record w id = id
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
                    return User.create_user_object(rec)
            except:
                break 
        read_obj.close()
        return None

    # finding a user by session token
    def find_by_session_token(session_token):
        read_obj = open('users.dat', 'rb')

        while True: 
            try:
                rec = pickle.load(read_obj)
                if rec['session_token'] == session_token:
                    read_obj.close()
                    return User.create_user_object(rec)
            except: 
                break 
        
        read_obj.close()
        return None

    # finding user with a particular username and password 
    # first finds a user w the given username (will never have multiple users with the same username)
    # then checks if password digest matches
    def find_by_credentials(username, password):
        read_obj = open('users.dat', 'rb')

        while True: 
            try: 
                rec = pickle.load(read_obj)
                if rec['username'] == username:
                    read_obj.close()
                    user = User.create_user_object(rec)
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
    
    # returns a list of all the posts authored by the user
    # eqv to rails has_many relation
    def posts(self): 
        read_obj = open('posts.dat', 'rb')
        posts = [] 

        while True: 
            try: 
                rec = pickle.load(read_obj)
                if rec['author_id'] == self.id: 
                    p = Post.create_post_object(rec)
                    posts.append(p)
            except:
                break 

        read_obj.close() 
        return posts 

    # creating an instance of the user in .dat file
    def create(self):
        if not (self.valid()): # ensuring that the user instance is valid
            return self.errors # returning the list of errors, used later to flash errors
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

            return User.create_user_object(h)

    # reseting a user's session token. 
    # updates user's session token in the .dat file and returns it as well
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

    # checking if stored password (digest) and given passwords match
    def check_password(self, password):
        return bcrypt.checkpw(bytes(password, 'utf-8'), self.password_digest)

    # private methods 

    # creating password digest, only called by class's #create() function
    def __create_password_digest(self, password):
        b_password = bytes(password, 'utf-8') # encoding the password 
        hashed_password = bcrypt.hashpw(b_password, bcrypt.gensalt())
        return hashed_password

    # returns false if username is taken
    def __ensure_unique_username(self):  
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
        return rec['id']

    # generates session token lul
    def __generate_session_token(self):
        return secrets.token_urlsafe(16)

