from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

coffee_rating = [("☕", "☕"), ("☕☕", "☕☕"), ("☕☕☕", "☕☕☕"), ("☕☕☕☕", "☕☕☕☕"), ("☕☕☕☕☕", "☕☕☕☕☕")]
wifi_strength = [("💪", "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"), ("💪💪💪💪", "💪💪💪💪"), ("💪💪💪💪💪", "💪💪💪💪💪")]
socket_availability = [("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌"), ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")]


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps (URL)', validators=[DataRequired(), URL()])
    opening = StringField('Opening Time e.g 8AM', validators=[DataRequired()])
    closing = StringField('Closing Time e.g 5:30PM', validators=[DataRequired()])
    rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=coffee_rating)
    wifi = SelectField('Wifi Strength Rating', validators=[DataRequired()], choices=wifi_strength)
    power = SelectField('Power Socket Availability', validators=[DataRequired()], choices=socket_availability)
    submit = SubmitField('Submit')



@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    new_row = []
    if form.validate_on_submit():
        print("True")
        new_row.append(form.cafe.data)
        new_row.append(form.location.data)
        new_row.append(form.opening.data)
        new_row.append(form.closing.data)
        new_row.append(form.rating.data)
        new_row.append(form.wifi.data)
        new_row.append(form.power.data)
        with open("cafe-data.csv", "a", newline='', encoding='utf-8') as cafes_file:
            writer = csv.writer(cafes_file)
            writer.writerow(new_row)
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
