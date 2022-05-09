import time


def __select_seed() -> int:
    return int(time.time())


SEED = __select_seed()
