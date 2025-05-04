Iimplementar un sistema de gestión de logs de estaciones meteorológicas descrito en este caso de estudio. 
Debe entregar un prototipo funcional que contemple los siguientes elementos y considere las restricciones y usos potenciales.

## Elementos a tener en cuenta:

### Productores de datos (Producers):
- Servicio en Python que simule o reciba datos de estaciones (JSON).
- Debe publicar a un exchange de RabbitMQ con mensajes durables.

### Broker de mensajería:
- Configuración de RabbitMQ con colas durables y bindings adecuados.
- Incluir dashboard de administración.

### Consumidores (Consumers): 
Microservicio en Python que:
- Procesa los mensajes con ack manual.
- Persiste en PostgreSQL (tabla weather_logs).
- Valida rangos de valores y gestiona errores.

### Base de datos:
- Definir esquema en PostgreSQL.
- Manejar conexiones seguras y reconexiones automáticas.

### Docker y orquestación:
- Contenedores para RabbitMQ, PostgreSQL, productores y consumidores.
- Archivo docker-compose.yml que garantice arranque ordenado y reinicios automáticos.

### Logs y monitoreo:
- Incluir registros de eventos en cada componente y métricas de rendimiento. 
- Proponer uso de Prometheus/Grafana si el tiempo lo permite.

## Restricciones técnicas:

- Python 3.13+ y librerías estables (pika, psycopg2).
- Mensajes marcados como persistent para evitar pérdida.
- Consumo con prefetch_count=1 para procesamiento ordenado.
- Bases de datos y colas deben ser stateful y persistentes en volúmenes Docker.
- Seguir buenas prácticas de código, documentación y manejo de excepciones.

## Posibles usos y extensiones:

- Servicio de alertas en tiempo real si un valor supera umbrales definidos.
- API REST para consulta de logs históricos y generación de reportes.
- Integración con paneles de visualización (Grafana) para dashboards en tiempo real.
- Escalabilidad horizontal: despliegue múltiple de consumidores según carga.

## Entregables esperados:

- Repositorio Git con código y README.md detallado.
- Video demostrativo publicado en el foro.
- Esquema visual del diseño en la documentación
- docker-compose.yml y configuración de volúmenes.
- Scripts de inicialización de la base de datos.
- Documentación de uso y pruebas de validación.

