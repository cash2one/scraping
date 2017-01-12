from queue import Queue
import  threading
import requests
import time
from BaiduHotwords import SearchByBaiduHotwords
from  gzhTor import SougouGzhTitleSearch
from daemon import runner
import daemon
import logging

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/var/run/testdaemon/testdaemon.pid'
        self.pidfile_timeout = 5

    def run(self):
        # main()
        while True:
            #Main code goes here ...
            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
            logging.info("11111111")
            time.sleep(1)
            # for i in range(2):
            #     t = ThreadUrl(queue)
            #     t.setDaemon(False)
            #     t.start()
            # queue.put('baidu')
            # queue.put('sougou')
            # queue.join()


app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/testdaemon/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)
daemon_runner = runner.DaemonRunner(app)
daemon_runner.daemon_context.files_preserve = [handler.stream]
daemon_runner.do_action()