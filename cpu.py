#!/usr/bin/python3

import signal # for signal.pause()

OP_NOP   = 0 # don't do anything
OP_LOAD  = 1 # load ACC from address
OP_STORE = 2 # store ACC to address
OP_JMP   = 3 # jump to given address

class Cpu:
  def __init__(self):
    self.acc = 0
    self.operation = 0
    self.operation_argument = 0
    self.pc = 0

    # Memory contents:
    #   0 -   5: program
    #   6 -   7: data
    #   8 - 100: empty (NOP) memory
    #
    self.memory = [ # PROGRAM
                    OP_LOAD,
                    6,
                    OP_STORE,
                    7,
                    OP_JMP,
                    0
                  ]            \
                    +          \
                  [ # DATA
                    77,
                    78
                  ]            \
                    +          \
                  [ 0 ] * 92

    self.debug_watch_addr = 7

  def run(self):
    self.loop()

  def loop(self):
     while(True):
       self.dump_cpu_state()
       self.load_next_instruction_from_memory()
       self.execute_loaded_instruction()

  def load_next_instruction_from_memory(self):
    self.operation          = self.memory[self.pc]
    self.operation_argument = self.memory[self.pc + 1]
    self.pc = self.pc + 2

  def execute_loaded_instruction(self):
    op = self.operation
    if(   op == OP_NOP   ):
      self.op_nop()
    elif( op == OP_LOAD  ):
      self.op_load()
    elif( op == OP_STORE ):
      self.op_store()
    elif( op == OP_JMP   ):
      self.op_jmp()
    else:
      self.op_unknown()


  def op_nop(self):
    print("executed nop")

  def op_load(self):
    self.acc = self.memory[self.operation_argument]

  def op_store(self):
    self.memory[self.operation_argument] = self.acc

  def op_jmp(self):
    self.pc = self.operation_argument

  def op_unknown(self):
    self.halt()

  def halt(self):
     print("CPU crashed")
     signal.pause() # sleep forever/until interrupted

  def dump_cpu_state(self):
    print("CPU state")
    print("---------")
    print("ACC:     %d" % self.acc)
    print("OP:      %d" % self.operation)
    print("OP_ARG:  %d" % self.operation_argument)
    print("PC:      %d" % self.pc)
    print("mem[%d]: %d" % (self.debug_watch_addr, self.memory[self.debug_watch_addr]))

cpu = Cpu()

cpu.run()
