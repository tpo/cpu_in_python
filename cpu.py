class Cpu:
  def __init__(self):
    self.acc = [0,0]
    self.operation = 0
    self.operation_argument = 0
    self.pc = 0

    self.memory = [0] * 100

  def run(self):
    self.loop()

  def loop(self):
     while(True):
       self.load_next_instruction_from_memory()
       self.execute_loaded_instruction()

  def load_next_instruction_from_memory(self):
    print("load")

  def execute_loaded_instruction(self):
    print("exec")

cpu = Cpu()

cpu.run()
