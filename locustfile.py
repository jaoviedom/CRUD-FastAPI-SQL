import json
from random import randrange
from sys import getsizeof
from locust import HttpUser, task, between

debug = False

def printDebug(msg):
  if debug:
    print(msg)

class Reader():
  def __init__(self):
    self.array = []

  
  def pickRandom(self):
    length = len(self.array)
    if length > 0:
      random_index = randrange(0, length - 1) if length > 1 else 0
      return self.array.pop(random_index)
    else:
      print(">> Reader: No encontramos ningún registro en el archivo.")
      return None
  
  def load(self):
    print(">> Reader: Estamos iniciando la lectura del archivo de datos.")
    
    try:
      with open('traffic.json', 'r') as data_file:
        self.array = json.loads(data_file.read())
    except Exception as error:
      print(f'>> Reader: No se cargaron los datos. Error: {error}')

class UserTrafic(HttpUser):
  wait_time = between(0.1, 0.9)
  reader = Reader()
  reader.load()

  def on_start(self):
    print(">> UserTraffic: Iniciamos el envío de tráfico.")
  
  @task
  def create_user(self):
    random_data = self.reader.pickRandom()

    if(random_data is not None):
      data_to_send = json.dumps(random_data)
      printDebug(data_to_send)

      self.client.post("/", json=random_data)
    else:
      print(">>UserTraffic: Envío de tráfico finalizado. No hay más registros para enviar.")
      self.stop(True)
  
  @task
  def getUsers(self):
    self.client.get("/")