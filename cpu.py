#!/usr/bin/python3

import signal # for signal.pause()

OP_NOP   = 0 # don't do anything
OP_LOAD  = 1 # load ACC from address
OP_STORE = 2 # store ACC to address
OP_JMP   = 3 # jump to given address

# "macro"
OP_YIELD = OP_JMP # jump back into scheduler

# Memory contents:
#   0 -   3: program
#
DISPATCHER = [ # PROGRAM
               OP_JMP,       #  0  # JMP PROCESS1
               4,            #  1  #
               OP_JMP,       #  2  # JMP PROCESS2
               12            #  3  # 
             ]                     # 
                                   # 
# Memory contents:                 # 
#   4 -   9: program               # 
#  10 -  11: data                  # 
#                                  # 
PROCESS1 =  [ # PROGRAM            # 
              OP_LOAD,       #  4  # 
              10,            #  5  # 
              OP_STORE,      #  6  # 
              11,            #  7  # 
              OP_YIELD,      #  8  # JPM DISPATCHER:2
              2              #  9  # 
            ]                      \
              +                    \
            [ # DATA               # 
              11,            # 10  # 
              111            # 11  # 
            ]                      # 
                                   # 
# Memory contents:                 # 
#  12 -  17: program               # 
#  18 -  19: data                  # 
#                                  # 
PROCESS2 =  [ # PROGRAM            # 
              OP_LOAD,       # 12  # 
              18,            # 13  # 
              OP_STORE,      # 14  # 
              19,            # 15  # 
              OP_YIELD,      # 16  #  JPM DISPATCHER:0
              0              # 17  # 
            ]                      \
              +                    \
            [ # DATA               #
              22,            # 18  #
              222            # 19  #
            ] 

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
    self.memory = DISPATCHER   \
                    +          \
                  PROCESS1     \
                    +          \
                  PROCESS2

    self.debug_watch_addr = 11

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
    next_op = self.memory[self.pc]
    next_op_arg = self.memory[self.pc+1]
    print("PC:      %d" % self.pc)
    print("OP_CODE: %d" % next_op)
    print("OP_ASM:  %s" % self.op_to_asm(next_op))
    print("OP_ARG:  %d" % next_op_arg)
    print("ACC:     %d" % self.acc)
    print("mem[%d]: %d" % (self.debug_watch_addr, self.memory[self.debug_watch_addr]))
    print()

  def op_to_asm(self, op):
    if(   op == OP_NOP   ):
      return "OP_NOP"
    elif( op == OP_LOAD  ):
      return "OP_LOAD"
    elif( op == OP_STORE ):
      return "OP_STORE"
    elif( op == OP_JMP   ):
      return "OP_JMP"
    else:
      return "UNKNOWN: DATA?"

cpu = Cpu()

cpu.run()
