import threading
import time

import cotyledon


class PrinterSerivce(cotyledon.Service):
    name = "printer"

    def __init__(self, worker_id):
        super(PrinterSerivce, self).__init__(worker_id)
        self._shutdown = threading.Event()

    def run(self):
        while not self._shutdown.is_set():
            print("Doing stuff")
            time.sleep(1)

    def terminate(self):
        self._shutdonw.set()


# manager 생성
manager = cotyledon.ServiceManager()
# PrinterService 2개를 실행하기 위해 추가
manager.add(PrinterSerivce, 2)
manager.run()

