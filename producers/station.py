import pika, json, random, time
from datetime import datetime

class Station:
    def __init__(self, station_id):
        self.station_id = station_id
        self.temperature = 20 #°C
        self.wind_speed = 40 #ms
        self.humidity = 20 # %

        self.params = None

    # Just to see how weather changes over time
    def change_weather_values(self):
        self.temperature += round(random.uniform(-1, 3), 2)
        self.wind_speed += round(random.uniform(-1, 2), 2)
        self.humidity += round(random.uniform(1, 2), 2)

    #NOTE: maybe fetch from real data
    def generate_weather_data(self):
        self.change_weather_values()
        return {
            "station_id": self.station_id,
            "timestamp": datetime.now().isoformat(),
            "temperature": self.temperature,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed
        }


    def set_connection_params(self, username, password):
        credentials = pika.PlainCredentials(
            username=username,
            password=password
        )
        self.params = pika.ConnectionParameters(
            host='rabbit',
            port = 5672,
            credentials = credentials,
            virtual_host='/'
        )

    def publish_to_rabbitmq(self):
        connection = pika.BlockingConnection(self.params)
        channel = connection.channel()
        channel.queue_declare(queue='weather_logs_queue', durable=True)
        
        data = self.generate_weather_data()
        channel.basic_publish(
            exchange='',
            routing_key='weather_logs_queue',
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        print(" [x] send weather data")
        connection.close()
        
if __name__ == "__main__":
    station = Station("station_22")
    station.set_connection_params(username='admin', password='adminpass')
    station.publish_to_rabbitmq()

