import os, sys, pika, json
import psycopg2
from psycopg2 import sql

class Consumer:
    def __init__(self):
        self.params = None

    def validate_weather_thresholds(self, data):
        if data['temperature'] >= 33:
            print("Critic temperature")
        if (data['wind_speed'] > 90):
            print("Critic wind speed")

    def save_to_db(self, data, cursor):
        insert = sql.SQL("""
            INSERT INTO weather_logs (station_id, time_stamp, temperature, humidity, wind_speed)
            VALUES (%s, %s, %s, %s, %s)
        """)
        cursor.execute(insert, (
            data['station_id'],
            data['time_stamp'],
            data['temperature'],
            data['humidity'],
            data['wind_speed']
        ))

    def callback(self, ch, method, properties, body):
        try:
            data = json.loads(body)
            self.validate_weather_thresholds(data)
            print(f" [y] received: {body}")

            conn = psycopg2.connect(host='postgres',
                        database='db', user='admin', password='adminpass')
            cursor = conn.cursor()
            self.save_to_db(data, cursor)

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error procesing message: {e}")

    def set_connection_params(self, username, password):
        credentials = pika.PlainCredentials(
            username=username,
            password=password
        )
        self.params = pika.ConnectionParameters(
            host='rabbit',
            port = 5672,
            credentials = credentials
        )
    
    def consume(self):
        try:
            connection = pika.BlockingConnection(self.params)
            channel = connection.channel()
        except Exception as e:
            print("Error on connection")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

        try:
            channel.queue_declare(queue='weather_logs_queue', durable=True)
            channel.basic_consume(queue='weather_logs_queue', on_message_callback=self.callback)
            print(" [*] Waiting Messages")
            channel.start_consuming()
        except Exception as e:
            print("Error consuming")

if __name__ == "__main__":

    consumer = Consumer()
    consumer.set_connection_params(username='admin', password='adminpass')
    try:
        consumer.consume()
    except KeyboardInterrupt:
        print("Interrumpt")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
