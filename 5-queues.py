import queue
import threading
import time


def target():
    thread = threading.current_thread()
    print('[{}] Entered thread'.format(thread.name))

    for i in range(10):
        time.sleep(0.075)

