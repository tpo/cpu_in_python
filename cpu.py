#!/usr/bin/python3

OP_NOP   = 0 # don't do anything

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
    self.operation = self.memory[self.pc]
    self.pc = self.pc + 1
    self.operation_argument = self.memory[self.pc]
    self.pc = self.pc + 1

  def execute_loaded_instruction(self):
    # read operation
    if( self.operation == OP_NOP ):
      self.op_nop()

  def op_nop(self):
    print("executed nop")

cpu = Cpu()

cpu.run()
