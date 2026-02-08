from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv()
URL = "https://api.themoviedb.org/3/search/movie"
api_access_token = os.getenv("API_ACCESS_TOKEN")
api_secret_key = os.getenv("API_SECRET_KEY")



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)






# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///best-movies.db"
db.init_app(app)

# CREATE TABLE


class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()

# new_movie = Movie(title="Phone Booth", year=2002,
#                   description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by"
#                               " an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's"
#                               " negotiation with the caller leads to a jaw-dropping climax.",
#                   rating=7.3,
#                   ranking=10,
#                   review="My favourite character was the caller.",
#                   img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#                   )
#
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()
#
#     second_movie = Movie(
#         title="Avatar The Way of Water",
#         year=2022,
#         description="Set more than a decade after the events of the first film, learn the story of the Sully family"
#                     " (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep"
#                     " each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#         rating=7.3,
#         ranking=9,
#         review="I liked the water.",
#         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#     )
#
# with app.app_context():
#     db.session.add(second_movie)
#     db.session.commit()

class UpdateRating(FlaskForm):
    rating = FloatField(label="Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")

class AddMovie(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    movies = result.scalars().all()
    movies_count = len(movies)
    for movie in movies:
        if movies_count != 0:
            movie.ranking = movies_count
            movies_count -= 1
    return render_template("index.html", movies=movies)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_rating(id):
    update_rating_form = UpdateRating()
    if update_rating_form.validate_on_submit():
        target_movie = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        target_movie.rating = update_rating_form.rating.data
        target_movie.review = update_rating_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=update_rating_form)

@app.route("/delete/<int:id>")
def delete(id):
    target_movie = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    db.session.delete(target_movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    add_movie_form = AddMovie()
    if add_movie_form.validate_on_submit():

        headers = {"accept": "application/json",
                   "Authorization": f"Bearer {api_access_token}"}
        parameters = {
            "query": f"{add_movie_form.title.data}"
        }

        response = requests.get(URL, headers=headers, params=parameters)
        data = response.json()
        all_movies = data["results"]
        return render_template("select.html", movies=all_movies)
    return render_template("add.html", form=add_movie_form)


@app.route("/selected/<title>/<year>/<desc>")
def add_selected(title, year, desc):
    img_path = request.args.get("img")
    new_movie = Movie(
        title=title,
        year=year,
        description=desc,
        img_url=f"https://image.tmdb.org/t/p/w500{img_path}"
    )
    db.session.add(new_movie)
    db.session.commit()

    movie = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
    return redirect(url_for('edit_rating', id=movie.id))




if __name__ == '__main__':
    app.run(debug=True)
# {{ url_for('add_selected', title= movie['title'], year=movie['release_date'][:4], desc= movie['overview'], img_path= movie['poster_path'])}}