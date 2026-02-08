import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)



class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/random", methods=["GET"])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe)).scalars()
    all_cafes = result.all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    result= db.session.execute(db.select(Cafe)).scalars()
    all_cafes = result.all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def cafe_search():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location)).scalars().all()
    if result:
        return jsonify(cafes=[cafe.to_dict() for cafe in result])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=request.form.get("coffee_price"),
    )
    if new_cafe:
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"Success": "Successfully added the new cafe"})
    else:
        pass


@app.route("/update_price/<int:cafe_id>", methods=["POST", "PATCH"])
def update_price(cafe_id):
    try:
        target_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        new_price = request.args.get("new_price")
        target_cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(success="Successfully updated the price")
    except AttributeError:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database"}), 404


@app.route("/report_closed/<int:cafe_id>", methods=["DELETE"])
def remove_cafe(cafe_id):
    key = request.args.get("api_key")
    if key == "TopSecretAPIKey":
        target_cafe = db.session.get(entity=Cafe, ident=cafe_id)
        if target_cafe:
            db.session.delete(target_cafe)
            db.session.commit()
            return jsonify(success="Successfully deleted the cafe")
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database"}), 404
    else:
        return jsonify(erroe="Sorry, that's not allowed. Make sure you have the correct api_key.")


if __name__ == '__main__':
    app.run(debug=True)
