from __future__ import annotations

import threading
from queue import Queue, Empty
from typing import Optional
import sys
import time

class DataWriter:
    def __init__(self, file_path_on_disk: str):
        self.file_path_on_disk = file_path_on_disk
        self.queue = Queue()
        self.is_closed = False
        self.writer_worker = threading.Thread(target=self._run_writer)
        self.writer_worker.start()
        
    def push(self, data: str) -> None:
        assert not self.is_closed, "DataWriter is closed"
        self.queue.put(data)

    def close(self) -> None:
        self.is_closed = True
        self.writer_worker.join()

    # Internal worker logic
    def _run_writer(self) -> None:
        while not self.is_closed:
            try:
                data = self.queue.get()
                print("write data to disk: ", data)
            except:
                continue

if __name__ == "__main__":
    dw = DataWriter("a.txt")
    def producer(data: str):
        for i in range(10):
            dw.push("{}:{}".format(data, i))

    threads = []
    for i in range(3):
        threads.append(threading.Thread(target=producer, args=(chr(ord('a') + i),)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    time.sleep(1)
    dw.close()