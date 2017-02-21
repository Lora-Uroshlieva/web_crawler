import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'nebo15'
HOME_PAGE = 'http://nebo15.com/'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)


# Create worker threads (will die when main exists)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# check if there are items in the queue , if so - crawl them
def crawl():
    queued_linls = file_to_set(QUEUE_FILE)
    if len(queued_linls) > 0:
        print(str(len(queued_linls)) + ' links in queue')
        create_jobs()


create_workers()
crawl()
