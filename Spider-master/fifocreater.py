import os
import time
fifopath1 = "my_result.fifo"
fifopath2= "my_baseurl.fifo"
os.mkfifo(fifopath1)
os.mkfifo(fifopath2)


