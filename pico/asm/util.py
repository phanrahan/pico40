def checku(u, len):
    max = 1 << len

    assert u < max

    return u & (max - 1)


def checks(i, len):
    min = -(1 << (len-1))
    max = 1 << len

    assert i >= min
    assert i <  max

    return i & (max - 1)
