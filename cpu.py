#!/usr/bin/python3

import signal # for signal.pause()
import time
import threading

OP_NOP     = 0 # don't do anything
OP_LOAD    = 1 # load ACC from address
OP_STORE   = 2 # store ACC to address
OP_JMP     = 3 # jump to given address
OP_JSUB    = 4 # jump to subroutine
OP_SET_SP  = 5 # copy ACC to SP
OP_PUSH_PC = 6 # push PC to stack
OP_POP_PC  = 7 # pop stack into PC
OP_PUSH    = 6 # push ACC to stack
OP_POP     = 7 # pop stack into ACC

# TODO: the following should only be allowed in Ring 0
OP_SET_INT = 8 # copy ACC to interrupt handler pointer

# "macro"
OP_RET     = OP_POP_PC # return from subroutine
OP_YIELD   = OP_RET    # return into scheduler

import program

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
    self.interrupt_handler = 0

    self.debug_watch_addr = [20,28,29,30]

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
      self.op_push_pc()
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
    elif( op == OP_SET_SP):
      self.op_set_sp()
    elif( op == OP_PUSH_PC ):
      self.op_push_pc()
    elif( op == OP_POP_PC ):
      self.op_pop_pc()
    elif( op == OP_PUSH ):
      self.op_push()
    elif( op == OP_POP ):
      self.op_pop()
    elif( op == OP_SET_INT):
      self.op_set_int()
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
    self.op_push_pc()
    self.op_jmp()

  def push(self,value):
    self.sp = self.sp + 1
    self.memory[self.sp] = value

  def pop(self):
    stack_top = self.memory[self.sp]
    self.sp = self.sp - 1
    return stack_top

  def op_set_sp(self):
    self.sp = self.acc

  def op_push_pc(self):
    self.push(self.pc)

  def op_pop_pc(self):
    self.pc = self.pop()

  def op_push(self):
    self.push(self.acc)

  def op_pop(self):
    self.acc = self.pop()

  def op_set_int(self):
    self.interrupt_handler = self.acc

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
    elif( op == OP_SET_SP):
      return "OP_SET_SP"
    elif( op == OP_PUSH_PC ):
      return "OP_PUSH_PC"
    elif( op == OP_POP_PC ):
      return "OP_POP_PC/RET/YIELD"
    elif( op == OP_PUSH ):
      return "OP_PUSH"
    elif( op == OP_POP ):
      return "OP_POP"
    elif( op == OP_SET_INT):
      return "OP_SET_INT"
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

cpu_instance = Cpu( program.executable, interrupt )
cpu_thread = threading.Thread( target = cpu_instance.run )
cpu_thread.start()

clock_instance = Clock( interrupt )
clock_thread = threading.Thread( target = clock_instance.run )
clock_thread.start()

## wait for threads to terminate (they wont)
cpu_thread.join()
clock_thread.join()
