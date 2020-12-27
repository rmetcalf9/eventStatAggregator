from .Base import Base


class CmdQuit(Base):
  def __init__(self):
    super().__init__(name="Quit", cmd="q")

  def run(self, context):
    context["running"] = False
