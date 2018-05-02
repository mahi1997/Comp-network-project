import os
import sys

path = "my_result.fifo"
fifo = open(path, "r")
for line in fifo:
  
   print(line)
  
fifo.close()

