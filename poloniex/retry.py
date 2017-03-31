# http://code.activestate.com/recipes/580745-retry-decorator-in-python/
import logging
from itertools import chain
from time import sleep

def retry(delays=(0, 1, 5, 30, 180, 600, 3600),
          exception=Exception,
          logger=logging.getLogger(__name__)):
    def wrapper(function):
        def wrapped(*args, **kwargs):
            problems = []
            for delay in chain(delays, [ None ]):
                try:
                    return function(*args, **kwargs)
                except exception as problem:
                    problems.append(problem)
                    if delay is None:
                        logger.error("retryable failed definitely:", problems)
                        raise
                    else:
                        logger.warn("retryable failed:", problem)
                        logger.info("-- delaying for %ds", delay)
                        sleep(delay)
        return wrapped
    return wrapper
