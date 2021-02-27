def enumerate(iterable, start=0):
    count = start
    for elem in iterable:
        yield count, elem
        count += 1
