import wx
import wx.lib.scrolledpanel
import threading
from Queue import Queue
from spider import Spider
from domain import *
from general import *
import os
import sys
######################################
pathurl = "my_baseurl.fifo"
fifourl = open(pathurl, "r")
for firsturl in fifourl:
   HOMEPAGE = firsturl
   
fifourl.close()
#########################################

delete_file_contents()
create_data_files(HOMEPAGE)
####################################
#PROJECT_NAME = 'viper-seo'
#HOMEPAGE = 'http://www.cplusplus.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
#QUEUE_FILE = PROJECT_NAME + '/queue.txt'
QUEUE_FILE = 'queue.txt'
CRAWLED_FILE = 'crawled.txt'
#CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()

working=True

#Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
Spider(HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    global working
    while working:
        url = queue.get()

        #if(queue.empty()):
           # working=False
            #sys.exit()
            #print("###############################################################\n###############################################################\n###############################################################\n")
        
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

    
# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
