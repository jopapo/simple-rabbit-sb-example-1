# simple-rabbit-sb-example-1
Simple RabbitMQ/ServiceBus test case

# Pré-requisitos

1. Um servidor service bus (tem q ser manual)

Obs: De preferência com capacidades equivalentes.

# Teste 1 - 1P3C

1 produtor numa exchange que direciona pra 1 queue que é lida por 3 consumers (o produtor tem um sleep de 0.1s e o consumidor é aleatório entre 0,5 e 1s).

Uso para rabbit:

```bash
docker-compose -d up rabbitmq-server
docker-compose up producer-rb consumer-rb
```

Uso para SB:

1. Colocar String Connection do SAS do SB em SB.env com a key SERVICE_BUS_CONNECTION_STRING;
2. Executar
```bash
docker-compose up producer-sb consumer-sb
```

# Referencias

https://github.com/FernandoBLima/python-rabbitmq-docker
https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq
https://pypi.org/project/azure-servicebus/
