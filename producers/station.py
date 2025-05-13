import pika, json, random, time
from datetime import datetime

class Station:
    def __init__(self, station_id):
        self.station_id = station_id
        self.temperature = 20 #°C
        self.wind_speed = 40 #ms
        self.humidity = 20 # %

        self.params = None
        self.connection = None
        self.channel = None

    # Just to see how weather changes over time
    def change_weather_values(self):
        self.temperature += round(random.uniform(-1, 3), 2)
        self.wind_speed += round(random.uniform(-1, 2), 2)
        self.humidity += round(random.uniform(1, 2), 2)

    def generate_weather_data(self):
        self.change_weather_values()
        return {
            "station_id": self.station_id,
            "time_stamp": datetime.now().isoformat(),
            "temperature": self.temperature,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed
        }


    def init_connection(self, username, password):
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
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='weather_logs_queue', durable=True)

    def publish_to_rabbitmq(self):
        data = self.generate_weather_data()
        self.channel.basic_publish(
            exchange='',
            routing_key='weather_logs_queue',
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        
if __name__ == "__main__":
    station = Station("station_22")
    station.init_connection(username='admin', password='adminpass')
    while True:
        try:
            station.publish_to_rabbitmq()
            time.sleep(2)
        except KeyboardInterrupt:
            print("Interrumpt")
            station.connection.close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
    try:
        station.connection.close()
    except Exception as e:
        print(f'error closing connection: {e}')


