from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# connecting database sqlite to the folder newbooking.db thats stores all the data that is inputed
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newbooking.db'
db = SQLAlchemy(app)


# database model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    staff = db.Column(db.String(200))
    comments = db.Column(db.Text())

    def __init__(self, customer, staff, comments):
        self.customer = customer
        self.staff = staff
        self.comments = comments


# route to mainpage
@app.route("/")
def home():
    return render_template("index.html")


# route to sent.html page that will display once the customer press "Book" button
@app.route('/submit', methods=["GET", 'POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        staff = request.form['staff']
        comments = request.form['comments']
        # if these fields are left empty the below msg will show
        if customer == '' or staff == '':
            return render_template('index.html', message='Please enter required fields')
        # filtering out if the customer has already made a booking and wont allow double booking
        if Booking.query.filter_by(customer=customer).count() == 0:
            data = Booking(customer, staff, comments)
            db.session.add(data)
            db.session.commit()
            # returns the sent.html page with the booking details the customer just made
            return render_template('sent.html', booking=data)
        return render_template('index.html', message='You have already booked an appointment')


@app.route("/allBookings", methods=["GET", "POST"])
def allBookings():
    bookings = Booking.query.all()
    return render_template("allBookings.html", bookings=bookings)


if __name__ == "__main__":
    app.run(debug=True)
