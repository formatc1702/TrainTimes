tuplelist = [('cat', 'dog'), ('hello', 'goodbye'), ('pretty', 'ugly')]
if 'goodbye' in (x[1] for x in tuplelist):
    print "match was found"
