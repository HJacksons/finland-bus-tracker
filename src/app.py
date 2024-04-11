from flask import Flask, request
from geopy import distance
from database import Database  # Import the database class from database.py

app = Flask(__name__)


@app.route('/')
def home():
    return """
        <b>Welcome to the bus tracker API! Here is how you can use it:</b><br><br>
        1. Search for a bus:   /bus/&lt;bus_id&gt; e.g. /bus/1014<br>
        (To get a list of available buses, visit: /bus_ids )<br><br>  
        2. Get the next stop for the bus: /bus/&lt;bus_id&gt;/next_stop e.g. /bus/1014/next_stop<br><br>
        3. Get the current location of the bus: /bus/&lt;bus_id&gt;/current_location e.g. /bus/1014/current_location<br><br>
        4. Search buses within a certain radius:<br>
           /buses_within_radius?lat=&lt;latitude&gt;&long=&lt;longitude&gt;&radius=&lt;radius&gt;;&limit=&lt;limit&gt; e.g. /buses_within_radius?lat=60.160594&long=24.7367544&radius=1.0&limit=5<br><br>
        """


@app.route('/bus_ids')
def get_bus_ids():
    db = Database()
    bus_ids = db.get_bus_ids()
    db.close()
    return {'bus_ids': bus_ids}



@app.route('/bus/<int:veh>')  # /bus/123
def get_bus(veh):
    db = Database()
    bus = db.get_bus(veh)
    db.close()
    if bus is None:
        return 'Bus not found', 404
    else:
        return {
            'desi': bus[0],
            'dir': bus[1],
            'oper': bus[2],
            'veh': bus[3],
            'tst': bus[4],
            'tsi': bus[5],
            'spd': bus[6],
            'hdg': bus[7],
            'lat': bus[8],
            'long': bus[9],
            'acc': bus[10],
            'dl': bus[11],
            'odo': bus[12],
            'drst': bus[13],
            'oday': bus[14],
            'jrn': bus[15],
            'line': bus[16],
            'start': bus[17],
            'loc': bus[18],
            'stop': bus[19],
            'route': bus[20],
            'occu': bus[21],
        }


@app.route('/bus/<int:veh>/next_stop')  # /bus/123/next_stop
def get_next_stop(veh):
    db = Database()
    next_stop = db.get_next_stop(veh)
    db.close()
    if next_stop is None:
        return 'Next stop not found', 404
    else:
        return {'next_stop': next_stop[0]}


@app.route('/bus/<int:veh>/current_location')  # /bus/123/current_location
def get_current_location(veh):
    db = Database()
    current_location = db.get_current_location(veh)
    db.close()
    if current_location is None:
        return 'Current location not found', 404
    else:
        return {'lat': current_location[0], 'long': current_location[1]}


@app.route('/buses_within_radius')  # /buses_within_radius?lat=...&long=...&radius=...&limit=...
def get_buses_within_radius():
    lat = request.args.get('lat')
    long = request.args.get('long')
    radius = request.args.get('radius')
    limit = request.args.get('limit')
    if lat is None or long is None or radius is None:
        return 'Missing lat, long, or radius query parameter', 400
    try:
        lat = float(lat)
        long = float(long)
        radius = float(radius)
        if limit is not None:
            limit = int(limit)
    except ValueError:
        return 'Invalid lat, long, radius, or limit query parameter', 400

    db = Database()
    buses = db.get_buses()
    db.close()
    buses_within_radius = set()
    for bus in buses:
        bus_lat, bus_long, veh = bus
        if bus_lat is None or bus_long is None:
            continue
        if distance.distance((lat, long), (bus_lat, bus_long)).km <= radius:
            buses_within_radius.add(veh)
            if limit is not None and len(buses_within_radius) >= limit:
                break
    return {'buses_within_radius': list(buses_within_radius)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
