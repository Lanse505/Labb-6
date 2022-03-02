import datetime
from time import strftime

class Logger(object):
  
  def Logger(self, identity: str = __file__, debugEnabled: bool = False):
    self.__init__(self, identity, debugEnabled)

  def __init__(self, identity: str, debugEnabled: bool):
      self.identity = identity
      self.debugEnabled = debugEnabled

  def info(self, input: str):
    print(f"{self.getTimeStamp()}[{self.identity}][INFO]: {input}")

  def debug(self, input: str):
    if (self.debugEnabled):
      print(f"{self.getTimeStamp()}[{self.identity}][DEBUG]: {input}")

  def warn(self, input: str):
    print(f"{self.getTimeStamp()}[{self.identity}][WARN]: {input}")

  def getTimeStamp(self):
    rawStamp = datetime.datetime.now()
    dateStr = r"%d/%m/%Y"
    timeStr = r"%H:%M:%S"
    stamp = f"[{rawStamp.strftime(dateStr)}][{rawStamp.strftime(timeStr)}]"
    return str(stamp)