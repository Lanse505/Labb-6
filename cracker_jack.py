import concurrent.futures
from http.client import FOUND
import multiprocessing
import numpy as np
import random
import time

LIMIT = 42069  # values up to 42069 is OK to wait for, 10s on my PC
KEY_NOT_FOUND = multiprocessing.Value('i', True)

def init(key_not_found, key):
    global KEY
    global KEY_NOT_FOUND
    KEY = key
    KEY_NOT_FOUND = key_not_found

def cracker_jack(cpu, start_key, end_key):
    print(f'CPU: {cpu} keyspace start at {start_key} and end at {end_key}\n')
    print(f'Secret Key: {KEY}\n')
    while KEY_NOT_FOUND.value and (start_key <= end_key):
        for i in range(start_key, end_key):
            print(f'CPU: {cpu} checking Key: {i} \n')
            if not KEY_NOT_FOUND.value:
                return f'Ending operations of CPU: {cpu} early due to the key being found!'
            if (i == KEY):
                KEY_NOT_FOUND.value = False
                return f'CPU: {cpu} found Key: {i}'
            elif i != KEY and i == end_key:
                return f'CPU: {cpu} ended operators after reaching "end_key" value: {end_key}'
        
if __name__ == "__main__":
    key = random.randrange(0, 4294967295)
    key_not_found = multiprocessing.Value('i', True)
    cpu_count = multiprocessing.cpu_count()
    cpus = [x for x in range(cpu_count)]
    start_keys = [0, 1073741823, 2147483646, 3221225469]
    end_keys = [1073741823, 2147483646, 3221225469, 4294967295]
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count, initializer=init, initargs=(key_not_found, 1000,)) as executor:
        for result in executor.map(cracker_jack, cpus, start_keys, end_keys):
                print(result)
