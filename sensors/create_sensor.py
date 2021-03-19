import sensor
import random

SENSOR_KIND = ['iluminacao', 'incendio', 'temperatura']

count = {'iluminacao':0, 'incendio':0, 'temperatura':0}
values = {'iluminacao':['escuro', 'bom', 'claro'],
          'incendio':['fire', 'normal'],
          'temperatura':[i for i in range(25,40)]}
timer = {'iluminacao':10, 'incendio':1, 'temperatura':20}
weights = {'iluminacao':None, 'incendio':[5, 95], 'temperatura':None}

for value in range(20):
    sensor_type = random.choice(SENSOR_KIND)
    count[sensor_type] = count[sensor_type]+1
    sensor.Sensor(queue_name = sensor_type+'.sensor'+str(count[sensor_type]),
                  values = values[sensor_type],
                  timer = timer[sensor_type],
                  weights = weights[sensor_type])