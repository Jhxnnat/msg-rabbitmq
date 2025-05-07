# msg-rabbitmq

protoripo de sistema de gestión de logs de estaciones meteorológicas. 

# TODO:

### Productores de datos (Producers):
- [x] Servicio en Python que simule o reciba datos de estaciones (JSON).
- [x] Debe publicar a un exchange de RabbitMQ con mensajes durables.

### Broker de mensajería:
- [x] Configuración de RabbitMQ con colas durables y bindings adecuados.

### Consumidores (Consumers): 
Microservicio en Python donde:
- [ ] Procesa los mensajes con ack manual.
- [ ] Persiste en PostgreSQL (tabla weather_logs).
- [ ] Valida rangos de valores y gestiona errores.

### Base de datos:
- [ ] Manejar conexiones seguras y reconexiones automáticas.

### Docker y orquestación:
- [x] Contenedores para RabbitMQ, PostgreSQL, productores y consumidores.
- [x] archivo docker-compose

### Logs y monitoreo:
- [ ] Incluir registros de eventos en cada componente y métricas de rendimiento. 
