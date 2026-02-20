import paho.mqtt.client as mqtt
import json

BROKER = 'localhost'
PORT = 1883
TOPIC = '#'

# Callback when a message is received
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        try:
            data = json.loads(payload)
        except Exception:
            data = payload
        if msg.topic != 'system/loop':
            print(f"[MQTT] Topic: {msg.topic} | Message: {data}")
    except Exception as e:
        print(f"Error decoding message: {e}")

# Callback when connected to broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker at {BROKER}:{PORT} with result code {rc}")
    client.subscribe(TOPIC)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    print(f"Subscribing to all topics on {BROKER}:{PORT}")
    client.loop_forever()
