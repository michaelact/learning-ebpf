#!/usr/bin/python3  
from bcc import BPF
from time import sleep

program = r"""
BPF_HASH(counter_table);

TRACEPOINT_PROBE(raw_syscalls, sys_enter)
{
   u64 key = args->id;
   u64 counter = 0;
   u64 *p;

   p = counter_table.lookup(&key);
   if (p != 0) {
      counter = *p;
   }
   counter++;
   counter_table.update(&key, &counter);
   return 0;
}
"""

b = BPF(text=program)

while True:
    sleep(2)
    s = ""
    for k,v in b["counter_table"].items():
        s += f"ID {k.value}: {v.value}\t"
    print(s)
