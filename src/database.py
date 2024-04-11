import sqlite3


class Database:
    """Class to interact with the SQLite database."""

    def __init__(self, db_name='telemetry.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create a SQLite table to store telemetry data."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS telemetry (
                desi TEXT,
                dir INTEGER,
                oper INTEGER,
                veh INTEGER,
                tst TEXT,
                tsi INTEGER,
                spd REAL,
                hdg INTEGER,
                lat REAL,
                long REAL,
                acc REAL,
                dl INTEGER,
                odo INTEGER,
                drst INTEGER,
                oday TEXT,
                jrn INTEGER,
                line INTEGER,
                start TEXT,
                loc TEXT,
                stop INTEGER,
                route TEXT,
                occu INTEGER
            )
        ''')
        self.conn.commit()

    def insert_telemetry(self, data):
        """Insert telemetry data into the SQLite table."""
        self.cursor.execute('''
                INSERT INTO telemetry (
                    desi, dir, oper, veh, tst, tsi, spd, hdg, lat, long, acc, dl, odo, drst, oday, jrn, line, start, loc, stop, route, occu
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            data.get('desi'),
            data.get('dir'),
            data.get('oper'),
            data.get('veh'),
            data.get('tst'),
            data.get('tsi'),
            data.get('spd'),
            data.get('hdg'),
            data.get('lat'),
            data.get('long'),
            data.get('acc'),
            data.get('dl'),
            data.get('odo'),
            data.get('drst'),
            data.get('oday'),
            data.get('jrn'),
            data.get('line'),
            data.get('start'),
            data.get('loc'),
            data.get('stop'),
            data.get('route'),
            data.get('occu')
        ))
        self.conn.commit()

    def get_bus_ids(self):
        """Get a list of unique bus IDs."""
        self.cursor.execute('SELECT DISTINCT veh FROM telemetry')
        bus_ids = [row[0] for row in self.cursor.fetchall()]
        return bus_ids

    def get_bus(self, veh):
        """Get telemetry data for a specific bus."""
        self.cursor.execute('SELECT * FROM telemetry WHERE veh=?', (veh,))
        bus = self.cursor.fetchone()
        return bus

    def get_next_stop(self, veh):
        """Get the next stop for a specific bus."""
        self.cursor.execute('SELECT stop FROM telemetry WHERE veh=?', (veh,))
        next_stop = self.cursor.fetchone()
        return next_stop

    def get_current_location(self, veh):
        """Get the current location for a specific bus."""
        self.cursor.execute('SELECT lat, long FROM telemetry WHERE veh=?', (veh,))
        current_location = self.cursor.fetchone()
        return current_location

    def get_buses(self):
        """Get the current location for all buses or a certain number of buses."""
        self.cursor.execute('SELECT lat, long, veh FROM telemetry')
        buses = self.cursor.fetchall()
        return buses

    def close(self):
        """Close the connection to the database."""
        self.conn.close()
