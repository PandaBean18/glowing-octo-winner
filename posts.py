# id: integer 
# title: string
# body: string
# author_id: integer 
# created_on: string (date)
import pickle 
from datetime import date

class Post:
    
    def create_post_object(attributes):
        try: 
            id = attributes['id']
            title = attributes['title']
            body = attributes['body']
            author_id = attributes['author_id']
            created_on = attributes['created_on']
            return Post(title, body, author_id, created_on, id)
        except KeyError:
            raise "Missing one or more attributes." 

    # update post attributes with the given id
    def update(id, attributes): 
        read_obj = open('posts.dat', 'rb')
        record_updated = False 
        posts = []

        while True:
            try:
                rec = pickle.load(read_obj)

                if rec['id'] == id: 
                    rec['title'] = attributes.get('title') or rec['title']
                    rec['body'] = attributes.get('body') or rec['body']
                    record_updated = True
                
                posts.append(rec)
            except: 
                break 

        read_obj.close()
        write_obj = open('posts.dat', 'wb')

        for post in posts: 
            pickle.dump(post, write_obj)

        write_obj.close()
        return record_updated

    # returns all the users in the posts.dat file
    # all the objects returned by this method are instances of the User class
    def all():
        read_obj = open('posts.dat', 'rb')
        data = [] 

        while True: 
            try: 
                rec = pickle.load(read_obj)
                data.append(rec)
            except: 
                break 
        read_obj.close()

        posts = []

        for rec in data:
            post = Post.create_post_object(rec)
            posts.append(post)

        return posts 

    def destroy(id):
        read_obj = open('posts.dat', 'rb')
        data = [] 

        while True: 
            try: 
                rec = pickle.load(read_obj)
                data.append(rec)
            except: 
                break 
        read_obj.close()

        write_obj = open('posts.dat', 'wb')

        for rec in data: 
            if rec['id'] != id:
                pickle.dump(rec, write_obj)

        write_obj.close()


    # finding post with id
    def find_by_id(id):
        read_obj = open('posts.dat', 'rb')

        while True: 
            try: 
                rec = pickle.load(read_obj)
                if rec['id'] == id: 
                    read_obj.close()
                    post = Post.create_post_object(rec)
                    return post
            except:
                break 
        read_obj.close()
        return None

    def __init__(self, title, body, author_id, created_on=None, id=None):
        self.title = title 
        self.body = body
        self.author_id = author_id
        self.created_on = created_on 
        self.id = id 
        self.errors = []

    def author(self): 
        from users import User
        return User.find_by_id(self.author_id)

    def create(self):
        if self.valid(): 
            id = self.__get_last_post_id() + 1
            title = self.title 
            body = self.body
            author_id = self.author_id
            created_on = date.today().strftime("%d %B, %Y")

            post = {
                'id': id,
                'title': title,
                'body': body, 
                'author_id': author_id, 
                'created_on': created_on
            }

            write_obj = open('posts.dat', 'ab')
            pickle.dump(post, write_obj)
            write_obj.close() 
            return Post(title, body, author_id, created_on, id)
        else: 
            return self.errors 

    def valid(self): 
        from users import User
        if len(self.title) == 0: 
            self.errors.append('Title can\'t be empty.')
            return False 
        elif len(self.body) == 0:
            self.errors.append('Body can\'t be empty.')
            return False 
        elif not (User.find_by_id(self.author_id)): 
            self.errors.append('User must exist')
            return False 
        self.errors = []
        return True 

    def __get_last_post_id(self):
        read_obj = open('posts.dat', 'rb')
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
            
    