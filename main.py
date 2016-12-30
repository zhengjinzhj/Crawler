#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread, currentThread  # thread = worker
from Queue import Queue  # queue = job
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'pingan'
HOMEPAGE = 'http://pws.paic.com.cn'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 4
queue = Queue()  # thread queue
# One and only one instance of Spider, the first spider, the 'main thread'
# Do something special - make directory, crawl the homepage and make files
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# 3. Create worker threads (will die when main exits)
def create_workers():  # create spiders
    for _ in range(NUMBER_OF_THREADS):
        worker = Thread(target=work)
        # Setting daemon to True will let the main thread exit even thought the worker threads are blocking
        # And the worker threads WILL die when main exits
        worker.daemon = True
        worker.start()
        # worker.join()  # Main thread will wait until worker threads die or just some seconds (*)


# 4. Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(currentThread().name, url)  # the workers' job, just get a page url and crawl it
        queue.task_done()  # tell the os that it's ready to do another job


# 2. Each queued link is a new job, put all the jobs to the thread queue, like a to-do list
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()  # thread queue manages the workers, deliver job to them
    crawl()  # check again after creating jobs


# 1. Check if there are items in the queue.txt, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print str(len(queued_links)) + ' links in the queue.'
        create_jobs()
    else:
        print 'No more link in the queue.'

create_workers()
crawl()
