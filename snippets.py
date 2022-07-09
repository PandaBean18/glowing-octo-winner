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

        def __init__(self, language, content, post_id, author_id, created_on=None, id=None): 
            pass 