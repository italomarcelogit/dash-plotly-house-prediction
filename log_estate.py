from loguru import logger
from datetime import datetime
import socket
meuip = socket.gethostbyname(socket.gethostname())

def agora():
  return datetime.now().strftime("%Y-%d-%m %H:%M:%S")

def inicializaLog():
    logger.add("data/coleta.log", 
             format="{extra[ip]} | {extra[agora]} ({extra[user]}): {message}",
             rotation="1 week", backtrace=True, diagnose=True) 
    logger.bind(ip="127.0.0.1", agora=agora(), user="italomarcelo").info("Iniciando ambiente de coleta de dados")

def meuLog(MSG, TIPO="INFO", USER='italomarcelo'):
   if TIPO == "INFO":
      logger.bind(ip=meuip, agora=agora(), user=USER).info(MSG)
   elif TIPO == "WARNING":
      logger.bind(ip=meuip, agora=agora(), user=USER).warning(MSG)
    
