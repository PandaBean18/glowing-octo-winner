This webapp is my 12th grade cs summer hhw built using [flask](https://flask.palletsprojects.com/en/2.1.x/)

Its basically a webapp where people can create posts explaining a programming
concept as pseudo code and then add code snippets to it in various languages to implement it. Anyone can add snippets to a post
so one post can have snippets in various languages.

# The Backend
The design of the application is based off of MVC architecture 

### The Data
Since I was not allowed to use Databases for this particular project, I have used binary (.dat) files for storing data as hashes

### Models 
Each model is a layer of python code that deals with CRUD operations of the data. They are python classes for different types of data (users, posts and snippets)
which have various class methods and instance methods to make CRUD operations easier. All these classes directly access the .dat files
[users.py](/users.py), [posts.py](/posts.py) and [snippets.py](/snippets.py) all have proper documentation as comments 

### Views 
All the views are html css files with [jinja template engine](https://jinja.palletsprojects.com/en/3.1.x/) for basic logic handling 

### Controllers 
All the controllers are python functions, stored in [main.py](/main.py)

### Syntax Highlighting in snippets
This was my most fav part of the project. The basic logic for this is stored in [Snippet](/snippets.py)#beautify_snippet() method. In a normal project I would 
use highlight-js for this but I wanted to keep the use of languages other then python to a minimal as it was a school project

# The application
I have not hosted the application as of now but here are some images of the final website:

Sign up:

<img src="https://cdn.discordapp.com/attachments/844189298030673940/1003200009627508786/unknown.png" width="500">

Home: 

<img src="https://cdn.discordapp.com/attachments/844189298030673940/1003211596341981234/unknown.png" width="500">

Post show: 

<img src="https://cdn.discordapp.com/attachments/844189298030673940/1003211326933434418/unknown.png" width="500">

<img src="https://cdn.discordapp.com/attachments/844189298030673940/1003211342410416208/unknown.png" width="500">

New post: 

<img src="https://cdn.discordapp.com/attachments/844189298030673940/1003730830725763102/unknown.png" width="500">

New snippet: 

<img src="https://cdn.discordapp.com/attachments/844189298030673940/1003731213690884166/unknown.png" width="500">

New post (error in submission):

<img src="https://cdn.discordapp.com/attachments/844189298030673940/1003731426354675732/unknown.png" width="500">