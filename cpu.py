#!/usr/bin/python3

import signal # for signal.pause()

OP_NOP     = 0 # don't do anything
OP_LOAD    = 1 # load ACC from address
OP_STORE   = 2 # store ACC to address
OP_JMP     = 3 # jump to given address
OP_JSUB    = 4 # jump to subroutine
OP_RET     = 5 # return from subroutine
OP_SET_SP  = 6 # copy ACC to SP

# "macro"
OP_YIELD   = OP_RET # return into scheduler

OO         = 0 # NO_DATA

INIT_STACK = [ # PROGRAM
               OP_LOAD,      #  0  #
               6,            #  1  # INIT_STACK.DATA
               OP_SET_SP,    #  2  #
               0,            #  3  # 
               OP_JMP,       #  4  #
               7             #  5  # DISPATCHER
             ]                     \
               +                   \
             [ # DATA              #
               29,           #  6  # STACK
             ]                     #
                                   # 
DISPATCHER = [ # PROGRAM           #
               OP_JSUB,      #  7  #
               13,           #  8  # PROCESS1
               OP_JSUB,      #  9  #
               21,           # 10  # PROCESS2 
               OP_JMP,       # 11  #
               7             # 12  # DISPATCHER 
             ]                     # 
PROCESS1 =  [ # PROGRAM            # 
              OP_LOAD,       # 13  # 
              19,            # 14  # PROCESS1.DATA.0
              OP_STORE,      # 15  # 
              20,            # 16  # PROCESS1.DATA.1
              OP_YIELD,      # 17  # RETURN
              OO             # 18  # 
            ]                      \
              +                    \
            [ # DATA               # 
              11,            # 19  # 
              111            # 20  # 
            ]                      # 
PROCESS2 =  [ # PROGRAM            # 
              OP_LOAD,       # 21  # 
              27,            # 22  # PROCESS2.DATA.0
              OP_STORE,      # 23  # 
              28,            # 24  # PROCESS3.DATA.0
              OP_YIELD,      # 25  #
              OO             # 26  #
            ]                      \
              +                    \
            [ # DATA               #
              22,            # 27  #
              222            # 28  #
            ]                      #
STACK    =  [ # STACK        # 29  #
              0              # ... #
            ] * 10

class Cpu:
  def __init__(self):
    self.acc = 0                  # accumulator
    self.operation = 0            # operation to execute
    self.operation_argument = 0   # operand
    self.pc = 0                   # program counter/instruction pointer
    self.sp = 0                   # stack pointer

    # Memory contents:
    #   0 -   5: program
    #   6 -   7: data
    #   8 - 100: empty (NOP) memory
    #
    self.memory = INIT_STACK   \
                    +          \
                  DISPATCHER   \
                    +          \
                  PROCESS1     \
                    +          \
                  PROCESS2     \
                    +          \
                  STACK

    self.debug_watch_addr = [20,28,29,30]

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
    elif( op == OP_JSUB   ):
      self.op_jsub()
    elif( op == OP_RET   ):
      self.op_ret()
    elif( op == OP_SET_SP):
      self.op_set_sp()
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

  def op_jsub(self):
    self.sp = self.sp + 1
    self.memory[self.sp] = self.pc
    self.op_jmp()

  def op_ret(self):
    self.pc = self.memory[self.sp]
    self.sp = self.sp - 1

  def op_set_sp(self):
    self.sp = self.acc

  def op_unknown(self):
    self.halt()

  def halt(self):
     print("system crashed")
     signal.pause() # sleep forever/until interrupted

  def dump_cpu_state(self):
    next_op = self.memory[self.pc]
    next_op_arg = self.memory[self.pc+1]
    print("PC:      %d" % self.pc)
    print("OP_CODE: %d" % next_op)
    print("OP_ASM:  %s" % self.op_to_asm(next_op))
    print("OP_ARG:  %d" % next_op_arg)
    print("ACC:     %d" % self.acc)
    print("SP:      %d" % self.sp)
    for mem_adr in self.debug_watch_addr:
       print("mem[%d]: %d" % (mem_adr, self.memory[mem_adr]))
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
    elif( op == OP_JSUB   ):
      return "OP_JSUB"
    elif( op == OP_RET   ):
      return "OP_RET"
    elif( op == OP_SET_SP):
      return "OP_SET_SP"
    else:
      return "UNKNOWN: DATA?"

cpu = Cpu()

cpu.run()
