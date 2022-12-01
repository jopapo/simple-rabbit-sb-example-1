# simple-rabbit-sb-example-1
Simple RabbitMQ/ServiceBus test case

# Pré-requisitos

1. Um servidor rabbitmq
1. Um servidor service bus

Obs: De preferência com capacidades equivalentes.

# Teste 1

1 produtor numa exchange que direciona pra 1 queue que é lida por 3 consumers (o produtor tem um sleep de 0.1s e o consumidor é aleatório entre 0,5 e 1s).

Melhor execução (em bash diferentes):

`docker-compose -f docker-consumer-test1.yaml up producer`

`docker-compose -f docker-consumer-test1.yaml up consumer`

# Teste 2




# Referencias

https://github.com/FernandoBLima/python-rabbitmq-docker
