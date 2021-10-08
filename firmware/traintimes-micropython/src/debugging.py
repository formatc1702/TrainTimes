debug_level = 2

def debug(level, *args, **kwargs):
    if debug_level >= level:
        print(*args, **kwargs)
