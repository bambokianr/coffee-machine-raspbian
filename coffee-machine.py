# from RPiSim.GPIO import GPIO
import time
import traceback
import random

VEL_SOM = 340 # em m/s

# Convenção
# Recipiente cheio -> distancia = 0
# Recipiente vazio -> distancia = 0.17 m

# definir que:
# menos que 10% de água - não rola fazer café --> 10% - distância do sensor a superfície = 0.153
# menos que 15% de café - não rola fazer café --> X% - distância do sensor a superfície = 0.12Y

class Cafeteira:
  def __init__(self, porcentAgua, porcentCafe):
    self.cafeteiraLigada = False
    self.cafeteiraPronta = False
    self.porcentAgua = porcentAgua
    self.porcentCafe = porcentCafe

  def ligarCafeteira(self): # pino LED 1 - acender
    if(self.cafeteiraLigada == True):
      print('--- Cafeteira já está ligada.')
    else:
      self.cafeteiraLigada = True
      print('--- Cafeteira ligada.')
  
  def desligarCafeteira(self): # pino LED 1 - apagar
    if(self.cafeteiraLigada == True):
      self.cafeteiraLigada = False
      print('--- Cafeteira desligada.')
  
  def TempoSensorAgua(self):
    return 0.001 * (100 - self.porcentAgua) / 100
  def TempoSensorCafe(self):
    return 0.001 * (100 - self.porcentCafe) / 100

  def checarCafeteiraPronta(self):
    distSensorAgua = MedirAgua(self)
    distSensorCafe = MedirCafe(self)
    print('--- {}% de água disponível.'.format(self.porcentAgua))
    print('--- {}% de pó de café disponível.'.format(self.porcentCafe))

    # se pode ou não realizar o preparo de um café
    if(distSensorAgua > 0.154 or distSensorCafe > 0.145):
      self.cafeteiraPronta = False
      if(distSensorAgua > 0.154):
        print('--- [CAFETEIRA] Pausa no processo - água insuficiente.')
      if(distSensorCafe > 0.145):
        print('--- [CAFETEIRA] Pausa no processo - pó de café insuficiente.')
    else:
      self.cafeteiraPronta = True
      print('--- [CAFETEIRA] Cafeteira pronta para preparar o café.')

  def adicionarAgua(self, qtd):
    self.porcentAgua += qtd

  def adicionarCafe(self, qtd):
    self.porcentCafe += qtd

  def fazerCafe(self):
    if(self.cafeteiraPronta == True):
      self.porcentAgua -= 10
      self.porcentCafe -= 15
      print('--- [CAFETEIRA] Café pronto.')
      self.cafeteiraPronta = False


def MedirAgua(cafeteira):
  print('--- [SENSOR] Medindo quantidade de água.')
  # GPIO.output(1, GPIO.HIGH)
  tempoTotal = cafeteira.TempoSensorAgua()
  # GPIO.output(1, GPIO.LOW)
  distancia = (tempoTotal * VEL_SOM) / 2
  return distancia

def MedirCafe(cafeteira):
  print('--- [SENSOR] Medindo quantidade de pó de café.')
  # GPIO.output(3, GPIO.HIGH)
  tempoTotal = cafeteira.TempoSensorCafe()
  # GPIO.output(3, GPIO.LOW)
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

def Main():
  cafeteira = Cafeteira(random.randint(0, 100), random.randint(0, 100))
  cmdLigarCafeteira = input("Ligar cafeteira? [S/N] ")
  if(cmdLigarCafeteira.upper() == 'S'):
    cafeteira.ligarCafeteira()
    
    comandosPreFazerCafe(cafeteira)

    if(cafeteira.cafeteiraPronta == True):
      cmdFazerCafe = input("Fazer café? [S/N] ")
      if(cmdFazerCafe.upper() == 'S'):
        cafeteira.fazerCafe()
        cmdFazerOutroCafe = input("Fazer outro café? [S/N] ")
        while(cmdFazerOutroCafe.upper() == 'S'):
          comandosPreFazerCafe(cafeteira)
          cafeteira.fazerCafe()
          cmdFazerOutroCafe = input("Fazer outro café? [S/N] ")
          if(cmdFazerOutroCafe.upper() == 'N'):
            cafeteira.desligarCafeteira()
            break
        if(cmdFazerOutroCafe.upper() == 'N'):
          cafeteira.desligarCafeteira()
          return
        
      elif(cmdFazerCafe.upper() == 'N'):
        cafeteira.desligarCafeteira()
        return

  elif(cmdLigarCafeteira.upper() == 'N'):
    return

Main()