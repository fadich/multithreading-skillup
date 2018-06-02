import threading


def target(wait_event: threading.Event, set_event: threading.Event):
    thread = threading.current_thread()
    print('[{}] Entered thread'.format(thread.name))
    print('[{}] Waiting for event {}'.format(thread.name, wait_event))
    wait_event.wait()
    print(input('[{}] Input something: '.format(thread.name)))
    print('[{}] Setting event {}'.format(thread.name, set_event))
    set_event.set()
    print('[{}] Leaving thread'.format(thread.name))


if __name__ == '__main__':
    e1 = threading.Event()
    e2 = threading.Event()

    t1 = threading.Thread(target=target, args=(e1, e2))
    t2 = threading.Thread(target=target, args=(e2, e1))

    t1.start()
    t2.start()

    input('[Press Enter to continue...]')
    e1.set()

    print('<{}> is_alive: {}'.format(t1.name, t1.is_alive()))
    t1.join()
    print('<{}> is_alive: {}'.format(t1.name, t1.is_alive()))

    print('<{}> is_alive: {}'.format(t2.name, t2.is_alive()))
    t2.join()
    print('<{}> is_alive: {}'.format(t2.name, t2.is_alive()))

