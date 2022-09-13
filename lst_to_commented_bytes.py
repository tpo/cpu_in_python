#!/usr/bin/python3

import re

print( "memory = [ ", end='')

with open('program.lst') as f:
    line_no = 0
    # excerpt from program.lst:
    #
    #     1:                                 ; acc = $0
    #     2:                                 ; pc  = $1
    #     3:                                 ; eq  = $2
    #     4:                                 
    #     [...]
    #     28:  0028  01 36                                           op_load init_stack_addr   ; setup init's own stack
    #     29:                                                                            ; so the scheduler can write init's
    #     30:                                                                            ; registers somewhere upon first scheduling
    #     31:  002A  06 00                                           op_acc_to_sp
    #     32:  002C  03 2C                          init_end:        op_jmp init_end           ; wait for scheduling to start
    #     33:
    #     34:  002E  00 00 00 00 00 00              init_stack:      db 0,0,0,0,0,0
    #
    for line in f:
        if line_no == 0:
            # ignore first line that looks like this:
            #
            #     File program.asm
            #
            pass # nop
        else:
          # remove spaces left
          line = line.lstrip()
          # remove newline
          line = line.rstrip()
          # remove line numbers "28:"
          line = re.sub( "^\d+:",  "", line)
          # if line has an address "0028" - that is: if it
          # contains generated memory content:
          if re.search( "^  [0-9A-F]{4}  ", line) != None:
            # drop leading spaces
            line = line.lstrip()
            address = re.sub( "  .*", "", line)
            line = re.sub( "^[0-9A-F]{4}  ", "", line)

            mem_bytes = []
            pad_spaces = ""
            # read in generated memory bytes "01 36"
            while re.search( "^[0-9A-F]{2} ", line) != None:
              pad_spaces += "   "
              next_byte = re.sub( " .*", "", line)
              next_byte = "0x" + next_byte + ", #"
              # rest of line
              line = re.sub( "^[0-9A-F]{2} ", "", line)
              mem_bytes.append(next_byte)
            # first byte gets the rest of the line (aka the comment)
            mem_bytes[0] = mem_bytes[0] + " " + address + pad_spaces + line
            # print out all bytes
            for next_byte in mem_bytes:
              print( next_byte)

          # print line that only contains comments
          else:
            line = "      #   " + line
            print(line)

        line_no += 1

print( "]")
