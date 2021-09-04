#!/usr/bin/python3

OP_NOP   = 0 # don't do anything
OP_LOAD  = 1 # load ACC from address
OP_STORE = 2 # store ACC to address

class Cpu:
  def __init__(self):
    self.acc = 0
    self.operation = 0
    self.operation_argument = 0
    self.pc = 0

    # Memory contents:
    #   0 -   3: program
    #   4 -   5: data
    #   6 - 100: empty (NOP) memory
    #
    self.memory = [ # PROGRAM
                    OP_LOAD,
                    4,
                    OP_STORE,
                    5
                  ]            \
                    +          \
                  [ # DATA
                    77,
                    78
                  ]            \
                    +          \
                  [ 0 ] * 94

  def run(self):
    self.loop()

  def loop(self):
     while(True):
       self.dump_cpu_state()
       self.load_next_instruction_from_memory()
       self.execute_loaded_instruction()

  def load_next_instruction_from_memory(self):
    self.operation = self.memory[self.pc]
    self.pc = self.pc + 1
    self.operation_argument = self.memory[self.pc]
    self.pc = self.pc + 1

  def execute_loaded_instruction(self):
    if( self.operation == OP_NOP ):
      self.op_nop()
    if( self.operation == OP_LOAD  ):
      self.op_load()
    if( self.operation == OP_STORE ):
      self.op_store()


  def op_nop(self):
    print("executed nop")

  def op_load(self):
    self.acc = self.memory[self.operation_argument]

  def op_store(self):
    self.memory[self.operation_argument] = self.acc


  def dump_cpu_state(self):
    print("CPU state")
    print("---------")
    print("ACC:    %d" % self.acc)
    print("OP:     %d" % self.operation)
    print("OP_ARG: %d" % self.operation_argument)
    print("PC:     %d" % self.pc)

cpu = Cpu()

cpu.run()
