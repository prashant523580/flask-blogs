from flask import Blueprint
from PIL  import Image
from flask import render_template, url_for, flash ,redirect,request,abort
from flaskblog import  db,bcrypt
from flaskblog.models import User,Post
from flaskblog.users.forms import (RegistrationForm,LoginForm, UpdateAccountForm,
                             ResetPasswordForm,RequestResetForm)
from flask_login import login_user , current_user,logout_user ,login_required
from flask_mail import Message 
from flaskblog.users.utils import save_picture ,send_reset_email
users = Blueprint('users', __name__)

@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data,email=form.email.data,password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created!{form.username.data}.","green") #success
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # decrypt_password = bcrypt.check_password_hash(user.password, form.password.data)
        # print(user.password)
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for("main.home"))
        else:
            flash(f"Login failed. Please check email and password","red")
    return render_template("login.html", title="Login", form=form )

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET","POST"])
@login_required  #login required to access route
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
         if form.picture.data:
             picture_file = save_picture(form.picture.data)
             current_user.image_file = picture_file
             
         current_user.username = form.username.data
         current_user.email = form.email.data
         db.session.commit()
         flash("Updated Successfully.", "green")
         return redirect(url_for("users.account"))
    elif request.method == "GET":
         form.username.data = current_user.username
         form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/"+ current_user.image_file)
    return render_template("account.html", Title="Account", image_file=image_file, form=form )


@users.route("/user/<string:username>")
def user_posts(username):
     page = request.args.get('page',1,type=int)
     user = User.query.filter_by(username=username).first_or_404()
    #  
     posts=Post.query.filter_by(author=user)\
                .order_by(Post.date_posted.desc())\
                .paginate(page=page,per_page=5)
     return render_template("user_post.html", posts=posts, user=user,title="User posts")


@users.route("/reset_password", methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user) 
        flash("An email has been sent with instructions to reset", 'green')
        return redirect(url_for("users.login"))
    return render_template('reset_request.html', title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET","POST"])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an Invalid or Expired token", "red")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hash_password
        db.session.commit()
        flash(f"Your password has been updated! You are now able to login","green") #success
        return redirect(url_for("users.login"))
    return render_template('reset_token.html', title="Reset Password", form=form)