#!/usr/bin/python3
#
# ATTENTION: THIS IS A GENERATED FILE!

memory = [       #                                    ; we have two processes that the OS context switched between
      #                                    ;
      #                                    ; each process has its own stack
      #                                    ;
      #                                    ; the stack holds the PCB (process control block) of each process
      #                                    ;
      #                                    ; the variables proc_1_sp and proc_2_sp hold the address of the
      #                                    ; respective stack of each process (aka each process' stack pointer SP)
      #                                    ;
      #   
      #                                    ; op_push and op_pop have an argument that determines on
      #                                    ; which register they act:
      #   
      #                                    ; acc = #0
      #                                    ; pc  = #1
      #                                    ; eq  = #2
      #                                    ;
      #                                    ; Examples:
      #                                    ;
      #                                    ; * `op_push #0` will push the ACC register on the stack
      #                                    ; * `op_pop  #1` will pop the top value from the stack and put it into
      #                                    ;                the program counter PC
      #                                    ;
      #   
0x03, # 0000                               init:                 op_jmp start_os_init      ; jump into operating system initialization code
0x24, #
      #   
      #                                    ; isr starts hardcoded at 0x02!
      #   
0x07, # 0002                               isr:                  op_push #0                ; save ACC on stack. PC gets saved on stack by CPU
0x00, #
0x07, # 0004                                                     op_push #2                ; save EQ on stack. PC gets saved on stack by CPU
0x02, #
      #   
0x01, # 0006                                                     op_load proc_1_id         ; who's running? proc_1 or proc_2 ?
0x64, #
0x09, # 0008                                                     op_eq running_proc        ; if it's proc_1
0x61, #
0x0A, # 000A                                                     op_jmp_eq run_proc_2      ; then run proc_2 now
0x14, #
      #                                                                                    ; else run proc_1
      #   
      #   
0x01, # 000C                               run_proc_1:           op_load proc_1_id         ; memorize that we'll run proc_1 now
0x64, #
0x02, # 000E                                                     op_store running_proc
0x61, #
0x01, # 0010                                                     op_load proc_1_sp
0x62, #
0x03, # 0012                                                     op_jmp isr_common
0x1C, #
      #   
0x01, # 0014                               run_proc_2:           op_load proc_2_id         ; memorize that we'll run proc_2 now
0x65, #
0x02, # 0016                                                     op_store running_proc
0x61, #
0x01, # 0018                                                     op_load proc_2_sp
0x63, #
0x03, # 001A                                                     op_jmp isr_common
0x1C, #
      #   
0x06, # 001C                               isr_common:           op_acc_to_sp
0x00, #
0x08, # 001E                                                     op_pop #2                 ; restore EQ from stack
0x02, #
0x08, # 0020                                                     op_pop #0                 ; restore ACC from stack
0x00, #
0x0C, # 0022                                                     op_iret                   ; will use PC on stack
0x00, #
      #   
0x00, # 0024                               start_os_init:        op_nop                    ; beginning of the OS initialization code
0x00, #
      #   
      #                                    ; we set up proc1's and proc2's stacks or respectively
      #                                    ; their PCB's (process control blocks) so that once an
      #                                    ; interrupt happens the interrupt routine can get proc1's
      #                                    ; and proc2's state from the stack/PCB, restore it and
      #                                    ; jump into the respective process
      #                                    ;
      #                                    ; a PCB and a stack are not the same thing, but here we save
      #                                    ; the PCB on the stack
      #                                    ;
0x01, # 0026                               init_proc_1:          op_load proc_1_stack_addr ; read proc1's stack address
0x5D, #
0x06, # 0028                                                     op_acc_to_sp              ; save proc1's stack address in the stack pointer
0x00, #
      #                                                                                    ; now the stack pointer points to proc_1's stack
0x01, # 002A                                                     op_load proc_1_addr       ; load the address of proc1's code
0x5F, #
0x07, # 002C                                                     op_push #0                ; save proc1's PC on the stack (== start address)
0x00, #
0x01, # 002E                                                     op_load zero              ; initialize the ACC with a zero
0x66, #
0x07, # 0030                                                     op_push #0                ; save the ACC (zero) on the stack/PCB
0x00, #
0x07, # 0032                                                     op_push #0                ; save the EQ flag (zero) on the stack/PCB
0x00, #
0x05, # 0034                                                     op_sp_to_acc              ; save the SP pointer in the ACC
0x00, #
0x02, # 0036                                                     op_store proc_1_sp        ; remember where proc1's stack/PCB is
0x62, #
      #   
0x01, # 0038                               init_proc_2:          op_load proc_2_stack_addr ; same as init_proc_1 for proc_2
0x5E, #
0x06, # 003A                                                     op_acc_to_sp
0x00, #
0x01, # 003C                                                     op_load proc_2_addr
0x60, #
0x07, # 003E                                                     op_push #0
0x00, #
0x01, # 0040                                                     op_load zero
0x66, #
0x07, # 0042                                                     op_push #0
0x00, #
0x07, # 0044                                                     op_push #0
0x00, #
0x05, # 0046                                                     op_sp_to_acc
0x00, #
0x02, # 0048                                                     op_store proc_2_sp
0x63, #
      #   
      #                                                          ; now setup the OS' own stack. This is done because
      #                                                          ; once the first interrupt happens, the interrupt procedure
      #                                                          ; will *also* save the current CPU state onto the current stack.
      #                                                          ; therefore we need to make sure the current stack is correctly
      #                                                          ; set up for the interrupt routine to be able to do it's thing
0x01, # 004A                                                     op_load os_init_stack_addr ; get address of OS' own stack
0x5C, #
0x06, # 004C                                                     op_acc_to_sp              ; save it in the stack pointer SP
0x00, #
0x03, # 004E                               init_end:             op_jmp init_end           ; do nothing/idle/wait for interrupt/scheduling
0x4E, #
      #                                                                                    ; to happen/to start
      #   
      #                                    ; first process
      #                                                          ; code of first process
0x0D, # 0050                               proc_1:               op_inc data_1
0x67, #
0x03, # 0052                                                     op_jmp proc_1
0x50, #
      #   
      #                                    ; second process
      #                                                          ; code of second process
0x0D, # 0054                               proc_2:               op_inc data_2
0x6C, #
0x03, # 0056                                                     op_jmp proc_2
0x54, #
      #   
0x00, # 0058                               os_init_stack:        db 0,0,0,0
0x00, #
0x00, #
0x00, #
      #   
0x58, # 005C                               os_init_stack_addr:   db os_init_stack       ; address of OS stack
      #   
0x68, # 005D                               proc_1_stack_addr:    db stack_1
0x6D, # 005E                               proc_2_stack_addr:    db stack_2
      #   
0x50, # 005F                               proc_1_addr:          db proc_1
0x54, # 0060                               proc_2_addr:          db proc_2
      #   
0x01, # 0061                               running_proc:         db 1
      #   
      #                                    ; the saved stack pointers of both processes, pointing
      #                                    ; to the stacks/PCBs of each process
0x00, # 0062                               proc_1_sp:            db 0
0x00, # 0063                               proc_2_sp:            db 0
      #   
      #                                    ; the PID's (process IDs) of each process
0x01, # 0064                               proc_1_id:            db 1
0x02, # 0065                               proc_2_id:            db 2
      #   
0x00, # 0066                               zero:                 db 0
      #   
      #                                    ; data of first process
0x00, # 0067                               data_1:               db 0
      #                                    ; the stack of the first process, holding the PCB
      #                                    ; of the first process
0x00, # 0068                               stack_1:              db 0,0,0,0
0x00, #
0x00, #
0x00, #
      #   
      #                                    ; data of second process
0x64, # 006C                               data_2:               db 100
      #                                    ; stack/PCB of the second process
0x00, # 006D                               stack_2:              db 0,0,0,0
0x00, #
0x00, #
0x00, #
      #   
]


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
