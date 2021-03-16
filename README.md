## First you need to have rabbitmq installed on your machine

You can use Docker:

```
sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

You need the lib pika to use rabbitmq

```
virtualenv sistemas_distribuidos
source sistemas_distribuidos/bin/activate
pip install pika
```