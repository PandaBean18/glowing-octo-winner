# id: integer
# language: string 
# content: string(text)
# post_id: integer
# author_id: integer
# created_on: string (date)

import pickle
from datetime import date

class Snippet: 

    def create_snippet_object(attributes):
        try: 
            id = attributes['id']
            language = attributes['language']
            content = attributes['content']
            post_id = attributes['post_id']
            author_id = attributes['author_id']
            created_on = attributes['created_on']
            return Snippet(language, content, post_id, author_id, created_on, id)
        except (KeyError, EOFError): 
            print("Missing one or more attributes")

    def find_by_id(id): 
        read_obj = open('snippets.dat', 'rb')

        while True: 
            try: 
                rec = pickle.load(read_obj)
                if rec['id'] == id: 
                    read_obj.close()
                    return Snippet.create_snippet_object(rec) 
            except: 
                break 
        read_obj.close()
        return None 


    def find_by_post_id(id): 
        read_obj = open('snippets.dat', 'rb')
        snippets = [] 

        while True: 
            try: 
                rec = pickle.load(read_obj)
                if rec['post_id'] == id: 
                    snippets.append(Snippet.create_snippet_object(rec))
            except: 
                break 
        
        return snippets

    def destroy(id): 
        read_obj = open('snippets.dat', 'rb')
        snippets = [] 

        while True: 
            try: 
                rec = pickle.load(read_obj)
                if rec['id'] != id: 
                    snippets.append(rec)
            except: 
                break 

        read_obj.close()
        write_obj = open('snippets.dat', 'wb')

        for snippet in snippets: 
            pickle.dump(snippet, write_obj)

        write_obj.close()

    def __init__(self, language, content, post_id, author_id, created_on=None, id=None): 
        self.allowed_langs = ['python', 'ruby', 'java', 'rust', 'c++', 'c#']
        self.language = language
        self.content = content 
        self.post_id = post_id
        self.author_id = author_id
        self.created_on = created_on
        self.id = id 
        self.errors = [] 

    # method to find the post to which the snippet belongs 
    def post(self): 
        from posts import Post 
        post = Post.find_by_id(self.post_id)
        return post 

    # method to find the author of the snippet
    def author(self): 
        from users import User 
        author = User.find_by_id(self.author_id)
        return author 

    def create(self): 
        if not self.valid(): 
            return self.errors
        else: 
            id = self.__get_last_snippet_id() + 1
            language = self.language
            content = self.content 
            post_id = self.post_id
            author_id = self.author_id
            created_on = date.today().strftime("%d %B, %Y")

            h = {
                'id': id, 
                'language': language, 
                'content': content, 
                'post_id': post_id, 
                'author_id': author_id, 
                'created_on': created_on
            }

            f = open('snippets.dat', 'ab')

            pickle.dump(h, f)

            f.close()

            return Snippet.create_snippet_object(h)


    def valid(self): 
        self.errors = []
        if self.language == '':
            self.errors.append('Language can\'t be empty.')
            return False 
        elif self.language not in self.allowed_langs: 
            self.errors.append('Language not supported.')
            return False 
        elif not self.__ensure_author_exists(): 
            self.errors.append('Author must exist.')
            return False 
        elif not self.__ensure_post_exists(): 
            self.errors.append('Post must exist.')
            return False 
        return True 

    def __ensure_author_exists(self): 
        if self.author() == None: 
            return False 
        return True 

    def __ensure_post_exists(self): 
        if self.post() == None: 
            return False 
        return True

    def __get_last_snippet_id(self): 
        read_obj = open('snippets.dat', 'rb')
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

    def beautify_snippet(self): 
        keywords = ['def',
                    'class', 
                    'if', 
                    'else', 
                    'end', 
                    'elsif', 
                    'elif', 
                    'try', 
                    'except', 
                    'begin', 
                    'rescue', 
                    'return', 
                    'for', 
                    'while', 
                    'in', 
                    'do', 
                    'fn', 
                    'int',
                    'String'
                ]
        sentences = [] 

        for sent in self.content.split('\r\n'):
            if sent.strip() and sent.strip()[0] == "#": 
                sentences.append(f'<span style=\'color: #7F8487\'>{sent}</span>')
                continue 

            words = [] 
            is_string = False 
            starting_string_char = None 
            i = 0
            w = sent.split(' ')
            while i < len(w):
                word = w[i]
                if len(word) == 0: 
                    i += 1
                    continue
                elif (word[0] == '\'' or word[0] == '"') and not is_string:
                    is_string = True 
                    starting_string_char = word[0]
                    words.append(f"<span style='color: #95CD41'>{word} ")
                elif (word[-1] == '\'' or word[-1] == '"') and is_string and starting_string_char == word[-1]:
                    is_string = False 
                    words[-1] += f"{word}</span>"
                elif is_string: 
                    words[-1] += f"{word} "
                elif word[-1] == ':' and word[0:-1] in keywords:
                    words.append(f"<span style='color: #79DAE8'>{word[0:-1]}</span><span>:</span>")
                elif word[0] == ':':
                    words.append(f"<span style='color: #FF8D29'>{word}</span>")
                elif word in keywords:
                    words.append(f"<span style='color: #79DAE8'>{word}</span>")
                elif sent.split(' ')[i-1] == 'class': 
                    words.append(f"<span style='color: #FFCD38'>{word}</span>")
                elif sent.split(' ')[i-1] == 'def':
                    words.append(f"<span style='color: #0AA1DD'>{word}</span>")
                else: 
                    words.append(word)
                i += 1
            
            sentences.append(f"<span>{' '.join(words)}</span>")

        return self.fix_indent("\r\n".join(sentences))

    def fix_indent(self, new_snippet): 
        i = 0
        sentences = self.content.split('\r\n')
        indented_snippet = [] 
        while i < len(sentences): 
            j = 0 
            x = new_snippet.split('\r\n')[i]
            while sentences[i] and sentences[i][j] and sentences[i][j] == ' ': 
                if x[7:11] == 'span': 
                    x = self.insert(x, ' ', 35)
                else: 
                    x = self.insert(x, ' ', 6)
                
                j += 1

            indented_snippet.append(x)
            i += 1
        return '\r\n'.join(indented_snippet)

    def insert(self, string, char, index):
        new_string = ''
        i = 0 
        for x in string: 
            if i == index: 
                new_string += char 

            new_string += x 
            i += 1
        return new_string 
        
                    