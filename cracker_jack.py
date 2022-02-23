import concurrent.futures
import multiprocessing
import random
import sys


def init(key_not_found):
    global KEY_NOT_FOUND
    KEY_NOT_FOUND = key_not_found


def cracker_jack(cpu, cur_key, end_key):
    print(f'CPU: {cpu} keyspace start at {cur_key} and end at {end_key}')
    while KEY_NOT_FOUND.value and (cur_key <= end_key):


if __name__ == "__main__":
    key = random.randrange(0, sys.maxsize)
    key_not_found = multiprocessing.Value('i', True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count, initializer=init, initargs=(key_not_found,)) as executor:
        for result in executor.map(cracker_jack, cpus, start_keys, end_keys):
            print(result)
