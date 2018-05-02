import os
import time
fifopath1 = "my_result.fifo"
a=os.mkfifo(fifopath1)
print(a)



fifo = open(fifopath1, "w")
time.sleep(3)
fifo.write("Mahendra Kumar..")
fifo.close()

