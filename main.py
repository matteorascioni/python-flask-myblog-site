from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)
app.debug = True

posts = requests.get('https://api.npoint.io/603766b691a02027b90a').json()
post_objects = []
for post in posts:
    post_objects.append(Post(post["id"], post["title"], post["subtitle"], post["body"]))

@app.route('/')
def home():
    return render_template("index.html", all_posts=post_objects)

@app.route('/post/<int:route_id>')
def post_route(route_id):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == route_id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
