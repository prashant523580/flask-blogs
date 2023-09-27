from flask import Blueprint
import os
import secrets
from PIL  import Image
from flask import render_template, request
from flaskblog.models import User,Post
from flask_login import login_user , current_user,logout_user ,login_required
from flask_mail import Message 
main = Blueprint("main", __name__)

@main.route("/")
def home():
    posts= Post.query.all()
    return render_template("home.html", posts=posts)

@main.route("/about")
def about():
    return render_template("about.html", title="About Page")
@main.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Page")
@main.route("/blogs")
def blogs():
     page = request.args.get('page',1,type=int)
     posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
     return render_template("blogs.html", posts=posts, title="Blogs")

