
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, result_tuple
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()

login_maneger = LoginManager()

login_maneger.init_app(app)


@login_maneger.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(
            email=request.form.get("email"),
            password=generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8),
            name=request.form.get("name")
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return render_template("secrets.html", name=new_user.name, logged_in=True)
        except:
            flash("You already have an acoount registered with that email")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_entered = request.form.get("email")
        user = db.session.execute(db.select(User).where(User.email == email_entered)).scalar()
        if user:
            if check_password_hash(pwhash=user.password, password=request.form.get("password")):
                login_user(user)
                flash("You're successfully logged in")
                return render_template("secrets.html", logged_in=True, name=user.name)
            else:
                flash("The password you entered is not correct")
                return redirect(url_for("login"))
        else:
            flash("The email you entered does not exist")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You're Successfully logged out")
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    return send_from_directory(
        "static", f"files/cheat_sheet.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
