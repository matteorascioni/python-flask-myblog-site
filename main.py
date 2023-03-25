from flask import Flask, render_template, request
from datetime import datetime
import requests
import smtplib
import os

MY_EMAIL = os.environ.get('MY_EMAIL') #Put your email here
MY_PASSWORD = os.environ.get('MY_PASSWORD') #Put your AppPassword (take a look in google account -> Security --> App Password)

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

@app.route("/contact", methods=["GET", "POST"])
def contact():
    is_data_sent = False
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        message = request.form["message"]
        send_email(name=name, email=email, phone=phone_number, message=message)
        return render_template("contact.html", year=year, is_data_sent=True)
    return render_template("contact.html", year=year, is_data_sent=False)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(MY_EMAIL, MY_EMAIL, email_message)

if __name__ == "__main__":
    app.run(debug=True)