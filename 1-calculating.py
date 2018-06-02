import threading


def target(n=50):
    tname = threading.current_thread().name
    print('[{}] Calculating...'.format(tname))

    # Calculating Fibonacci
    a, b = 0, 1
    for x in range(n):
        a, b = b, a + b

    print('[{}] Finished with result: {}'.format(tname, a))


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
