import urllib2
import os
#from urllib.request import urlopen
from urllib2 import urlopen
from link_finder import LinkFinder
from domain import *
from general import *

from datetime import datetime

fifopath1 = "my_result.fifo"
class Spider:

    global fifopath1
    #os.mkfifo(fifopath1)
    ########################
    #project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, base_url, domain_name):
        
        #Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = 'queue.txt'
        #Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.crawled_file = 'crawled.txt'
        #self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        #create_project_dir(Spider.project_name)
        create_data_files(Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        global fifopath1
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            print(datetime.now().strftime("%H:%M:%S")+'\n')
            crawl_time=datetime.now().strftime("%H:%M:%S")
             
            Spider.add_links_to_queue(Spider.gather_links(page_url),page_url,crawl_time)
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            #response = urllib2.urlopen(page_url)
            request = urllib2.Request(page_url)
            response = urllib2.urlopen(request)
            
            u = response.info().getheader('Content-Type')
            if u.startswith('text/html'):
            #if 'text/html' in response.getheader('Content-Type'):

                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links,page_url1,crawl_time):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)
            ############################
            global fifopath1
            linetofeed=page_url1+" "+url+" "+crawl_time

            try:
                fifo1 = open(fifopath1, "w")
                fifo1.write(linetofeed+"\n")
                #time.sleep(1)
                fifo1.close()
            except Exception as e:
                print("OS fifo error ..")

            ############################
            


    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
