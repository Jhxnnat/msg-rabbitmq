import os, sys, pika, json
import psycopg2
from psycopg2 import sql

def validate_weather_data(data):
    # Validar rangos de valores
    if not (-50 <= data['temperature'] <= 60):
        raise ValueError("Temperatura fuera de rango")

# def save_to_postgres(data, cursor):
#     insert = sql.SQL("""
#     INSERT INTO weather_logs 
#     (station_id, timestamp, temperature, humidity, wind_speed, rainfall)
#     VALUES (%s, %s, %s, %s, %s, %s)
#     """)
#     cursor.execute(insert, (
#         data['station_id'],
#         data['timestamp'],
#         data['temperature'],
#         data['humidity'],
#         data['wind_speed'],
#         data['rainfall']
#     ))

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        validate_weather_data(data)
        print(f" [x] recivido: {body}")
        
        # conn = psycopg2.connect(
        #     host="postgres",
        #     database="weather_db",
        #     user="admin",
        #     password="securepassword")
        
        # with conn.cursor() as cursor:
        #     save_to_postgres(data, cursor)
        #     conn.commit()
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error procesando mensaje: {e}")
        # Puede implementarse dead-letter queue aquí

def main():
    credentials = pika.PlainCredentials(
        username='admin',
        password='adminpass'
    )
    params = pika.ConnectionParameters(
        host='rabbit',
        port = 5672,
        credentials = credentials
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='weather_logs_queue', durable=True)
    channel.basic_consume(queue='weather_logs_queue', on_message_callback=callback)
    
    print(" [*] Esperando mensajes. CTRL+C para salir")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrumpido")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
