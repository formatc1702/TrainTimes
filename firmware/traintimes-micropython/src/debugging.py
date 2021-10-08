import gc

debug_level = 2

def debug(level, *args, **kwargs):
    if debug_level >= level:
        print(*args, **kwargs)

def debug_free_memory(level):
    debug(level, f'Free memory: {gc.mem_free()}')
