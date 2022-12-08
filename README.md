# Resumo

Teste simples de mensageria com modelo para RabbitMQ e ServiceBus.

# Pré-requisitos

1. Um servidor service bus (tem q ser manual) e a connection string
1. Um ambiente python (testado com 3.8)
1. Um orquestrador docker (testado com [Rancher Desktop](https://rancherdesktop.io/))

# Teste 1 - 1P3Ci

Um produtor numa exchange que direciona pra 1 queue que é lida por 3 consumers com mensagens únicas (o produtor tem um sleep de 0.1s e o consumidor é aleatório entre 0,5 e 1s).

Uso para rabbit:

```bash
docker-compose -d up rabbitmq-server
docker-compose up producer-rb consumer-rb
```

Uso para SB:

1. Colocar String Connection do SAS do SB em sb.env com a key SERVICE_BUS_CONNECTION_STRING;
1. Executar
```bash
docker-compose up producer-sb consumer-sb
```

# Teste 2 - 1P2Cc

Similar ao anterior com a diferença que os consumidores recebem mensagens replicadas (tópico/exchange).

* Recomendado: Diminuir o scale dos consumers pra 1.

```bash
docker-compose -d up rabbitmq-server
docker-compose up producer-rb consumer-rb consumer-rb-extra
```

Uso para SB:

```bash
docker-compose up producer-sb consumer-sb consumer-sb-extra
```

# Referencias

https://github.com/FernandoBLima/python-rabbitmq-docker
https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq
https://pypi.org/project/azure-servicebus/
https://github.com/Azure/azure-sdk-for-python/tree/azure-servicebus_7.8.1/sdk/servicebus/azure-servicebus/samples/sync_samples
