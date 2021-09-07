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

ATTENTION when working on this repo
-----------------------------------

Until this project is somewhat stable I intend to keep on
rewriting its git history. Justification: the goal here
is for the commits to reflect clear logical progress and
not the historic tribulations of its development.

That means that until this project is stable you can not
expect to be able to pull from this repo without major
conflicts.
