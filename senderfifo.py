import os
import time
fifopath1 = "my_program.fifo"
os.mkfifo(fifopath1)


for i in range(1,250):
  fifo = open(fifopath1, "w")
  fifo.write("Message No.: "+str(i)+"\n")
  #time.sleep(1)
  fifo.close()
