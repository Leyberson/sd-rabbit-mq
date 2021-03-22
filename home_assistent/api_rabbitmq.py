from fastapi import FastAPI
import grpc

from actuators import actuators_pb2_grpc, actuators_pb2

import pika

ILUMINACAO='iluminacao.sensor1'
INCENDIO = 'incendio.sensor1'
TEMPERATURA='temperatura.sensor1'

global message

app = FastAPI()


@app.get("/")
async def read_root():
    return "Ambiente inteligente"


def callback(ch, method, properties, body):
    ch.stop_consuming()
    global message
    message = body.decode()


@app.get('/sensor/iluminacao')
def read_iluminacao():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))

    channel = connection.channel()
    channel.queue_declare(queue = ILUMINACAO)

    channel.basic_consume(queue = ILUMINACAO, auto_ack = True, on_message_callback = callback)
    channel.start_consuming()
    global message
    return message

@app.get('/sensor/incendio')
def read_incendio():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))

    channel = connection.channel()
    channel.queue_declare(queue = INCENDIO)

    channel.basic_consume(queue = INCENDIO, auto_ack = True, on_message_callback = callback)
    channel.start_consuming()
    global message
    return message


@app.get('/sensor/temperatura')
def read_temperatura():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))

    channel = connection.channel()
    channel.queue_declare(queue = TEMPERATURA)

    channel.basic_consume(queue = TEMPERATURA, auto_ack = True, on_message_callback = callback)
    channel.start_consuming()
    global message
    return message


@app.get('/actuators/iluminacao/ligar')
def actuators_iluminacao_ligar():
    with grpc.insecure_channel('localhost:50001') as channel:
        stub = actuators_pb2_grpc.ActuatorStub(channel)
        try:
            response = stub.turn_on(actuators_pb2.Action())
            return {'atuador_iluminacao':response.turned}
        except Exception as e:
            return str(e)


@app.get('/actuators/iluminacao/desligar')
def actuators_iluminacao_desligar():
    with grpc.insecure_channel('localhost:50001') as channel:
        stub = actuators_pb2_grpc.ActuatorStub(channel)
        try:
            response = stub.turn_off(actuators_pb2.Action())
            return {'atuador_iluminacao': response.turned}
        except Exception as e:
            print("não foi possível se conectar ao sevidor grpc")


@app.get('/actuators/incendio/ligar')
def actuators_incendio_ligar():
    with grpc.insecure_channel('localhost:50002') as channel:
        stub = actuators_pb2_grpc.ActuatorStub(channel)
        try:
            response = stub.turn_on(actuators_pb2.Action())
            return  {'atuador_incendio':response.turned}
        except:
            print('não foi possível se conectar ao sevidor grpc')


@app.get('/actuators/incendio/desligar')
def actuators_incendio_desligar():
    with grpc.insecure_channel('localhost:50002') as channel:
        stub = actuators_pb2_grpc.ActuatorStub(channel)
        try:
            response = stub.turn_off(actuators_pb2.Action())
            return {'atuador_incendio': response.turned}
        except:
            print('não foi possível se conectar ao sevidor grpc')


@app.get('/actuators/temperatura/ligar')
def actuators_temperatura_ligar():
    with grpc.insecure_channel('localhost:50003') as channel:
        stub = actuators_pb2_grpc.ActuatorStub(channel)
        try:
            response = stub.turn_on(actuators_pb2.Action())
            return {'atuador_ar_condicionado':response.turned}
        except:
            print('não foi possível se conectar ao sevidor grpc')


@app.get('/actuators/temperatura/desligar')
def actuators_temperatura_desligar():
    with grpc.insecure_channel('localhost:50003') as channel:
        stub = actuators_pb2_grpc.ActuatorStub(channel)
        try:
            response = stub.turn_off(actuators_pb2.Action())
            return {'atuador_ar_condicionado': response.turned}
        except:
            print('não foi possível se conectar ao sevidor grpc')

@app.get('/iluminacao')
def get_iluminacao():
    sensor_response = read_iluminacao()
    atuador_response=None
    if sensor_response == 'too shiny':
        atuador_response= actuators_iluminacao_desligar()
    elif sensor_response=='too dark':
        atuador_response = actuators_iluminacao_ligar()

    if atuador_response:
        return {'sensor_iluminacao':sensor_response, 'atuador_iluminacao':atuador_response['atuador_iluminacao']}
    return{'sensor_iluminacao':sensor_response}


@app.get('/temperatura')
def get_temperatura():
    sensor_response = read_temperatura()
    atuador_response=None
    if int(sensor_response) < 25:
        atuador_response= actuators_temperatura_desligar()
    elif int(sensor_response)>30:
        atuador_response = actuators_temperatura_ligar()

    if atuador_response:
        return {'sensor_temperatura':sensor_response, 'atuador_temperatura':atuador_response['atuador_ar_condicionado']}
    return {'sensor_temperatura':sensor_response}


@app.get('/incendio')
def get_incendio():
    sensor_response = read_incendio()
    atuador_response=None
    if sensor_response == 'normal':
        atuador_response= actuators_incendio_desligar()
    elif sensor_response=='fire':
        atuador_response = actuators_incendio_ligar()

    if atuador_response:
        return {'sensor_incendio':sensor_response, 'atuador_incendio':atuador_response['atuador_incendio']}
    return {'sensor_incendio':sensor_response}