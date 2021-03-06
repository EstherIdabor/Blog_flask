from flask import Flask, render_template,  redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class BlogPst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default = 'N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __repr__(self):
        return 'BlogPost ' + str(self.id)


@app.route('/posts', methods=['GET', 'POST'])
def post():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPst(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/home')
    else:
        all_posts = BlogPst.query.order_by(BlogPst.date_posted).all()     
        return render_template('post.html', posts = all_posts) 

@app.route('/home')
def index():
    all_posts = BlogPst.query.order_by(BlogPst.date_posted).all()
    return render_template('index.html', posts = all_posts)         

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPst.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def Edit(id):
    post = BlogPst.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:    
        return render_template('edit.html', post = post) 

@app.route('/newpost', methods = ['GET', 'POST'])    
def New_Post():
    return render_template('new_post.html')  
    


if __name__ == "__main__":
    app.run(debug=True)    