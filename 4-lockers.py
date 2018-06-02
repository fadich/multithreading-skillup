import threading
import time


def target(lock: threading.Lock):
    thread = threading.current_thread()
    print('[{}] Entered thread'.format(thread.name))

    for i in range(150):
        with lock:
            print('[{}] {}'.format(thread.name, i))
            time.sleep(0.075)

        """It's the same for:
        ```
            lock.acquire()
            print('[{}] {}'.format(thread.name, i))
            time.sleep(0.075)
            lock.release()
        ```
        """


if __name__ == '__main__':
    locker = threading.Lock()

    t1 = threading.Thread(target=target, args=(locker, ))
    t2 = threading.Thread(target=target, args=(locker, ))

    try:
        t1.start()
        t2.start()
    except KeyboardInterrupt:
        pass
    finally:
        t1.join()
        t2.join()



