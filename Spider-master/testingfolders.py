import os
from general import *

queue = set()
crawled = set()

queue.add('link 1')
queue.add('link 2')

crawled.add('clink 3')
crawled.add('clink 4')

set_to_file(queue,'queue.txt')
set_to_file(crawled,'crawled.txt')

