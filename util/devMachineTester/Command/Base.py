

class Base():
  name = None
  cmd = None
  def __init__(self, name, cmd):
    self.name = name
    self.cmd = cmd

  def run(self, context):
    pass #default is do nothing
