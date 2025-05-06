import pika, json, random
from datetime import datetime

def generate_weather_data(station_id):
    return {
        "station_id": station_id,
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(-10, 35), 2),
        "humidity": random.randint(20, 100),
        "wind_speed": round(random.uniform(0, 100), 2),
        "rainfall": round(random.uniform(0, 50), 2)
    }

def publish_to_rabbitmq():
    credentials = pika.PlainCredentials(
        username='admin',
        password='adminpass'
    )
    params = pika.ConnectionParameters(
        host='rabbit',
        port = 5672,
        credentials = credentials,
        virtual_host='/'
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    channel.exchange_declare(
        exchange='weather_data',
        exchange_type='direct',
        durable=True
    )

    channel.queue_declare(queue='weather_logs_queue', durable=True)

    channel.queue_bind(
        exchange='weather_data',
        queue='weather_logs_queue',
        routing_key='raw_data'
    )
    
    data = generate_weather_data("station_1")
    channel.basic_publish(
        exchange='weather_data',
        routing_key='raw_data',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # mensaje persistente
        )
    )
    print(" [x] send weather data")
    connection.close()

if __name__ == "__main__":
    publish_to_rabbitmq()
