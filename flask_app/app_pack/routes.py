import csv
import hashlib
import secrets
from datetime import datetime

from app_pack import (app, current_user, flash, login_manager,
                      login_required, login_user, logout_user,
                      redirect, render_template, request, url_for)
from app_pack.validation import LoginForm, ProfileForm, RoomForm, SignupForm

from models import storage
from models.rooms import Room
from models.users import User

from os import path


@login_manager.user_loader
def load_user(user_id):
    """funtion to load user session"""
    return storage.get("User", user_id)


@app.errorhandler(404)
def errorHandler(error):
    """handles 404 error occurences"""
    return render_template("error404.html")


@app.errorhandler(401)
def errorHandler401(error):
    """handles 401 error occurences"""
    return redirect(url_for('login'))


@app.route("/")
def index():
    """index route of the site"""
    return render_template("index.html")


@app.route("/rooms", methods=["GET", "POST"])
@login_required
def rooms():
    """login route function"""
    """rooms route to return the list of all rooms"""
    form = RoomForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            newRoom = Room(name=form.name.data,
                           description=form.description.data,
                           creator_id=current_user.id)
            storage.new(newRoom)
            storage.save()
        num = 0
        roomsList = []
        for room in storage.all("Room").values():
            roomsList.append(room)
            num += 1
            if num == 5:
                break
        newDict = []
        for user in storage.all("User").values():
            for room in storage.all("Room").values():
                if room.creator_id == user.id:
                    newDict.append({'userName': user.name,
                                    'roomName': room.name,
                                    'roomDescription': room.description,
                                    'created_at': room.created_at,
                                    'profileImg': user.profile_image})
        return render_template("rooms.html", userName=current_user.name,
                               rooms=roomsList, roomDetails=newDict, form=form)
    # else:
    return redirect(url_for('login'))


@app.route("/chatroom/<user_id>/<room_id>")
@app.route("/chatroom")
@login_required
def chatroom(user_id=None, room_id=None):
    """the chat space route"""
    # all_messages = storage.all("Message")
    all_messages = [message for message in storage.all("Message").values()
                    if message.room_id == room_id]
    for i in range(len(all_messages)):
        if all_messages[i].created_at < all_messages[i + 1].created_at:
            all_messages[i], all_messages[i + 1] = all_messages[i + 1],\
                all_messages[i]
    return render_template("chatroom.html", messages=all_messages)


@app.route("/about/<user_id>")
@app.route("/about")
def about(user_id=None):
    """about page route"""
    return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """creating new users"""
    form = SignupForm()
    if form.validate_on_submit():
        with open('file.csv', 'a', encoding='utf-8') as file:
            objects = [form.name.data, form.email.data, form.password1.data]
            writer = csv.writer(file)
            writer.writerow(objects)

        passwordHash = hashlib.md5(
            form.password1.data.encode('utf-8')).hexdigest()
        newUser = User(name=form.name.data, email=form.email.data,
                       number=form.number.data,
                       password=passwordHash)
        storage.new(newUser)
        storage.save()
        return redirect(url_for('rooms'))
    return render_template("signup.html", form=form)


def save_image(fileImage):
    """saves the image file"""
    a_hex = secrets.token_hex(8)
    _, f_ext = path.splitext(fileImage.filename)
    picName = a_hex + f_ext
    picPath = path.join(app.root_path, app.config['UPLOADS_FOLDER'], picName)
    fileImage.save(picPath)
    return picName


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    """user profile page"""
    form = ProfileForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.profileImg.data:
                fileName = save_image(form.profileImg.data)
                current_user.profile_image = fileName
            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.number = form.number.data
            setattr(current_user, 'updated_at', datetime.utcnow())
            storage.save()
            return redirect(url_for('profile'))
        # add an error checker here
    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.number.data = current_user.number
    return render_template('profile.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """login route for the app"""
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.getBy_email("User", form.email.data)
        if user is None:
            return render_template('login.html', form=form)
        passwordHash = hashlib.md5(
            form.password.data.encode('utf-8')).hexdigest()
        if user.password == passwordHash:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('rooms'))
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    """logout and clear user session"""
    logout_user()
    return redirect(url_for('index'))


@app.teardown_appcontext
def close(close_session):
    """closes a session"""
    storage.close()
