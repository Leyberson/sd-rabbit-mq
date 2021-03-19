from actuators import actuator
import threading

th_light = threading.Thread(target = actuator.serve, args = ('50001', 'LightActuator'))
th_fire = threading.Thread(target = actuator.serve, args = ('50002', 'FireActuator'))
th_temp = threading.Thread(target = actuator.serve, args = ('50003', 'AirConditioningActuator'))

th_light.start()
th_fire.start()
th_temp.start()

print('started')