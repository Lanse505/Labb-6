import multiprocessing
import concurrent.futures
import time
import numpy as np

LIMIT = 10001 # values up to 10001 is OK to wait for, 10s on my PC

# showing how to use an uint
np_val = np.uint32(LIMIT) 
MAX_FACT_VALUE = multiprocessing.Value('i', 0)

# https://stackoverflow.com/questions/56010428/how-to-share-state-when-using-concurrent-futures
def init_globals(fact_max):
    """init global variables for processes"""
    global MAX_FACT_VALUE
    MAX_FACT_VALUE = fact_max

# https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
def factorize(num):
    """factorize == what are the factors (divisors) for a specific number"""
    # the code below is just for showing how to use a global variable between processes
    # i.e. every process can read/write the MAX_FACT_VALUE.value
    # if num < MAX_FACT_VALUE.value:
    #     print(f'Current number: {num} and MAX_FACT_VALUE.value: {MAX_FACT_VALUE.value}\n')

    result = set()
    for i in range(1, int(num ** 0.5) + 1):
        div, mod = divmod(num, i)
        if mod == 0:
            result |= {i, div}
    return num, result


def main():
    """setup and receive result"""
    # the code below is just for showing how to use the global variable
    fact_max = multiprocessing.Value('i', np_val)
    numbers = range(1, fact_max.value)
    #numbers = range(1, 101)

    # If max_workers is None or not given, it will default to the number of processors on the machine
    # every core will do one factorization of a number, then take the next number until the whole work is done
    with concurrent.futures.ProcessPoolExecutor(max_workers=4, initializer=init_globals, initargs=(fact_max,)) as executor:
        for number, factors in executor.map(factorize, numbers):
            # for every finished process, print the number and the factorized factors (divisors)
            display(number, factors)


def display(number, factors):
    if len(factors) < 3:
        print(f'---> {number}: {factors}')   # prime#
    else:
        print(f'{number}: {factors}')


if __name__ == '__main__':
    start = time.perf_counter()
    # for i in range(LIMIT):
    #     number, factors = factorize(i)    # test without multiprocessing
    #     display(number, factors)
    main()
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} seconds')