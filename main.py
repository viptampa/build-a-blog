from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ok@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(120))
   body = db.Column(db.String(500))

   def __init__(self, title, body):
       self.title = title
       self.body = body

@app.route('/blog', methods=['GET'])
def display_post():
   posts = Blog.query.all()
   if len(request.args) != 0:
       writeup_id = request.args.get("id")
       writeup = Blog.query.get(writeup_id)

       return render_template('writeup.html', writeup=writeup)

   return render_template('blog.html', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
   if request.method == 'POST':
       title = request.form['title']
       body = request.form['body']

       

       if title == "" or body == "":
           if title == "":
               title_error = "Please enter a title"
           if body == "":
               body_error = "Please enter a post body"
           return render_template('/newpost.html', title=title, body=body, title_error=title_error, body_error=body_error)
       else:
           post = Blog(title, body)
           db.session.add(post)
           db.session.commit()

           body_id = str(post.id)
           return redirect("/blog?id=" + body_id)

   return render_template('/newpost.html')
     

@app.route('/', methods=['POST', 'GET'])
def index():

   if request.method == 'POST':
       blog_title = request.form['title']
       new_blog = Blog(blog_title)
       db.session.add(new_blog)
       db.session.commit()

   blogs = Blog.query.all()
   return render_template('blog.html',title="Blog!", blogs=blogs)




if __name__ == '__main__':
app.run()