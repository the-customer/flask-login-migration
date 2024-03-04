from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#----
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user

app = Flask(__name__)
app.config.from_pyfile("./config.py")
app.app_context().push()
#
login_manager = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return "<h1>Index</h1>"

@app.route("/login")
def login():
    user = User.query.filter_by(username="aly").first()
    # Sauvegarder l'utilisateur connecte
    login_user(user)
    return "<h1>Vous vous etes connecte!!!</h1>"

@app.route("/home")
@login_required
def home():
    return "<h1>Welcome  {}</h1>".format(current_user.username)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer, default=12)



if __name__ == "__main__":
    app.run(debug=True)