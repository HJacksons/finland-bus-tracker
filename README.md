# Finland Bus Tracker

This project provides a service that consumes telemetry data from the MQTT server at `mqtt.hsl.fi`, stores the data in a SQLite database, and provides an API for searching the data/buses.

## Features

- Real-time tracking of buses in Finland
- Search for buses close to a specific location
- Get the next stop for a specific bus
- Get the current location of a specific bus
- Get a list of buses within a certain radius of a given location

## Installation

1. Clone this repository:
    ```
    git clone https://github.com/HJacksons/finland-bus-tracker.git
    ```
2. Change into the project directory:
    ```
    cd finland-bus-tracker
    ```
3. Build the Docker image:
    ```
    docker build -t finland-bus-tracker .
    ```
   Alternatively, you can install the dependencies and run the project locally:
    ```
    pip install -r requirements.txt
    mqtt_client.py   # Run this script to start the MQTT client
    python app.py    # Run this script to start the Flask server
    ```

## Usage

1. Run the Docker container:
    ```
    docker run -p 5001:5001 finland-bus-tracker
    ```
2. Access the API at `http://localhost:5001 ` or `http://127.0.0.1:5001`.

## API Endpoints

- `/bus_ids`: Get a list of bus IDs.
- `/bus/<int:veh>`: Get information about a specific bus.
- `/bus/<int:veh>/next_stop`: Get the next stop for a specific bus.
- `/bus/<int:veh>/current_location`: Get the current location of a specific bus.
- `/buses_within_radius?lat=<latitude>&long=<longitude>&radius=<radius>&limit=<limit>`: Get a list of buses within a certain radius of a given location.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.