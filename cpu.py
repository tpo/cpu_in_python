#!/usr/bin/python3

memory = [ ] # please fill this array with the code of your program. See the README.md.

import signal # for signal.pause()
import time
import threading

# register handles
ACC        = 0
PC         = 1
EQ         = 2

OP_NOP        =  0x00 # don't do anything
OP_LOAD       =  0x01 # load ACC from address
OP_STORE      =  0x02 # store ACC to address
OP_JMP        =  0x03 # jump to given address
OP_JSUB       =  0x04 # jump to subroutine
OP_SP_TO_ACC  =  0x05 # copy SP TO ACC
OP_ACC_TO_SP  =  0x06 # copy ACC to SP
OP_PUSH       =  0x07 # push register onto stack
OP_POP        =  0x08 # pop stack into register
OP_EQ         =  0x09 # compare ACC with value at address and set EQ flag
OP_JMP_EQ     =  0x0a # jump to given address if EQ flag is set
OP_INC        =  0x0d # increment value at address


# TODO: the following should only be allowed in Ring 0
OP_IRET       = 0x0c # return from exception, will pop the PC

# "macro"
OP_RET     = OP_POP # OP_RET PC   - return from subroutine
OP_YIELD   = OP_RET # OP_YIELD PC - return into scheduler

class Interrupt:
  def __init__(self):
    self.interrupt = False

  def signal(self):
    self.interrupt = True

  def acknowledge(self):
    self.interrupt = False

  def test(self):
    return self.interrupt

class Cpu:
  def __init__(self,memory,interrupt):
    self.acc = 0                  # accumulator
    self.operation = 0            # operation to execute
    self.operation_argument = 0   # operand
    self.pc = 0                   # program counter/instruction pointer
    self.sp = 0                   # stack pointer
    self.memory = memory          # RAM
    self.interrupt = interrupt    # signal interrupt
    self.interrupt_handler = 0x02 # hard coded!
    self.eq = False

    self.debug_watch_addr = [0x67,0x6c]

  def run(self):
    self.loop()

  def loop(self):
     while(True):
       self.dump_cpu_state()
       self.load_next_instruction_from_memory()
       self.execute_loaded_instruction()
       self.handle_interrupt()

  def handle_interrupt(self):
    if self.interrupt.test():
      print("handling an interrupt")
      self.interrupt.acknowledge()
      self.op_push(PC)
      self.pc = self.interrupt_handler

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
    elif( op == OP_SP_TO_ACC):
      self.op_sp_to_acc()
    elif( op == OP_ACC_TO_SP):
      self.op_acc_to_sp()
    elif( op == OP_PUSH ):
      self.op_push()
    elif( op == OP_POP ):
      self.op_pop()
    elif( op == OP_EQ):
      self.op_eq()
    elif( op == OP_JMP_EQ):
      self.op_jmp_eq()
    elif( op == OP_IRET):
      self.op_iret()
    elif( op == OP_INC):
      self.op_inc()
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
    self.op_push(PC)
    self.op_jmp()

  def op_push(self, operation_argument = None):
    self.sp = self.sp + 1

    if operation_argument == None:
      operation_argument = self.operation_argument

    if   operation_argument == ACC:
      value = self.acc
    elif operation_argument == PC:
      value = self.pc
    elif operation_argument == EQ:
      value = self.eq
    else:
      print("unknown operation_argument %d" % operation_argument)
      self.halt()

    self.memory[self.sp] = value

  def op_pop(self, operation_argument = None):
    stack_top = self.memory[self.sp]

    if operation_argument == None:
      operation_argument = self.operation_argument

    if   operation_argument == ACC:
      self.acc = stack_top
    elif operation_argument == PC:
      self.pc = stack_top
    elif operation_argument == EQ:
      self.eq = stack_top
    else:
      print("unknown operation_argument %d" % operation_argument)
      self.halt()

    self.sp = self.sp - 1

  def op_acc_to_sp(self):
    self.sp = self.acc

  def op_sp_to_acc(self):
    self.acc = self.sp

  def op_eq(self):
    self.eq = ( self.acc == self.memory[self.operation_argument] )

  def op_jmp_eq(self):
    if self.eq:
      self.op_jmp()

  def op_iret(self):
    self.op_pop(PC)

  def op_inc(self):
    self.memory[self.operation_argument] += 1

  def op_unknown(self):
    self.halt()

  def halt(self):
     print("system crashed")
     signal.pause() # sleep forever/until interrupted

  def dump_cpu_state(self):
    next_op = self.memory[self.pc]
    next_op_arg = self.memory[self.pc+1]
    print("PC:      %s" % hex(self.pc))
    print("OP_CODE: %s" % hex(next_op))
    print("OP_ASM:  %s" % self.op_to_asm(next_op))
    print("OP_ARG:  %d (%s)" % (next_op_arg, hex(next_op_arg)))
    print("ACC:     %d (%s)" % (self.acc, hex(self.acc)))
    print("SP:      %s" % hex(self.sp))
    print("INT:     %r" % self.interrupt.test())
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
    elif( op == OP_ACC_TO_SP):
      return "OP_ACC_TO_SP"
    elif( op == OP_SP_TO_ACC):
      return "OP_SP_TO_ACC"
    elif( op == OP_PUSH ):
      return "OP_PUSH"
    elif( op == OP_POP ):
      return "OP_POP/RET/YIELD"
    elif( op == OP_EQ):
      return "OP_EQ"
    elif( op == OP_JMP_EQ):
      return "OP_JMP_EQ"
    elif( op == OP_IRET):
      return "OP_IRET"
    elif( op == OP_INC):
      return "OP_INC"
    else:
      return "UNKNOWN: DATA?"

class Clock:
  def __init__(self, interrupt):
    self.interrupt = interrupt

  def run(self):
    while True:
        time.sleep(2)
        print("tick")
        self.interrupt.signal()

interrupt = Interrupt()

cpu_instance = Cpu( memory, interrupt )
cpu_thread = threading.Thread( target = cpu_instance.run )
cpu_thread.start()

clock_instance = Clock( interrupt )
clock_thread = threading.Thread( target = clock_instance.run )
clock_thread.start()

## wait for threads to terminate (they wont)
cpu_thread.join()
clock_thread.join()
