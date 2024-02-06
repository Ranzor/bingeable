import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required

app = Flask(__name__)

img_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images')
extensions = set(["png", "jpg", "jpeg"])

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = img_folder
Session(app)

db = SQL("sqlite:///comics.db")





@app.route("/", methods=["GET","POST"])
@login_required
def index():

    comic_series = db.execute("SELECT * FROM comic_series")
    binges = db.execute("SELECT * FROM binges WHERE user_id = ?",session["user_id"])
    writers = db.execute("SELECT * FROM writers")
    artists = db.execute("SELECT * FROM artists")
    reading_list = db.execute("SELECT * FROM reading_list WHERE user_id = ?",session["user_id"] )

    return render_template("index.html", comic_series=comic_series, binges=binges, writers=writers, artists=artists,reading_list=reading_list,)


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            error = "Must provide username"
            return render_template("login.html", error=error)
        elif not request.form.get("password"):
            error = "Must provide password"
            return render_template("login.html", error=error)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not (check_password_hash(rows[0]["hash"], request.form.get("password"))):
            error = "Invalid username or password"
            return render_template("login.html", error=error)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method =="POST":        
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            error = "Username already used"
            return render_template("register.html", error=error)
        else:
            user = request.form.get("username")
            if user == "":
                error = "please provide a username"
                return render_template("register.html", error=error)
            
            pwa = request.form.get("password")
            pwb = request.form.get("confirmation")
            if not pwa == pwb:
                error = "Both passwords must be identical"
                return render_template("register.html", error=error)            
            if pwa == "" or pwb == "":
                print("pwa : " + pwa)
                print("pwb : " + pwb)
                error = "please provide a password"
                return render_template("register.html", error=error)

            pw = generate_password_hash(request.form.get("password"))                          
            db.execute("INSERT INTO users(username, hash) VALUES(?,?)", user, pw)
            user_info = db.execute("SELECT id FROM users WHERE username = ?", user)
            session["user_id"] = user_info[0]["id"]
            return redirect("/")                    
    else:
        return render_template("register.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@app.route("/writers", methods=["GET", "POST"])
@login_required
def writers():
    if request.method == "POST":
        img = request.files['image']

        if img and allowed_file(img.filename):
            imgname = secure_filename(img.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], imgname))
        else:
            imgname = ""

        name = request.form.get("name")
        desc = request.form.get("desc")

        if name:
            db.execute("INSERT INTO writers(name, desc, img) VALUES(?,?,?)", name, desc, imgname)   
        else:
            error = "Please enter name to create a new entry"
            return render_template("writers.html", error=error)

        return redirect("/")        

    else:
        return render_template("writers.html")

@app.route("/artists", methods=["GET", "POST"])
@login_required
def artists():
    if request.method == "POST":
        img = request.files['image']

        if img and allowed_file(img.filename):
            imgname = secure_filename(img.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], imgname))
        else:
            imgname = ""

        name = request.form.get("name")
        desc = request.form.get("desc")

        if name:
            db.execute("INSERT INTO artists(name, desc, img) VALUES(?,?,?)", name, desc, imgname)   
        else:
            error = "Please enter name to create a new entry"
            return render_template("artists.html", error=error)

        return redirect("/")        

    else:
        return render_template("artists.html")


@app.route("/publishers", methods=["GET", "POST"])
@login_required
def publishers():
    if request.method == "POST":
        img = request.files['image']

        if img and allowed_file(img.filename):
            imgname = secure_filename(img.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], imgname))
        else:
            imgname = ""

        name = request.form.get("name")

        if name:
            db.execute("INSERT INTO publishers(name, img) VALUES(?,?)", name, imgname)   
        else:            
            error = "Please enter name to create a new entry"
            return render_template("publishers.html", error=error)

        return redirect("/")        

    else:
        return render_template("publishers.html")

@app.route("/series", methods=["GET", "POST"])
@login_required
def series():
    publishers = db.execute("SELECT * FROM publishers")

    if request.method == "POST":
        img = request.files['image']

        if img and allowed_file(img.filename):
            imgname = secure_filename(img.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], imgname))
        else:
            imgname = ""

        name = request.form.get("name")
        try:
            year = int(request.form.get("year"))
        except:
            error = "Please enter a valid year"
            return render_template("series.html", error=error, publishers=publishers)
        desc = request.form.get("desc")
        
        try:
            publisher = int(request.form.get("publisher"))
        except:
            error = "Please enter a valid publisher"
            return render_template("series.html", error=error, publishers=publishers)
        
        if name:
            db.execute("INSERT INTO comic_series(name, year, desc, publisher_id, img) VALUES(?,?,?,?,?)", name, year, desc, publisher, imgname)   
        else:
            error = "Please enter a name to create a new series"
            return render_template("series.html", error=error, publishers=publishers)

        return redirect("/")        

    else:
        return render_template("series.html", publishers=publishers)

@app.route("/binge", methods=["GET", "POST"])
@login_required
def binge():
    if request.method == "POST":        
        title = request.form.get("title")
        if title:
            db.execute("INSERT INTO binges(user_id, title) VALUES(?,?)", session["user_id"], title)
        else:
            error = "Please enter name to create a new binge"
            return render_template("binge.html", error=error)
        return redirect("/")
    else:
        return render_template("binge.html")


@app.route("/addissue", methods=["GET", "POST"])
@login_required
def addissue():
    comic_series = db.execute("SELECT * FROM comic_series")
    binges = db.execute("SELECT * FROM binges WHERE user_id = ?",session["user_id"])
    writers = db.execute("SELECT * FROM writers")
    artists = db.execute("SELECT * FROM artists")
    reading_list = db.execute("SELECT * FROM reading_list WHERE user_id = ?",session["user_id"] )
    binge = request.form.get("binge")
    setBinge = request.form.get("setbinge")

    if request.method == "POST":

        
        if binge:
            binge = db.execute("SELECT * FROM binges WHERE id = ?", binge)
            return render_template("addissue.html", comic_series=comic_series,binges=binges, writers=writers, artists=artists, reading_list=reading_list, binge=binge[0])

        
        comic_id = request.form.get("series")
        user_id = session["user_id"]
        issue = request.form.get("issue")
        writer_id = request.form.get("writer")
        artist_id = request.form.get("artist")
        have_read = 0
        desc = request.form.get("desc")
        binge = request.form.get("binge")

        stop = 0        
        if not comic_id:
            stop = 1
            flash("please select a series")
        if not issue:
            stop = 1
            flash("please enter issue number")
        if not writer_id:
            stop = 1
            flash("please select a writer")
        if not artist_id:
            stop = 1
            flash("please select an artist")

        if stop == 1:          
            return redirect("/")

        db.execute("INSERT INTO reading_list(issue, user_id, comic_id, writer_id, artist_id, have_read, desc, binge_id) VALUES(?,?,?,?,?,?,?,?)", issue, user_id, comic_id, writer_id, artist_id, have_read, desc, setBinge)

        return redirect("/")
    else:
        return render_template("addissue.html", comic_series=comic_series,binges=binges, writers=writers, artists=artists, reading_list=reading_list, binge=binge[0])
    

@app.route("/updatedesc", methods=["GET", "POST"])
@login_required
def updatedesc():

    if request.method == "POST":
        desc = request.form.get("desc")
        issue = request.form.get("issue")
        db.execute("UPDATE reading_list SET desc = ? WHERE id = ?", desc, issue)

    return redirect("/")

@app.route("/read", methods=["GET", "POST"])
@login_required
def read():

    if request.method == "POST":
        read = request.form.get("read")
        issue = request.form.get("issue")

        db.execute("UPDATE reading_list SET have_read = ? WHERE id = ?", read, issue)
    return redirect("/")

@app.route("/deleteissue", methods=["GET", "POST"])
@login_required
def deleteissue():
    if request.method == "POST":
        issue = request.form.get("issue")
        db.execute("DELETE FROM reading_list WHERE id = ?", issue)

    return redirect("/")

@app.route("/deletebinge", methods=["GET","POST"])
@login_required
def deletebinge():
    if request.method == "POST":
        binge = request.form.get("binge")
        db.execute("DELETE FROM binges WHERE id = ?", binge)
        db.execute("DELETE FROM reading_list WHERE binge_id = ?", binge)
    return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        user = session["user_id"]
        name = request.form.get("name")
        person = db.execute("SELECT * from writers WHERE name = ?", name)
        creator = "writer"
        if len(person) != 1:
            person = db.execute("SELECT * FROM artists WHERE name = ?", name)
            creator = "artist"
        if len(person) != 1:
            return redirect("/")
        
        if creator == "writer":            
            reading_list = db.execute("SELECT * FROM reading_list WHERE writer_id = (SELECT id FROM writers WHERE name = ?)", name)
        else:
            reading_list = db.execute("SELECT * FROM reading_list WHERE artist_id = (SELECT id FROM artists WHERE name = ?)", name)
        
        print(name)
        print(reading_list)

        comic_series = db.execute("SELECT * FROM comic_series")
        return render_template("profile.html", person=person[0], reading_list=reading_list, comic_series=comic_series, user=user, creator=creator)
    else:
        return redirect("/")