from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def booking():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        arrival = request.form['arrival']
        departure = request.form['departure']

        conn = sqlite3.connect('bookings.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO bookings (name, email, arrival, departure)
        VALUES (?, ?, ?, ?)
        ''', (name, email, arrival, departure))

        conn.commit()
        conn.close()

        return "<h2>Booking submitted!</h2>"

    return '''
    <h1>Fonteyn Holiday Parks</h1>

    <h2>Booking System</h2>

    <form method="POST">

        Name:<br>
        <input type="text" name="name"><br><br>

        Email:<br>
        <input type="email" name="email"><br><br>

        Arrival Date:<br>
        <input type="date" name="arrival"><br><br>

        Departure Date:<br>
        <input type="date" name="departure"><br><br>

        <button type="submit">Book Now</button>

    </form>
    '''

app.run(host='0.0.0.0', port=80)
