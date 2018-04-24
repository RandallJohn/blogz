from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode1@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.completed = True



@app.route('/blog', methods=['POST', 'GET'])
def index():

    blog = Blog.query.all()  #gets a list of: querying all rows on the 'Blog' table (aka object) within the database = returns all feilds in a list format
    #completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html', blog=blog, title="build-a-blog") #renders blog.html passes on newly formed 'blog' list data on into blog.html




def is_filled(text):

    if text != "":
        return True
    else:   
        return False



@app.route('/newpost', methods=['GET', 'POST'])

def create_blog():
    if request.method == "GET":
        return render_template('newpost.html')

    else:
        if request.method == "POST":
            title = request.form['title']
            body = request.form['body']

            title_error = ''
            body_error = ''

            if not is_filled(title):
                title_error = 'Please fill in title'
                title = ''
    
            if not is_filled(body):
                body_error = 'Please fill in body'
                body=''

            if not title_error and not body_error:
                blog_title = request.form['title']
                blog_body = request.form['body']

                new_blog = Blog(blog_title, blog_body) #creating a new blog
                db.session.add(new_blog)
                db.session.commit()

                blog_id = new_blog.id

                #blog_id = int(request.form['blog-id'])
                
                
                return redirect('/new_blog?blog_id={0}'.format(blog_id))  #new page using pulling blog id from new blog object
            
            else:
                return render_template('newpost.html', title_error = title_error, body_error=body_error, body=body, title=title)

@app.route('/new_blog')
def blog_temp():
    blog_id = request.args.get('blog_id')
    blog = Blog.query.get(blog_id) 
    title = blog.title
    body = blog.body
        
    return render_template('new_blog.html', title = title, body = body )


#@app.route('/newpost', methods = ['POST'])
#def validate_blog_form():

    #title = request.form['title']
    #body = request.form['body']

    #title_error = ''
    #body_error = ''

    #if not is_filled(title):
        #title_error = 'Please fill in title'
        #title = ''
    
    #if not is_filled(body):
        #body_error = 'Please fill in body'
        #body=''

    #if not title_error and not body_error:
        #return 'Good'
    #else:
        #return render_template('newpost.html', title_error = title_error, body_error=body_error, body=body, title=title)


##################################################

    #blog_id = int(request.form['blog-id'])
    #blog = Blog.query.get(blog_id)
    #task.completed = True
    #db.session.add(blog)
    #db.session.commit()

###################################################

if __name__ == '__main__':
    app.run()
