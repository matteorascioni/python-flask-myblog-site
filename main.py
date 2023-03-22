from flask import Flask, render_template
from datetime import datetime
import requests

posts = requests.get('https://api.npoint.io/603766b691a02027b90a').json()
app = Flask(__name__)
current_time = datetime.now()
year = current_time.year

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts, year=year)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post, year=year)

@app.route("/about")
def about():
    return render_template("about.html", year=year)

@app.route("/contact")
def contact():
    return render_template("contact.html", year=year)

if __name__ == "__main__":
    app.run(debug=True)
