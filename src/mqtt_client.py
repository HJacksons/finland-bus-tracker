import paho.mqtt.client as mqtt_client
import json
from database import Database

# Create an instance of the Database class
db = Database()


# MQTT code
def on_connect(client, userdata, flags, rc, *extra_params):
    """Callback for when the client receives a CONNACK response from the server."""
    print("Connected with result code " + str(rc))
    client.subscribe("/hfp/v2/journey/ongoing/vp/bus/#")


def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the server."""
    try:
        data = json.loads(msg.payload)['VP']
        db.insert_telemetry(data)
    except json.JSONDecodeError:
        print("Error decoding JSON message: " + msg.payload)


if __name__ == '__main__':
    client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("mqtt.hsl.fi", 1883, 60)
        client.loop_forever()
    except Exception as e:
        print("Error connecting to MQTT broker: " + str(e))
