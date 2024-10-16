from flask import Flask, request, redirect, url_for, render_template, abort
app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route('/')   # URL '/' to be handled by main() route handler
def main():
    return render_template("base.html")

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return  render_template("home.html",agent=agent)

@app.route('/hi/<string:name>')  # /hi/ivan?age=30
def greetings(name):
    name = name.upper()
    age = request.args.get("age", 0, int)
    return  render_template("hi.html",name=name,age=age)

@app.route('/admin')
def admin():
    to_url = url_for("greetings", name="administrator", _external=True)    # --> "http://localhost:8080/hi/administrator"
    print(to_url)
    return redirect(to_url)
   
posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
]
@app.route('/posts')
def get_posts():
    return render_template ("posts.html", posts=posts)
    
@app.route('/post/<int:id>')
def detail_post(id):
    if id>3:
        abort(404)
    post= posts[id-1]
    return render_template ("detail_post.html", post=post)
    


if __name__ == "__main__":
    app.run()  # Launch built-in web server and run this Flask webapp, debug=True
 