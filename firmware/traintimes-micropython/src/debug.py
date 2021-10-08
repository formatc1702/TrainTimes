debug_level = 2

def debug(level, contents, end='\n'):
    if level >= debug_level:
        print(contents, end=end)
