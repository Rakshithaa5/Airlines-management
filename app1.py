from flask import Flask, render_template, request, jsonify
import mysql.connector
from collections import deque

app = Flask(__name__, template_folder='template')

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Allizwell@5',
    'database': 'airline_system'
}

# Data structures
checkin_queue = deque()
priority_queue = deque()
passenger_hash = {}  # booking_ref -> passenger_data
seat_assignment = {}  # seat_number -> booking_ref

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/checkin', methods=['POST'])
def checkin():
    # Get passenger data from form
    booking_ref = request.form['booking_ref']

    # Check if the booking reference already exists
    if booking_ref in passenger_hash:
        return jsonify({'status': 'failed', 'message': 'Duplicate booking reference.'})

    passenger_data = {
        'name': request.form['name'],
        'flight': request.form['flight'],
        'class': request.form['class'],
        'seat_pref': request.form['seat_pref']
    }

    # Add to appropriate queue
    if passenger_data['class'] in ['business', 'first']:
        priority_queue.append(booking_ref)
    else:
        checkin_queue.append(booking_ref)

    # Add to hash table
    passenger_hash[booking_ref] = passenger_data

    return jsonify({'status': 'success'})

@app.route('/next_passenger')
def next_passenger():
    # Priority passengers first
    if priority_queue:
        booking_ref = priority_queue.popleft()
    elif checkin_queue:
        booking_ref = checkin_queue.popleft()
    else:
        return jsonify({'status': 'empty'})

    passenger_data = passenger_hash.get(booking_ref, {})
    return jsonify({'passenger': passenger_data})

@app.route('/assign_seat', methods=['POST'])
def assign_seat():
    booking_ref = request.form['booking_ref']
    seat_number = request.form['seat_numb']

    # Check seat availability
    if seat_number in seat_assignment:
        return jsonify({'status': 'failed', 'message': 'Seat already occupied.'})

    # Assign seat
    seat_assignment[seat_number] = booking_ref
    passenger_hash[booking_ref]['seat'] = seat_number

    return jsonify({'status': 'success'})

@app.route('/get_passenger/<booking_ref>')
def get_passenger(booking_ref):
    # Debugging: print the reference to see what's coming in
    print(f"Looking up passenger with booking reference: {booking_ref}")
    
    passenger_data = passenger_hash.get(booking_ref, None)
    if not passenger_data:
        return jsonify({'status': 'failed', 'message': 'Passenger not found'})

    return jsonify({'status': 'success', 'passenger': passenger_data})

@app.route('/get_seat_map/<flight_number>')
def get_seat_map(flight_number):
    # Mock seat map data for demonstration
    seat_map = {
        'first': [['1A', '1B', '', '1C', '1D'], ['2A', '2B', '', '2C', '2D']],
        'business': [['3A', '3B', '3C', '3D', '3E', '3F'], ['4A', '4B', '4C', '4D', '4E', '4F']],
        'economy': [['5A', '5B', '5C', '', '5D', '5E', '5F'], ['6A', '6B', '6C', '', '6D', '6E', '6F']]
    }

    cursor = mysql.connector.connect(**db_config).cursor()
    cursor.execute("SELECT seat_number FROM passengers WHERE flight_number = %s", (flight_number,))
    occupied_seats = {seat[0] for seat in cursor.fetchall()}

    for class_type in seat_map:
        for row in seat_map[class_type]:
            for i in range(len(row)):
                if row[i] in occupied_seats:
                    row[i] = ''

    return jsonify({'seat_map': seat_map})

@app.route('/check_seat_availability', methods=['POST'])
def check_seat_availability():
    flight_number = request.form['flight_number']
    seat_number = request.form['seat_numb']

    cursor = mysql.connector.connect(**db_config).cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM passengers WHERE flight_number = %s AND seat_number = %s",
        (flight_number, seat_number)
    )
    is_available = cursor.fetchone()[0] == 0

    return jsonify({'available': is_available})

if __name__ == '__main__':
    app.run(debug=True)
