import threading
import time


def target():
    tname = threading.current_thread().name
    for i in range(10):
        print('[{}] Calculating...'.format(tname))
        print('[{}] Sleeping...'.format(tname))
        time.sleep(0.01)

    print('[{}] Finished'.format(tname))


if __name__ == '__main__':
    t1 = threading.Thread(target=target)
    t2 = threading.Thread(target=target)

    t1.start()
    t2.start()

    print('{} is_alive: {}'.format(t1.name, t1.is_alive()))
    t1.join()
    print('{} is_alive: {}'.format(t1.name, t1.is_alive()))

    print('{} is_alive: {}'.format(t2.name, t2.is_alive()))
    t2.join()
    print('{} is_alive: {}'.format(t2.name, t2.is_alive()))
