from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, URL
import csv
from secret_key import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    cafe_location_url = URLField('Cafe URL', validators=[DataRequired(), URL(message='URL 형식에 맞춰서 작성해주세요.')])
    cafe_open_time = StringField('Opening Time e.g., 8AM', validators=[DataRequired()])
    cafe_close_time = StringField('Closing Time e.g., 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[('☕️', '☕️'), ('☕️☕️', '☕️☕️'), ('☕️☕️☕️', '☕️☕️☕️'), ('☕️☕️☕️☕️', '☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')])
    wifi_rating = SelectField('Wifi Strength Rating', choices=[('🙅', '🙅'), ('💪', '💪️'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')])
    power_rating = SelectField('Power Socket Availability', choices=[('🙅', '🙅'), ('🔌', '🔌‍'), ('🔌🔌', '🔌‍🔌‍'), ('🔌🔌🔌', '🔌‍🔌‍🔌‍'), ('🔌🔌🔌🔌', '🔌‍🔌‍🔌‍🔌‍'), ('🔌🔌🔌🔌🔌', '🔌‍🔌‍🔌‍🔌‍🔌‍')])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

# map link부분 map.naver.com/fkj,0,0,0인 부분이 있어서 csv의 ,와 구분이 안되는 문제가 있음
@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        message = f'\n{form.cafe.data}, {form.cafe_location_url.data}, ' \
                  f'{form.cafe_open_time.data}, {form.cafe_close_time.data}, {form.coffee_rating.data},' \
                  f'{form.wifi_rating.data}, {form.power_rating.data}'
        print(message)
        with open('cafe-data.csv', 'a') as file:
            file.write(message)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
