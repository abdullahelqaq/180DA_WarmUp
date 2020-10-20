import paho.mqtt.client as mqtt

# Connection request callback
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

    # Subscribe to topic
    client.subscribe("ece180d/comms_tutorial/team3", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnect")
    else:
        print("Expected disconnect")

# Message callback
def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + '" on topic "' + message.topic + '" with QoS ' + str(message.qos))

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message

# Connect to broker
mqtt_client.connect_async('mqtt.eclipse.org')

mqtt_client.loop_start()

for i in range(50):
    mqtt_client.publish("ece180d/comms_tutorial/team3", "Hello, MQTT!", qos=1)

mqtt_client.loop_stop()
mqtt_client.disconnect()