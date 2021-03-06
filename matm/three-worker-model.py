from random import uniform, random
from time import sleep, time
from queue import Queue, Empty
from threading import Thread, Lock

import logging

TASK_EDUCATIONAL = 0
TASK_TECHNICAL = 1
TASK_TYPES = ('EDUCATIONAL', 'TECHNICAL')

TIME_RATE = 1 / 60 / 60

QUEUE_GET_TIMEOUT = 100 * TIME_RATE

PROBABILITY_EDUCATIONAL = 0.8
PROBABILITY_TECHNICAL = 0.2

TIME_REQUEST_PERIOD = (3 * 60 * TIME_RATE, 7 * 60 * TIME_RATE)  # 5±2 min
TIME_REQUEST_PREPARE = (1 * 60 * TIME_RATE, 3 * 60 * TIME_RATE)  # 2±1 min
TIME_SEARCH_EDUCATIONAL = (2 * 60 * TIME_RATE, 10 * 60 * TIME_RATE)  # 6±4 min
TIME_SEARCH_TECHNICAL = (5 * 60 * TIME_RATE, 11 * 60 * TIME_RATE)  # 8±3 min
TIME_RESULT_OUTPUT = (1 * 60 * TIME_RATE, 1 * 60 * TIME_RATE)  # 1 min

TIME_SIMULATION = 600 * 60 * TIME_RATE  # 10 hours


logging.basicConfig(
    level=logging.INFO,
    format='[%(client)s] %(asctime)s: %(message)s')
logger = logging.getLogger()


def worker(q: Queue, stop: Lock):
    ex = {'client': 'WORKER'}

    while not stop.locked():
        # For exit thread in stopping simulation.
        try:
            task_id = q.get(timeout=QUEUE_GET_TIMEOUT)
        except Empty:
            continue

        logger.info('New task - {}'.format(TASK_TYPES[task_id]), extra=ex)

        search_time = uniform(*TIME_SEARCH_EDUCATIONAL) \
            if task_id == TASK_EDUCATIONAL else uniform(*TIME_SEARCH_TECHNICAL)

        sleep(search_time)
        logger.info('Task completed in {:.2f} min'.format(search_time),
                    extra=ex)

        output_time = uniform(*TIME_RESULT_OUTPUT)
        sleep(output_time)
        logger.info('Results output in {:.2f} min'.format(output_time),
                    extra=ex)

        q.task_done()


def terminal(q: Queue, worker_q: Queue, task_type: int, stop: Lock):
    ex = {'client': '{} TERMINAL'.format(TASK_TYPES[task_type])}

    while not stop.locked():
        # For exit thread in stopping simulation.
        try:
            task_id = q.get(timeout=QUEUE_GET_TIMEOUT)
        except Empty:
            continue

        logger.info('New request', extra=ex)
        prepare_time = uniform(*TIME_REQUEST_PREPARE)
        sleep(prepare_time)
        logger.info('Results prepared in {:.2f} min'.format(prepare_time),
                    extra=ex)

        worker_q.put(task_id)

        q.task_done()


if __name__ == '__main__':
    extra = {'client': 'MAIN'}

    stop_lock = Lock()  # Stop simulation locker.

    worker_queue = Queue()  # Computing system queue.
    educational_queue = Queue()  # Terminal queue.
    technical_queue = Queue()  # Terminal queue.

    worker_thread = Thread(target=worker, args=(worker_queue, stop_lock))
    e_terminal_thread = Thread(
        target=terminal, daemon=True,
        args=(educational_queue, worker_queue, TASK_EDUCATIONAL, stop_lock))
    t_terminal_thread = Thread(
        target=terminal, daemon=True,
        args=(technical_queue, worker_queue, TASK_TECHNICAL, stop_lock))

    started_at = time()

    worker_thread.start()
    e_terminal_thread.start()
    t_terminal_thread.start()

    logger.info('Starting simulation. Waiting for user...', extra=extra)

    while time() - started_at < TIME_SIMULATION:

        waiting_time = uniform(*TIME_REQUEST_PERIOD)
        sleep(waiting_time)

        if random() < 0.8:
            task = TASK_EDUCATIONAL
            queue = educational_queue
        else:
            task = TASK_TECHNICAL
            queue = technical_queue

        queue.put(task)

        logger.info('New user request. Waiting time - {:.2f}. Task - {}'.format(
                waiting_time, TASK_TYPES[task]
            ), extra=extra)

    print('<SIMULATION STOPPED>')

    with stop_lock:
        worker_thread.join()
        print('Worker thread joined.')
        e_terminal_thread.join()
        print('Educational Terminal thread joined.')
        t_terminal_thread.join()
        print('Technical Terminal thread joined.')

    logger.info('''Simulation completed.

    Details:
     - Worker queue len = {}.
     - Educational terminal queue len = {}.
     - Technical terminal queue len = {}.
    '''.format(
        len(worker_queue.queue),
        len(educational_queue.queue),
        len(technical_queue.queue)
    ), extra=extra)
