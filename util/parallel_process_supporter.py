# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 9. 30.
"""
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

from tqdm import tqdm


def parallel_process(func, params, process_multiplier=None, use_kwargs=False, front_num=1, timeout=None):
    """
    A parallel version of the map function with a progress bar.

    :param params: (array-like) The parameters to iterate over.
    :param func: (function) A python function to apply to the elements of array
    :param process_multiplier: (int, default=None) The multiplier of processes.
        When the processes variable is None, the processes variable become os.cpu_count() or 1
    :param use_kwargs: (boolean, default=False) Whether to consider the elements of array as dictionaries of
        keyword arguments to function
    :param front_num: (int, default=1) The number of iterations to run serially before kicking off the parallel job.
        Useful for catching bugs
    :param timeout: (int, default=None) The maximum number of seconds to wait. If None, then the timeout become
        (# of array + 3).

    :return results: (?) The result of futures.
    """
    # Set the processes. If getting cpu count is failed, use 1.
    processes = os.cpu_count() or 1
    if type(process_multiplier) is int:
        processes = processes * process_multiplier

    print('# of processes:{}'.format(processes))
    # Set the timeout.
    if timeout is None:
        timeout = len(params) + 3
    # We run the first few iterations serially to catch bugs
    front = []
    if front_num > 0:
        front = [func(**a) if use_kwargs else func(a) for a in params[:min(front_num, len(params))]]
    # If we set n_jobs to 1, just run a list comprehension. This is useful for benchmarking and debugging.
    if processes == 1:
        [func(**a) if use_kwargs else func(a) for a in tqdm(params[front_num:])]
    # Assemble the workers
    with ProcessPoolExecutor(max_workers=processes) as pool:
        # Pass the elements of array into function
        if use_kwargs:
            futures = [pool.submit(func, **a) for a in params[front_num:]]
        else:
            futures = [pool.submit(func, a) for a in params[front_num:]]
        kwargs = {
            'total': len(futures),
            'unit': 'it',
            'unit_scale': True,
            'leave': True
        }
        # Print out the progress as tasks complete
        # Set the timeout as (# of tasks + 3) seconds.
        for _ in tqdm(as_completed(futures, timeout), **kwargs):
            pass
    out = []
    # Get the results from the futures.
    for i, future in tqdm(enumerate(futures)):
        try:
            out.append(future.result())
        except Exception as e:
            out.append(e)
    results = front + out
    return results
