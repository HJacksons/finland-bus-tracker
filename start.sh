#!/bin/bash
python src/mqtt_client.py &
exec python src/app.py