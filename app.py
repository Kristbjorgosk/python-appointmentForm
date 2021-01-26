from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newbooking.db'
db = SQLAlchemy(app)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    staff = db.Column(db.String(200))
    comments = db.Column(db.Text())

    def __init__(self, customer, staff, comments):
        self.customer = customer
        self.staff = staff
        self.comments = comments


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/submit', methods=["GET", 'POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        staff = request.form['staff']
        comments = request.form['comments']
        # return render_template("sent.html")
        if customer == '' or staff == '':
            return render_template('index.html', message='Please enter required fields')
        # if db.session.query(Booking).filter(Booking.customer == customer).count() == 0:
        if Booking.query.filter_by(customer=customer).count() == 0:
            data = Booking(customer, staff, comments)
            db.session.add(data)
            db.session.commit()
            # send_mail(customer, staff, comments)
            return render_template('sent.html', booking=data)
        return render_template('index.html', message='You have already booked an appointment')


if __name__ == "__main__":
    app.run(debug=True)
