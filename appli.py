from flask import Flask,session, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#----
from flask_login import (
                            LoginManager, 
                            UserMixin, 
                            login_user, 
                            login_required, 
                            current_user, 
                            logout_user
                        )

app = Flask(__name__)
app.config.from_pyfile("./config.py")
app.app_context().push()
#
login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message = "Connecter vous pour acceder a cette page!!!😜"

db = SQLAlchemy(app)
migrate = Migrate(app,db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return "<h1>Index</h1>"

@app.route("/login", methods=["GET","POST"])
def login():
    # user = User.query.filter_by(username="aly").first()
    # Sauvegarder l'utilisateur connecte
    # login_user(user)
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username = username).first()
        if not user:
            return "<h1>Vas creer un compte!😎</h1>"
        # login_user(user,remember=True)
        login_user(user)
        if 'next' in session:
            next = session["next"]
            if next is not None:
                return redirect(next)
        session["next"] = request.args.get("next")
        # return "<h1>Vous etes bien connecte!🤙🏾</h1>"
    return render_template("login.html")

@app.route("/home")
@login_required
def home():
    return "<h1>Welcome  {}</h1>".format(current_user.username)

@app.route("/profile")
@login_required
def profile():
    return "<h1>Profile de  {}</h1>".format(current_user.username)

@app.route("/logout")
def logout():
    logout_user()
    return "<h1>Vous vous etes deconnecte!!!</h1>"


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer, default=12)




if __name__ == "__main__":
    app.run(debug=True)