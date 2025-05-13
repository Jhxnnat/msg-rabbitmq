# Sistema Mensajería
Sistema de gestión de logs de estaciones meteorológicas simuladas con microservicios usando Docker.

## Servicios
RabbitMQ es el broker de mensajería para la comunicación entre los servicios, los datos de los registros se almacenan en una base de datos PostgreSQL.
- El servicio *Producers*: genera y publica datos simulados de una estación meteorológica a RabbitMQ.
- El servicio *Consumers*: obtiene los mensajes de la cola de RabbitMQ, los valida y almacena en la base de datos.

## Dependencias
- Python 3.13+
- Docker (con plugin docker-compose)

## Uso
- `docker-compose up --build`
- El dashboard de RabbitMQ estará en localhost:15672. usuario: admin, contraseña: adminpass

