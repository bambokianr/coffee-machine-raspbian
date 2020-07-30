from RPiSim.GPIO import GPIO
import time
import traceback
import random

GPIO.setmode(GPIO.BCM)

VEL_SOM = 340 # em m/s

# Sobre a cafeteira, definiu-se:
# Recipiente cheio -> distância superfície sensor: 0m
# Recipiente vazio -> distância superfície sensor: 0.17m

# porcentagem de água necessária para preparo de 1 café -> 10% => equivale a distância superfície sensor = 0.153m
# porcentagem de pó necessário para preparo de 1 café -> 15% => equivale a distância superfície sensor = 0.1445m

class Cafeteira:
  # pino 2 - out - cafeteira ligada?
  GPIO.setup(2, GPIO.OUT, initial = GPIO.LOW)
  # pino 3 - out - cafeteira apta?
  GPIO.setup(3, GPIO.OUT, initial = GPIO.LOW)
  # pino 4 - out - café pronto?
  GPIO.setup(4, GPIO.OUT, initial = GPIO.LOW)

  def __init__(self, porcentAgua, porcentCafe):
    self.cafeteiraLigada = False
    self.cafeteiraPronta = False
    self.porcentAgua = porcentAgua
    self.porcentCafe = porcentCafe

  def ligarCafeteira(self):
    if(self.cafeteiraLigada == True):
      print('--- Cafeteira já está ligada.')
    else:
      self.cafeteiraLigada = True
      GPIO.output(2, GPIO.HIGH)
      print('--- Cafeteira ligada.')
  
  def desligarCafeteira(self):
    if(self.cafeteiraLigada == True):
      self.cafeteiraLigada = False
      GPIO.output(2, GPIO.LOW)
      print('--- Cafeteira desligada.')
  
  def TempoSensorAgua(self):
    return 0.001 * (100 - self.porcentAgua) / 100
  def TempoSensorCafe(self):
    return 0.001 * (100 - self.porcentCafe) / 100

  def checarCafeteiraPronta(self):
    GPIO.output(4, GPIO.LOW)
    distSensorAgua = MedirAgua(self)
    distSensorCafe = MedirCafe(self)
    print('--- {}% de água disponível.'.format(self.porcentAgua))
    print('--- {}% de pó de café disponível.'.format(self.porcentCafe))

    if(distSensorAgua > 0.154 or distSensorCafe > 0.145):
      self.cafeteiraPronta = False
      GPIO.output(3, GPIO.LOW)
      if(distSensorAgua > 0.154):
        print('--- [CAFETEIRA] Pausa no processo - água insuficiente.')
      if(distSensorCafe > 0.145):
        print('--- [CAFETEIRA] Pausa no processo - pó de café insuficiente.')
    else:
      self.cafeteiraPronta = True
      GPIO.output(3, GPIO.HIGH)
      print('--- [CAFETEIRA] Cafeteira pronta para preparar o café.')

  def adicionarAgua(self, qtd):
    self.porcentAgua += qtd

  def adicionarCafe(self, qtd):
    self.porcentCafe += qtd

  def fazerCafe(self):
    if(self.cafeteiraPronta == True):
      self.porcentAgua -= 10
      self.porcentCafe -= 15
      time.sleep(3)
      print('--- [CAFETEIRA] Café pronto.')
      GPIO.output(4, GPIO.HIGH)
      self.cafeteiraPronta = False
      GPIO.output(3, GPIO.LOW)

def SensorAgua():
    # pinos 17 e 18 - sensor de distância - água
    GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW) # TRIGGER
    GPIO.setup(18, GPIO.IN) # ECHO

def SensorCafe():
    # pinos 22 e 23 - sensor de distância - pó de café
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW) # TRIGGER
    GPIO.setup(23, GPIO.IN) # ECHO

def MedirAgua(cafeteira):
  print('--- [SENSOR] Medindo quantidade de água.')
  GPIO.output(17, GPIO.HIGH)
  tempoTotal = cafeteira.TempoSensorAgua()
  #time.sleep(tempoTotal)
  time.sleep(2)
  GPIO.output(17, GPIO.LOW)
  distancia = (tempoTotal * VEL_SOM) / 2
  return distancia

def MedirCafe(cafeteira):
  print('--- [SENSOR] Medindo quantidade de pó de café.')
  GPIO.output(22, GPIO.HIGH)
  tempoTotal = cafeteira.TempoSensorCafe()
  #time.sleep(tempoTotal)
  time.sleep(2)
  GPIO.output(22, GPIO.LOW)
  distancia = (tempoTotal * VEL_SOM) / 2
  return distancia

def comandosPreFazerCafe(cafeteira):
  while(cafeteira.cafeteiraPronta == False):
    cafeteira.checarCafeteiraPronta()
    if(cafeteira.porcentAgua < 10):
      cmdAdcAgua = input("Adicionar água? [S/N] ")
      if(cmdAdcAgua.upper() == 'S'):
        cmdQtdAgua = input("% de água adicionada: ")
        cafeteira.adicionarAgua(int(cmdQtdAgua))
      elif(cmdAdcAgua.upper() == 'N'):
        cafeteira.desligarCafeteira()
        break
    if(cafeteira.porcentCafe < 15):
      cmdAdcCafe = input("Adicionar pó de café? [S/N] ")
      if(cmdAdcCafe.upper() == 'S'):
        cmdQtdCafe = input("% de pó de café adicionado: ")
        cafeteira.adicionarCafe(int(cmdQtdCafe))
      elif(cmdAdcCafe.upper() == 'N'):
        cafeteira.desligarCafeteira()
        break

def ExecutarCafeteira():
  cafeteira = Cafeteira(random.randint(0, 100), random.randint(0, 100))
  
  cmdLigarCafeteira = input("Ligar cafeteira? [S/N] ")
  # ! LIGAR CAFETEIRA
  if(cmdLigarCafeteira.upper() == 'S'):
    cafeteira.ligarCafeteira()
    comandosPreFazerCafe(cafeteira)

    if(cafeteira.cafeteiraPronta == True):
      cmdFazerCafe = input("Fazer café? [S/N] ")
      # ! FAZER CAFÉ
      while(cafeteira.cafeteiraPronta == True and cmdFazerCafe.upper() == 'S'):
        cafeteira.fazerCafe()
        cmdFazerCafe = input("Fazer outro café? [S/N] ")
        if(cmdFazerCafe.upper() == 'S'):
          comandosPreFazerCafe(cafeteira)
        
      # ! NÃO FAZER CAFÉ
      if(cmdFazerCafe.upper() == 'N'):
        cafeteira.desligarCafeteira()

def Main():
  # GPIO.setmode(GPIO.BCM)
  # GPIO.setwarnings(False)
  SensorAgua()
  SensorCafe()
  ExecutarCafeteira()

Main()