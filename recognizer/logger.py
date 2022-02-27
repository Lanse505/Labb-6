import datetime

class Logger(object):
  
  def Logger(self, identity: str = __file__, debugEnabled: bool = False):
    self.__init__(self, identity, debugEnabled)

  def __init__(self, identity: str, debugEnabled: bool):
      self.identity = identity
      self.debugEnabled = debugEnabled

  def info(self, input: str):
    print(f"\n {self.getTimeStamp}[INFO]: {input}")

  def debug(self, input: str):
    if (self.debugEnabled):
      print(f"\n {self.getTimeStamp}[DEBUG]: {input}")

  def warn(self, input: str):
    print(f"\n {self.getTimeStamp}[WARN]: {input}")

  def getTimeStamp(self):
    rawStamp = datetime.datetime.now()
    splitStamp = rawStamp.split(' ')
    stamp = f"[{splitStamp[0]}][{splitStamp[1][0:7]}]"
    return stamp