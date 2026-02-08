from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


app = Flask(__name__)


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()





@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = request.form
        data_dict = data.to_dict(flat=True)
        new_book = Book(title=data_dict['title'], author= data_dict['author'], rating= data_dict['rating'])
        with app.app_context():
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        new_rating = request.form.to_dict()['rating']
        target_book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        target_book.rating = new_rating
        db.session.commit()
        return redirect(url_for("home"))
    target_book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    return render_template("rating.html", book=target_book)


@app.route("/delete/<int:id>")
def delete(id):
    target_book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    db.session.delete(target_book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

