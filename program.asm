; we have two processes that the OS context switched between
;
; each process has its own stack
;
; the stack holds the PCB (process control block) of each process
; 
; the variables proc_1_sp and proc_2_sp hold the address of the
; respective stack of each process (aka each process' stack pointer SP)
;

; op_push and op_pop have an argument that determines on
; which register they act:

; acc = #0
; pc  = #1
; eq  = #2
;
; Examples:
;
; * `op_push #0` will push the ACC register on the stack
; * `op_pop  #1` will pop the top value from the stack and put it into
;                the program counter PC
;

init:                 op_jmp start_os_init      ; jump into operating system initialization code

; isr starts hardcoded at 0x02!

isr:                  op_push #0                ; save ACC on stack. PC gets saved on stack by CPU
                      op_push #2                ; save EQ on stack. PC gets saved on stack by CPU

                      op_load proc_1_id         ; who's running? proc_1 or proc_2 ?
                      op_eq running_proc        ; if it's proc_1
                      op_jmp_eq run_proc_2      ; then run proc_2 now
                                                ; else run proc_1


run_proc_1:           op_load proc_1_id         ; memorize that we'll run proc_1 now
                      op_store running_proc 
                      op_load proc_1_sp
                      op_jmp isr_common

run_proc_2:           op_load proc_2_id         ; memorize that we'll run proc_2 now
                      op_store running_proc 
                      op_load proc_2_sp
                      op_jmp isr_common

isr_common:           op_acc_to_sp
                      op_pop #2                 ; restore EQ from stack
                      op_pop #0                 ; restore ACC from stack
                      op_iret                   ; will use PC on stack

start_os_init:        op_nop                    ; beginning of the OS initialization code

; we set up proc1's and proc2's stacks or respectively
; their PCB's (process control blocks) so that once an
; interrupt happens the interrupt routine can get proc1's
; and proc2's state from the stack/PCB, restore it and
; jump into the respective process
;
; a PCB and a stack are not the same thing, but here we save
; the PCB on the stack
;
init_proc_1:          op_load proc_1_stack_addr ; read proc1's stack address
                      op_acc_to_sp              ; save proc1's stack address in the stack pointer
                                                ; now the stack pointer points to proc_1's stack
                      op_load proc_1_addr       ; load the address of proc1's code
                      op_push #0                ; save proc1's PC on the stack (== start address)
                      op_load zero              ; initialize the ACC with a zero
                      op_push #0                ; save the ACC (zero) on the stack/PCB
                      op_push #0                ; save the EQ flag (zero) on the stack/PCB
                      op_sp_to_acc              ; save the SP pointer in the ACC
                      op_store proc_1_sp        ; remember where proc1's stack/PCB is

init_proc_2:          op_load proc_2_stack_addr ; same as init_proc_1 for proc_2
                      op_acc_to_sp
                      op_load proc_2_addr
                      op_push #0
                      op_load zero
                      op_push #0
                      op_push #0
                      op_sp_to_acc
                      op_store proc_2_sp

                      ; now setup the OS' own stack. This is done because
                      ; once the first interrupt happens, the interrupt procedure
                      ; will *also* save the current CPU state onto the current stack.
                      ; therefore we need to make sure the current stack is correctly
                      ; set up for the interrupt routine to be able to do it's thing
                      op_load os_init_stack_addr ; get address of OS' own stack
                      op_acc_to_sp              ; save it in the stack pointer SP
init_end:             op_jmp init_end           ; do nothing/idle/wait for interrupt/scheduling
                                                ; to happen/to start

; first process
                      ; code of first process
proc_1:               op_inc data_1
                      op_jmp proc_1

; second process
                      ; code of second process
proc_2:               op_inc data_2
                      op_jmp proc_2

os_init_stack:        db 0,0,0,0

os_init_stack_addr:   db os_init_stack       ; address of OS stack

proc_1_stack_addr:    db stack_1
proc_2_stack_addr:    db stack_2

proc_1_addr:          db proc_1
proc_2_addr:          db proc_2

running_proc:         db 1

; the saved stack pointers of both processes, pointing
; to the stacks/PCBs of each process
proc_1_sp:            db 0
proc_2_sp:            db 0

; the PID's (process IDs) of each process
proc_1_id:            db 1
proc_2_id:            db 2

zero:                 db 0

; data of first process
data_1:               db 0
; the stack of the first process, holding the PCB
; of the first process
stack_1:              db 0,0,0,0

; data of second process
data_2:               db 100
; stack/PCB of the second process
stack_2:              db 0,0,0,0

