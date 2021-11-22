; acc = $0
; pc  = $1
; eq  = $2

init:            op_load isr_addr
                 op_set_int

init_proc_1:     op_load proc_1_stack_addr ; save proc1's registers on its stack
                 op_acc_to_sp              ; use proc_1's stack
                 op_load proc_1_addr
                 op_push #0                ; save PC   (== start address)
                 op_load zero_addr
                 op_push #0                ; save ACC  (== zero)
                 op_push #0                ; save EQ   (== zero)
                 op_sp_to_acc              ; get SP
                 op_store proc_1_sp        ; save SP in PCB

init_proc_2:     op_load proc_2_stack_addr ; same as init_proc_1 for proc_2
                 op_acc_to_sp
                 op_load proc_2_addr
                 op_push #0
                 op_load zero_addr
                 op_push #0
                 op_push #0
                 op_sp_to_acc
                 op_store proc_2_sp

                 op_load init_stack_addr   ; setup init's own stack
                                           ; so the scheduler can write init's
                                           ; registers somewhere upon first scheduling
                 op_acc_to_sp
init_end:        op_jmp init_end           ; wait for scheduling to start

init_stack:      db 0,0,0,0,0,0


isr_addr:        db isr
zero_addr:       db zero
init_stack_addr: db init_stack
pad0:            db 0

proc_1_stack_addr:    db stack_1
proc_2_stack_addr:    db stack_2

proc_1_addr:     db proc_1
proc_2_addr:     db proc_2

isr:             op_push #0                ; save ACC on stack. PC gets saved on stack by CPU
                 op_push #2                ; save EQ on stack. PC gets saved on stack by CPU

                 op_load proc_1_id         ; who's running? proc_1 or proc_2 ?
                 op_eq running_proc        ; if it's proc_1
                 op_jmp_eq run_proc_2      ; then run proc_2 now
                                           ; else run proc_1

run_proc_1:      op_load proc_1_id         ; memorize that we'll run proc_1 now
                 op_store running_proc 
                 op_load proc_1_sp
                 op_jmp isr_common

run_proc_2:      op_load proc_2_id         ; memorize that we'll run proc_2 now
                 op_store running_proc 
                 op_load proc_2_sp
                 op_jmp isr_common

isr_common:      op_acc_to_sp
                 op_pop #2
                 op_pop #0
                 op_iret                ; will use PC on stack

running_proc:    db 1
pad1:            db 0

proc_1_sp:       db 0
proc_2_sp:       db 0

proc_1_id:       db 1
proc_2_id:       db 2

proc_2_inited:   db 0
not_inited:      db 0
zero:            db 0
pad2:            db 0

proc_1:          op_load data_1_1
                 op_store data_1_2
                 op_jmp proc_1
data_1_1:        db 11
data_1_2:        db 111
stack_1:         db 0,0,0,0

proc_2:          op_load data_2_1
                 op_store data_2_2
                 op_jmp proc_2
data_2_1:        db 22
data_2_2:        db 222
stack_2:         db 0,0,0,0

