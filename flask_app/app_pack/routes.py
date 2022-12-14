from app_pack import app, render_template, request
from models import storage


@app.errorhandler(404)
def errorHandler(error):
    return render_template("error404.html")

@app.route("/")
def index():
    """index route of the site"""
    return render_template("index.html")

@app.route("/rooms")
def rooms():
    """rooms route to return the list of all rooms"""
    roomsList = [room for room in storage.all("Room").values()]
    newDict = []
    for user in storage.all("User").values():
        for room in storage.all("Room").values():
            if room.creator_id == user.id:
                newDict.append({'userName': user.name, 'roomName': room.name, 'roomDescription': room.description})
    return render_template("rooms.html", rooms=roomsList, roomDetails=newDict)

@app.route("/about")
def about():
    """about page route"""
    return render_template("about.html")

@app.route("/signup", methods=["Get", "POST"])
def signup():
    """creating new users"""
    return render_template("signup.html")
#     from app_pack.validation import SignupForm
#     if request.method == "POST":
#         pass


@app.teardown_appcontext
def close(close_session):
    """closes a session"""
    storage.close()
