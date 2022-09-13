a "teaching device" CPU in Python
=================================

Goal
----

To demonstrate the major Operating Systems (OS) mechanisms
on a very simple, software-implemented CPU.

### Doubts

Q: Why on a software-implemented CPU?
A: Because in order to understand what fundamental problems
   need to be tackled in a computer system - and more specifically
   which of those problems' solutions are part of the OS -
   one needs to understand how those problems
   come about. So we create a CPU ourselves to see those
   problems emerge and then we solve them.

   We do the CPU in SW, because creating a working CPU has
   the lowest requirements when created as SW.

Stages
------

We're going to develop the CPU step by step. This are
our steps that we want to reach one by one:

* [ ] basic CPU:
  * [ ] has an accumulator ACC
  * [ ] has RAM
  * [ ] has a Programm Counter PC
  * [ ] can fetch operations from memory
  * [ ] can load a word from memory to ACC
  * [ ] can store the ACC to memory

* [ ] collaborative multitasking

ATTENTION when working on this repo
-----------------------------------

Until this project is somewhat stable I intend to keep on
rewriting its git history. Justification: the goal here
is for the commits to reflect clear logical progress and
not the historic tribulations of its development.

That means that until this project is stable you can not
expect to be able to pull from this repo without major
conflicts.

Understanding what's in this repo and how to run the cpu.py
-----------------------------------------------------------

* `cpu.py`
  * this is a minimal virtual CPU written in Python. It has a memory,
    but the memory is empty. Its memory needs to be filled with
    machine code and data in order to do something useful. This CPU
    has the "Tpo" instruction set (just a random name).

* `program.asm`
  * this is example assembler code that solves the above stated
    problems:
    * it contains a minimal "OS"
    * it contains to processes or "programs"
    * it contains an interrupt handler to do context switching
      between processes

* `program.lst`
  * this is the generated machine code for the given cpu from
    `program.asm`. This code has been generated with
    [kasm](https://github.com/tpo/kasm-generic/ for the "Tpo" CPU
    instruction set.

* `lst_to_commented_bytes.py`
  * this will transform `program.list` into a python array along
    with comments, so that it can be used by the `cpu.py`

* `cpu_with_program.py` - this is the cpu.py code coupled with
  "memory" generated from `program.lst`. That is this is the
  `cpu.py` with code and data from `program.asm` running on it.

* `run_program`
  * combines all the necessary steps and executes `program.asm` on
    the `cpu.py`
    1. calls `kasm.py` to generate `program.lst` from `program.asm`
    2. calls `lst_to_commented_bytes.py` to generate a python
       `memory` array from `program.lst`
    3. combines `cpu.py` and the generated `memory` array from the
       previous step into a `cpu_with_program.py` executable
    4. executes `cpu_with_program.py`

